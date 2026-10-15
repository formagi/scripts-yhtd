# Conjectura de Collatz

Implementação didática da **Conjectura de Collatz**, que exibe, passo a passo, toda a sequência partindo de um inteiro positivo `N` até atingir o `1`, informando ao final o **total de passos** necessários e o **maior valor** atingido no caminho.

O cálculo da sequência é feito por uma **função recursiva**: cada chamada é um passo da conjectura.

## A teoria

A Conjectura de Collatz (também conhecida como problema `3n + 1`) foi proposta pelo matemático alemão **Lothar Collatz** em 1931. Enunciada em termos simples, tornou-se uma das conjecturas mais famosas da matemática — e uma das menos demonstráveis.

### A regra

Partindo de um inteiro positivo `N`, repita o processo:

- se `n` for **par**, vá para `n / 2`;
- se `n` for **ímpar**, vá para `3 × n + 1`.

A conjectura afirma que, **para qualquer `N` inicial, a sequência sempre termina no ciclo `4 → 2 → 1`**.

### Exemplo clássico

Para `N = 6`:

```
6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
```

São **8 passos** e o maior valor atingido é `16`. Note como a sequência sobe e desce sem padrão aparente — é justamente essa imprevisibilidade que torna o problema tão difícil.

### O que se sabe (e o que não se sabe)

- A conjectura **nunca foi provada**. Não existe demonstração formal de que toda sequência termina em `1`.
- Foi verificada **computacionalmente** para enormes intervalos de entrada (até valores da ordem de `2^60` e além), sem encontrar exceção — mas verificação finita não é prova.
- O único ciclo conhecido é o trivial `4 → 2 → 1`. Não se sabe se existem outros (ciclos maiores foram buscados e não encontrados).
- Toda sequência já observada, antes de cair no ciclo, alcança alguma **potência de 2** — a partir daí o caminho até o `1` é inevitável.
- A função `3n + 1` cresce rápido para ímpares, mas a divisão por `2` subsequente derruba o valor: por isso as sequências oscilam, em vez de divergirem.

Vale notar: o problema é enunciado em uma frase, entendido por qualquer estudante — e resiste a séculos de tentativas. Paul Erdős chegou a dizer: *"A matemática talvez não esteja pronta para um problema desse tipo."*

## Como usar

O script está em [script-collatz.py](./script-collatz.py) e requer Python 3 (sem dependências externas).

```shell
# concede permissão de execução (se necessário)
chmod u+x ./script-collatz.py

# informa o valor inteiro positivo N como argumento
./script-collatz.py 27
```

Se nenhum valor for informado como argumento, o script pergunta no terminal. Caso a entrada não seja interativa (por exemplo, em um pipeline), ele orienta o uso e encerra com código de erro.

### Parâmetros

| Parâmetro | Descrição |
| --- | --- |
| `N` (posicional, opcional) | Valor inteiro positivo inicial, até `1000000`. Se omitido, solicitado interativamente. |
| `-s [SEGUNDOS]`, `--sleep [SEGUNDOS]` | Pausa, em segundos, após cada passo. Sem valor, usa `0.5`. Sem a opção, não pausa. |

Validações: aceita apenas números inteiros maiores que zero e até `1000000`; entradas como `abc`, `-5`, `0`, `2.5` ou `1000001` são rejeitadas com código de saída `1`.

### Exemplo de execução

```shell
$ ./script-collatz.py 6
>> Conjectura de Collatz para N = 6
>> (par: n/2 | ímpar: 3 × n + 1 | recursão: limite 10000 frames)

>> Passo 1: 6 é par  →  6 / 2 = 3
>> Passo 2: 3 é ímpar  →  3 × 3 + 1 = 10
>> Passo 3: 10 é par  →  10 / 2 = 5
>> Passo 4: 5 é ímpar  →  3 × 5 + 1 = 16
>> Passo 5: 16 é par  →  16 / 2 = 8
>> Passo 6: 8 é par  →  8 / 2 = 4
>> Passo 7: 4 é par  →  4 / 2 = 2
>> Passo 8: 2 é par  →  2 / 2 = 1

>> Sequência: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
>> Total de passos: 8
>> Maior valor atingido: 16
```

Para ver os passos com pausa:

```shell
$ ./script-collatz.py 27 -s 0.5
```

O número `27` é um clássico: leva **111 passos** para chegar ao `1` e atinge o pico de `9232`.

## A implementação: recursão

A função `collatz()` do script **é** o laço da conjectura — não há `while` nem `for` percorrendo os passos. Em vez disso:

- **Caso-base:** se `n == 1`, a sequência terminou; retorna `(0, 1)` — zero passos restantes.
- **Passo recursivo:** imprime o passo (`n/2` ou `3n+1`) e chama a si mesma para o próximo valor, somando `1` ao resultado da sub-sequência e propagando o maior valor encontrado.

```python
def collatz(n, passo, pausa, sequencia):
    sequencia.append(n)
    if n == 1:
        return 0, 1

    if n % 2 == 0:
        proximo = n // 2          # par → n/2
    else:
        proximo = 3 * n + 1       # ímpar → 3n+1

    passos_restantes, maior_restante = collatz(proximo, passo + 1, pausa, sequencia)
    return 1 + passos_restantes, max(n, maior_restante)
```

Cada nível da pilha de chamadas devolve o par **`(total de passos, maior valor)`** da sua sub-sequência — ao final da primeira chamada, esses valores são exatamente o resumo impresso pelo script.

### A limitação da recursão (importante)

Escolher a recursão traz uma consequência prática que este projeto trata de forma explícita:

- **A profundidade da pilha de recursão é igual ao número de passos** da sequência. Para `N = 27`, são 111 frames empilhados.
- O Python limita a profundidade de recursão (padrão: `1000` frames), porque cada frame ocupa espaço na pilha real do processo. O script eleva esse limite para `10000` com `sys.setrecursionlimit(10_000)`.
- Para garantir que a pilha nunca estoure, o script aceita apenas **`N ≤ 1000000`**: o pior caso (`837799`) leva cerca de `525 passos` — muito abaixo do limite configurado, mesmo para valores bem maiores que o exigido.
- Caso o limite fosse ultrapassado, o Python interromperia a execução com **`RecursionError`** (um erro legível, com *traceback*), e não com um crash do processo.
- Uma versão **iterativa** (com `while`) eliminaria completamente essa limitação — a recursão foi escolhida aqui por didatismo, pois ilustra bem a natureza "repetida até o caso-base" da conjectura.

## Ferramentas de IA utilizadas

Este trabalho — o plano, o código do script e esta documentação — foi desenvolvido com o auxílio do **OpenCode**, utilizando o modelo **`opencode/big-pickle`**, além de revisão humana. As decisões de projeto (incluindo a escolha pela implementação recursiva e o tratamento da limitação de pilha) foram discutidas e aprovadas previamente, e o resultado foi verificado por execução do script contra casos conhecidos (por exemplo, `6 → 8 passos`, `27 → 111 passos com pico 9232` e `1 → 0 passos`).

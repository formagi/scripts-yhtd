# Crivo de Erastótenes

Implementação didática do **Crivo de Erastótenes**, que exibe, passo a passo, a remoção dos números não primos de uma listagem de `0` até um valor inteiro positivo `N`, apresentando ao final os valores primos encontrados.

## A teoria

O crivo de Erastótenes é um algoritmo milenar para encontrar todos os números primos até um limite `N`. O nome é uma homenagem a **Eratóstenes de Cirene** (c. 276–194 a.C.), matemático grego que também ficou conhecido por estimar a circunferência da Terra.

A ideia central é simples: começamos com a lista de todos os inteiros de `0` a `N` e vamos **eliminando** os números que sabidamente não são primos. Ao final, os sobreviventes são exatamente os primos.

### O que é um número primo?

Um número natural é **primo** quando possui **exatamente dois divisores positivos distintos**: o `1` e ele mesmo.

Disso decorrem dois casos que costumam gerar dúvida:

- **0 não é primo.** Todo inteiro positivo divide o `0` (`0 / k = 0`), então o `0` teria infinitos divisores — não exatamente dois.
- **1 não é primo.** O `1` possui um único divisor positivo (o próprio `1`), e não dois.

Por isso o script os remove logo no **Passo 0**, antes de iniciar o crivo propriamente dito.

### Como o crivo funciona

1. Escreva a lista `2, 3, 4, ..., N`.
2. O primeiro número é o `2`, que é primo. Em seguida, **risque todos os múltiplos de 2** maiores que ele (`4, 6, 8, ...`).
3. O próximo número não riscado é o `3`, que também é primo. Risque os múltiplos de `3`.
4. Repita o processo para cada número não riscado. Ao final, os números que sobraram são os primos.

### Dois fatos que otimizam o crivo

**Fato 1 — basta testar primos `p ≤ √N`.**
Se um número `n ≤ N` é composto, ele pode ser escrito como `n = a · b` com `1 < a ≤ b < n`. Daí `a ≤ √n ≤ √N`. Como `a` é composto ou primo, e todo composto possui um fator primo, existe um primo `p ≤ a ≤ √N` que divide `n`. Ou seja: **todo composto possui um fator primo menor ou igual a `√N`**. Por isso o laço principal do script percorre apenas `p` de `2` até `⌊√N⌋`. Os números maiores que `√N` que sobreviveram à crivagem são automaticamente primos.

**Fato 2 — podemos começar a riscar em `p²`.**
Ao processar o primo `p`, os seus múltiplos `p, 2p, ..., (p-1)p` já foram removidos por primos menores que `p` (por exemplo, `2p` saiu quando crivamos o `2`, `3p` saiu quando crivamos o `3`). Logo, o primeiro múltiplo de `p` ainda presente na lista é `p²`. É por isso que o script inicia a remoção em `p²`. Essa também é a razão pela qual o script informa quantos múltiplos de `p` já haviam sido removidos: são exatamente os `p - 1` múltiplos menores que `p²`.

Cada número composto é, portanto, atribuído ao **seu menor fator primo** — é justamente o "passo" em que ele é removido.

### Complexidade

O crivo executa em tempo `O(N log log N)` e usa `O(N)` de memória. É muito mais eficiente do que testar a primalidade de cada número individualmente.

## Como usar

O script está em [script-crivo.py](./script-crivo.py) e requer Python 3 (sem dependências externas).

```shell
# concede permissão de execução (se necessário)
chmod u+x ./script-crivo.py

# informa o valor inteiro positivo N como argumento
./script-crivo.py 30
```

Se nenhum valor for informado como argumento, o script pergunta no terminal. Caso a entrada não seja interativa (por exemplo, em um pipeline), ele orienta o uso e encerra com código de erro.

### Parâmetros

| Parâmetro | Descrição |
| --- | --- |
| `N` (posicional, opcional) | Valor inteiro positivo; limite superior da listagem. Se omitido, solicitado interativamente. |
| `-s [SEGUNDOS]`, `--sleep [SEGUNDOS]` | Pausa, em segundos, após cada passo. Sem valor, usa `0.5`. Sem a opção, não pausa. |

Validações: aceita apenas números inteiros maiores que zero; entradas como `abc`, `-5`, `0` ou `2.5` são rejeitadas com código de saída `1`.

### Exemplo de execução

```shell
$ ./script-crivo.py 30
>> Consulta ao crivo de Erastótenes para N = 30

>> Passo 0: 0 e 1 não são primos e são removidos da listagem.
   0 não é primo: todo inteiro positivo divide o 0.
   1 não é primo: possui um único divisor positivo (o próprio 1),
   enquanto a definição exige exatamente dois divisores positivos distintos.
>> Passo 1: 2 é primo (não foi removido por nenhum fator menor).
   Removendo múltiplos de 2 a partir de 4: 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30
   (1 múltiplo(s) de 2 menores que 4 já haviam sido removidos por primos menores.)
>> Passo 2: 3 é primo (não foi removido por nenhum fator menor).
   Removendo múltiplos de 3 a partir de 9: 9, 15, 21, 27
   (2 múltiplo(s) de 3 menores que 9 já haviam sido removidos por primos menores.)
>> Passo 3: 5 é primo (não foi removido por nenhum fator menor).
   Removendo múltiplos de 5 a partir de 25: 25
   (4 múltiplo(s) de 5 menores que 25 já haviam sido removidos por primos menores.)

>> Valores primos encontrados até 30:
   2, 3, 5, 7, 11, 13, 17, 19, 23, 29
>> Total: 10 primo(s) — pi(30) = 10
```

Para ver os passos com pausa:

```shell
$ ./script-crivo.py 100 -s 0.5
```

## Ferramentas de IA utilizadas

Este trabalho — o plano, o código do script e esta documentação — foi elaborado com o auxílio de um **AI-Assistant**, utilizando o modelo **`opencode/big-pickle`**, além de revisão humana. As decisões de projeto foram discutidas e aprovadas previamente, e o resultado foi verificado por execução do script contra casos conhecidos (por exemplo, `π(30) = 10`, `π(100) = 25` e `π(10000) = 1229`).

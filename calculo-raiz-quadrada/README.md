# Cálculo de raíz quadrada pelo "Método de Júlia"
Se você encontrou esse repositório ainda no ano de 2023, ou muito próximo disso, você deve ter visto sobre a Júlia, uma menina de 11 anos que apresentou uma sugestão alternativa para calcular a raíz quadrada de um número. O método foi apelidade de "Regressão de Júlia", ou ["Método de Júlia"](https://g1.globo.com/jornal-nacional/noticia/2023/11/10/aluna-de-11-anos-ajuda-a-desenvolver-formula-para-descobrir-raiz-quadrada-de-uma-nova-maneira.ghtml).

Antes de tudo, vou tentar descrever o método, para entendermos melhor. Vamos tentar descobrir a raíz quadrada do número 169. Para isso, vou começar com um número próximo, do qual eu já conheço a raíz quadrada, no caso, o 100 (a raíz de 100 é 10). O método consistem em somar ao 100, o número 10, sua raíz, e próximo a este, o número 11, se o resultado da soma não for o número 169, repete-se o processo, com os números subsequentes. Veja no exemplo abaixo:
```
100 + 10 + 11 = 121 (ainda não chegamos no número 169)
121 + 11 + 12 = 144 (ainda não chegamos no número 169)
144 + 12 + 13 = 169 (chegamos no número 169!)
```
Em nosso caso, o último número somado foi o 13, logo a raíz quadrada de 169 é 13. Você pode usar uma calculadora para multiplicar 13 por 13, para remover a dúvida, se estiver tentando.

## Sugestão de atividade
A ideia aqui é tentarmos escrever um `script shell` que calcule a raíz quadrada usando do "Método de Júlia".

O script receberá dois parâmetros:

- Primeiro (A): um número do qual se deseja descobrir a raíz quadrada.
- Segundo (B): um número de uma raíz quadrada próxima.

Definição dos parâmetros:
- A e B são números inteiros.
- A e B são números maiores que zero.
- Se B for multiplicado por ele mesmo, o resultado terá de ser menor que A, logo: (B * B) < A.

Como adicional, quero incluir: 
- Validar dos valores de entrada.
    - Somente números inteiros.
    - Somente número maiores que zero.
    - Somente dois parâmetros para a execução do script.
- Validar se existe uma raíz quadrada exata, como resultado.

Confira no [script-raiz-quadrada.sh](./script-raiz-quadrada.sh) a implementação do código.

## Como usar

```shell
# conceda permissão de execução no script
chmod u+x ./script-raiz-quadrada.sh

# informe dois parâmetros
./script-raiz-quadrada.sh 100 10
```

#### Exemplo de execução
```shell
$ ./script-raiz-quadrada.sh 169 13
.. ( 100 + 10 + 11 ) = 121
.. ( 121 + 11 + 12 ) = 144
.. ( 144 + 12 + 13 ) = 169
>> A raiz de 169 é: 13
```
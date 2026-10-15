#!/usr/bin/env python3
"""Exemplifica a Conjectura de Collatz, passo a passo, por recursão.

Recebe um inteiro positivo N e exibe, um a um, os passos da sequência
de Collatz (par: n/2; ímpar: 3n+1) até atingir 1, informando ao final
o total de passos necessários e o maior valor atingido no caminho.

A própria sequência é calculada por função recursiva: cada chamada é
um passo, o caso-base é n == 1, e o par (passos, maior valor) é
propagado de volta pela pilha de chamadas.
"""

import argparse
import sys
import time

# A profundidade da pilha é igual ao número de passos da sequência.
# O limite padrão do Python é 1000; 10000 dá folga para qualquer
# sequência partindo de N <= 10**6 (pior caso observado: ~525 passos).
LIMITE_RECURSAO = 10_000
LIMITE_N = 1_000_000


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Exemplifica a Conjectura de Collatz, mostrando os passos "
            "da sequência até atingir 1, por meio de função recursiva."
        ),
        epilog="Exemplo: ./script-collatz.py 27 -s 0.5",
    )
    parser.add_argument(
        "n",
        nargs="?",
        help="Valor inteiro positivo inicial (até 1000000).",
    )
    parser.add_argument(
        "-s",
        "--sleep",
        nargs="?",
        const=0.5,
        type=float,
        metavar="SEGUNDOS",
        help="Pausa, em segundos, após cada passo (padrão: 0.5).",
    )
    return parser.parse_args()


def obter_n(argumento):
    # Sem argumento: tenta ler interativamente; sem terminal, orienta o uso
    if argumento is None:
        if not sys.stdin.isatty():
            print(">> Informe um valor inteiro positivo como argumento", file=sys.stderr)
            sys.exit(1)
        try:
            argumento = input(">> Informe um valor inteiro positivo: ")
        except EOFError:
            print(">> Nenhum valor informado", file=sys.stderr)
            sys.exit(1)

    # Validação: aceitar somente números inteiros
    try:
        n = int(argumento)
    except ValueError:
        print(">> Informe apenas valores inteiros", file=sys.stderr)
        sys.exit(1)

    # Validação: aceitar somente números maiores que zero
    if n < 1:
        print(">> O valor informado precisa ser maior que zero", file=sys.stderr)
        sys.exit(1)

    # Validação: manter a profundidade da recursão dentro do limite
    if n > LIMITE_N:
        print(f">> O valor informado precisa ser menor ou igual a {LIMITE_N}",
              file=sys.stderr)
        sys.exit(1)

    return n


def pausa_entre(segundos):
    if segundos:
        time.sleep(segundos)


def collatz(n, passo, pausa, sequencia):
    # Caso-base: a sequência termina ao atingir 1 (0 passos restantes)
    sequencia.append(n)
    if n == 1:
        return 0, 1

    # Passo didático: par → n/2; ímpar → 3n+1
    if n % 2 == 0:
        proximo = n // 2
        print(f">> Passo {passo}: {n} é par  →  {n} / 2 = {proximo}")
    else:
        proximo = 3 * n + 1
        print(f">> Passo {passo}: {n} é ímpar  →  3 × {n} + 1 = {proximo}")

    pausa_entre(pausa)

    # Chamada recursiva: soma 1 passo ao resultado da sub-sequência
    passos_restantes, maior_restante = collatz(proximo, passo + 1, pausa, sequencia)
    return 1 + passos_restantes, max(n, maior_restante)


def main():
    sys.setrecursionlimit(LIMITE_RECURSAO)
    args = parse_args()
    n = obter_n(args.n)

    print(f">> Conjectura de Collatz para N = {n}")
    print(f">> (par: n/2 | ímpar: 3 × n + 1 | recursão: limite {LIMITE_RECURSAO} frames)")
    print()

    sequencia = []
    passos, maior = collatz(n, 1, args.sleep, sequencia)

    print()
    print(f">> Sequência: {' → '.join(map(str, sequencia))}")
    print(f">> Total de passos: {passos}")
    print(f">> Maior valor atingido: {maior}")


if __name__ == "__main__":
    main()

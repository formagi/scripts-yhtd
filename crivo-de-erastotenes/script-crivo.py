#!/usr/bin/env python3
"""Exemplifica o Crivo de Erastótenes, passo a passo.

Recebe um inteiro positivo N e exibe os passos de remoção dos números
não primos da listagem 0..N, apresentando ao final os valores primos
encontrados e a contagem pi(N).
"""

import argparse
import math
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Exemplifica o Crivo de Erastótenes, mostrando os passos "
            "de remoção dos números não primos até o valor informado."
        ),
        epilog="Exemplo: ./script-crivo.py 30 -s 0.5",
    )
    parser.add_argument(
        "n",
        nargs="?",
        help="Valor inteiro positivo (limite superior da listagem).",
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

    return n


def pausa_entre(segundos):
    if segundos:
        time.sleep(segundos)


def crivo(n, pausa):
    # Lista de controle: removido[k] == True significa que k saiu da listagem
    removido = [False] * (n + 1)

    print(f">> Consulta ao crivo de Erastótenes para N = {n}")
    print()

    # Passo 0: 0 e 1 não são primos, por definição, e são removidos de imediato
    removido[0] = True
    if n >= 1:
        removido[1] = True
    print(">> Passo 0: 0 e 1 não são primos e são removidos da listagem.")
    print("   0 não é primo: todo inteiro positivo divide o 0.")
    print("   1 não é primo: possui um único divisor positivo (o próprio 1),")
    print("   enquanto a definição exige exatamente dois divisores positivos distintos.")
    pausa_entre(pausa)

    # Basta testar p <= raiz(N): todo composto n <= N tem fator primo p <= raiz(N)
    limite = math.isqrt(n)
    passo = 1

    for p in range(2, limite + 1):
        if removido[p]:
            continue

        inicio = p * p
        removidos = [m for m in range(inicio, n + 1, p) if not removido[m]]

        print(f">> Passo {passo}: {p} é primo (não foi removido por nenhum fator menor).")
        if removidos:
            print(f"   Removendo múltiplos de {p} a partir de {inicio}: "
                  + ", ".join(map(str, removidos)))
        else:
            print(f"   Não há múltiplos de {p} para remover entre {inicio} e {n}.")

        # Múltiplos de p menores que p^2 (p, 2p, ..., (p-1)p) já saíram antes
        ja_removidos = p - 1
        if ja_removidos:
            print(f"   ({ja_removidos} múltiplo(s) de {p} menores que {inicio} "
                  f"já haviam sido removidos por primos menores.)")

        for m in removidos:
            removido[m] = True

        passo += 1
        pausa_entre(pausa)

    primos = [k for k in range(2, n + 1) if not removido[k]]

    print()
    print(f">> Valores primos encontrados até {n}:")
    if primos:
        print("   " + ", ".join(map(str, primos)))
    else:
        print("   (nenhum)")
    print(f">> Total: {len(primos)} primo(s) — pi({n}) = {len(primos)}")


def main():
    args = parse_args()
    n = obter_n(args.n)
    crivo(n, args.sleep)


if __name__ == "__main__":
    main()

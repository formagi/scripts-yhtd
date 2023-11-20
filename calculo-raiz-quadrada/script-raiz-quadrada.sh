#!/bin/bash

num_a=$1
num_b=$2

# Validação da quantidade de parâmetros repassados ao script
if [ ! $# -eq 2 ]; then
  printf ">> Informe dois parâmetros para poder executar o cálculo\n"
  exit 1
fi

# Validação dos valores, para aceitar somente números inteiros
if ! [[ "${num_a}" =~ ^[0-9]+$ ]] || ! [[ "${num_b}" =~ ^[0-9]+$ ]]; then
  printf ">> Informe apenas valores inteiros\n"
  exit 1
fi

# Validação dos valores, para aceitar somente números maiores que zero
if [ ${num_a} -le 0 ] || [ ${num_b} -le 0 ]; then
  printf ">> Os valores informados precisam ser maiores que zero\n"
  exit 1
fi

result=$((num_b * num_b))

# Validação dos valores, para somente se (B * B) < A
if [ ${result} -gt ${num_a} ]; then
  printf ">> (${num_b} * ${num_b}) = ${result}\n"
  printf ">> ${result} é maior que ${num_a}\n"
  exit 1
fi

# Execução do "Método de Júlia"
while [ ! ${num_a} -le ${result} ]; do
  printf ".. ( ${result} + ${num_b} + $((num_b + 1)) ) = "
  result=$(( result + num_b + ( num_b + 1) ))
  printf "${result}\n"
  num_b=$(( num_b + 1 ))
  sleep 0.5
done

# Validação para definir se há uma raíz quadrada exata, encontrada no cálculo
if [ ! ${result} -eq ${num_a} ]; then
  printf ">> Sem raiz exata.\n"
  exit 1
fi

# Impressão da resposta final
printf ">> A raiz de ${num_a} é: ${num_b}\n"
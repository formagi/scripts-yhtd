#!/bin/bash

set -e

function dt() { date +%F\ %T; }

function printlog() {
    printf "$(dt) - $1\n"
}

printlog "Inicio do script para manipulacao de repositorios do github\n"

read -p "## Informe o diretorio, onde sera feito o clone do repositorio: " repo_dir
cd "${repo_dir}"

read -p "## Informe a SSH URL do repositorio que sera feito o clone: " repo_ssh_url
git clone "${repo_ssh_url}"

repo_dir_name="$(cut -d "/" -f 2 <<< "${repo_ssh_url}" | cut -d '.' -f 1)"
cd "${repo_dir_name}"

git checkout main
git pull

read -p "## Informe o nome da nova branch: " repo_work_branch
git checkout -b "${repo_work_branch}"

read -p "## Informe o nome do novo projeto: " work_project
cp -rf ../../template/ "./${work_project}/"

while IFS='=' read -s conf value; do
    sed -e "s/%${conf}%/${value}/g" -i ./${work_project}/*
done < ../../inputs.cfg

git add --all "./${work_project}"
git commit -m "Mensagem de commit"
# put push origin "${repo_work_branch}"
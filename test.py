import argparse
import shlex

# Crie um objeto ArgumentParser
parser = argparse.ArgumentParser()

# Adicione os argumentos que você deseja analisar
parser.add_argument('--nome', help='Nome do usuário')
parser.add_argument('--idade', type=int, help='Idade do usuário')
parser.add_argument('-l', type=int, help='Contagem de mensagens')

# Defina a string que você deseja extrair os dados
command = '!comand --nome "Pedro Godoy" -l 2'

# Use shlex para fazer a divisão da string respeitando as aspas
command_split = shlex.split(command)

# Analise a lista de palavras
args = parser.parse_args(command_split[1:])

# Acesse os valores dos argumentos
nome = args.nome
idade = args.idade
limit = args.l
teste = 2

teste = teste - 1 if type(teste) == int else teste

# Exemplo de uso dos valores dos argumentos
print(f'Nome: {nome}')
print(f'Idade: {"yes" if idade == None else "no"}')
print(f'Limite: {limit}')
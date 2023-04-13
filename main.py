#!/usr/bin/env python3
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta

time_format = '%d/%m/%Y %H:%M'
left_format = '%d dias, %H horas e %M minutos'
filename = 'tarefas.csv'

def header(num):
    print('┅'*num)

def str_format_to_date(date):
    return dt.strptime(date, time_format)

def tempo_agora():
    return dt.now().strftime(time_format)

def date_diff(date1, date2, date_obj=False):
    if date_obj:
        delta_date = date2 - date1
        #delta_date = delta_date - timedelta(days=1)
        delta_date = dt.utcfromtimestamp(delta_date.total_seconds())
        return delta_date

    date1 = dt.strptime(date1, time_format)
    date2 = dt.strptime(date2, time_format)
    
    delta_date = date2 - date1
    #delta_date = delta_date - timedelta(days=1)
    
    delta_date = dt.utcfromtimestamp(delta_date.total_seconds())
    return delta_date

def read_chore(df, idx):
    header(50)
    agora = tempo_agora()
    
    if str_format_to_date(df.loc[idx]["dfim"]) < dt.now():
        restante = 'o prazo já acabou.'
    
    else:
        restante = date_diff(agora, df.loc[idx]["dfim"])
        restante = restante.strftime(left_format)

    print(f'Índice: {idx}')
    print(f'Matéria: {df.loc[idx]["materia"]}')
    print(f'Descrição: {df.loc[idx]["descricao"]}')
    print(f'Data de início: {df.loc[idx]["dinicio"]}')
    print(f'Data de fim: {df.loc[idx]["dfim"]}')
    print(f'Tempo restante: {restante}')
    print(f'Feito? {df.loc[idx]["feito"]}')

def add_chore(df):
    print('Qual é a matéria?')
    materia = input('>> ')

    print('\nDigite a descrição.')
    desc = input('>> ')

    print('\nDigite a data em que foi passada a tarefa no formato dia/mês/ano')
    data_inicio = input('>> ')

    print('\nDigite a data limite da tarefa no formato dia/mês/ano hora:minuto')
    data_fim = input('>> ')

    linha = {
        'materia': materia,
        'descricao': desc,
        'dinicio': data_inicio,
        'dfim': data_fim,
        'feito': 'n'
    }
    
    linha = pd.DataFrame(linha, index=[0])
    df = pd.concat([df, linha], ignore_index=True)

    print('Tarefa criada.')

    return df

def mark_done(df):
    print('Digite o índice da tarefa.')
    i = int(input('>> '))

    df.loc[i]['feito'] = 's'
    print('\nTarefa salva como feita.')
    
    return df

def mark_undone(df):
    print('Digite o índice da tarefa.')
    i = int(input('>> '))

    df.loc[i]['feito'] = 'n'
    print('\nTarefa salva como não feita')

    return df

def readi_chore(df):
    print('Digite o índice da tarefa.')
    i = int(input('>> '))
    read_chore(df, i)
    header(50)
    return df

def read_chores(df, ver_feito=True, apenas_feito=False):
    for i in range(len(df)):
        if not ver_feito:
            if df.loc[i]['feito'] == 's':
                pass
                continue

        if apenas_feito:
            if df.loc[i]['feito'] == 'n':
                pass
                continue
        read_chore(df, i)

    header(50)
    return df

def read_only_done(df):
    read_chores(df, apenas_feito=True)
    return df

def read_not_done(df):
    read_chores(df, ver_feito=False)
    return df

def edit_chore(df):
    print('Digite o índice da tarefa que você quer editar.')
    i = int(input('>> '))

    headers = ['materia', 'descricao', 'dinicio', 'dfim']

    branco = '(deixe em branco se quiser manter)'

    print(f'\nQual o novo nome da matéria? {branco}')
    materia = input('>> ')

    print(f'\nQual a nova descrição? {branco}')
    descricao = input('>> ')

    print(f'\nQual a nova data de início? {branco}')
    dinicio = input('>> ')

    print(f'\nQual a nova data de fim? {branco}')
    dfim = input('>> ')

    for h in headers:
        if locals()[h] != '':
            df.loc[i][h] = locals()[h]

    print(f'\nTarefa {i} editada.')
    return df

def delete_chore(df):
    print('Digite o índice da tarefa que vocÊ quer deletar.')
    i = int(input('>> '))

    df.drop(i)
    print(f'\nTarefa {i} deletada.')
    return df

def menu():
    print('[0] - Adicionar nova tarefa')
    print('[1] - Ler uma tarefa')
    print('[2] - Ler várias tarefas')
    print('[3] - Ler várias tarefas ainda não feitas')
    print('[4] - Ler várias tarefas já feitas')
    print('[5] - Marcar atividade como feita')
    print('[6] - Marcar atividade como não feita')
    print('[7] - Editar tarefa')
    print('[8] - Excluir tarefa')
    print('[9] - Fechar o programa')

def sair(df):
    print('Tem certeza que quer fechar o programa? (s/n)')
    ctz = input('>> ')
    if ctz == 's':
        print('\nSalvando mudanças...')
        df.to_csv(filename, sep=';', index=False)
        print('Mudanças salvas!')
        print('\nObrigado por usar!\nFeito por Cristian (aka Canário)')
        exit()

    return df

def main():
    func_opts = {
        0: add_chore,
        1: readi_chore,
        2: read_chores,
        3: read_not_done,
        4: read_only_done,
        5: mark_done,
        6: mark_undone,
        7: edit_chore,
        8: delete_chore,
        9: sair
    }

    df = pd.read_csv(filename, sep=';')
    header(30)
    print('  Agendinha')
    header(30)

    while True:
        print()
        menu()
        print()

        opcao = int(input('>> '))

        if opcao < 0 or opcao > 9:
            print('\nPor favor, insira uma opção válida.')
            continue

        print()
        df = func_opts[opcao](df)

if __name__ == '__main__':
    main()

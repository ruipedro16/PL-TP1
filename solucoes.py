import re

from graphviz import Source
from matplotlib import pyplot as plt


def alinea_a(processos_dict):
    x = []
    y = []

    for anos_dict in sorted(processos_dict.values(), key=lambda item: sorted(item)):
        for (ano, p) in sorted(anos_dict.items()):
            print(f'{ano}: {len(p)} processos')
            x.append(ano)
            y.append(len(p))
    print(f'Foram analisados {len(processos_dict)} seculos')

    min_seculo = min(processos_dict.keys())
    min_ano = min(processos_dict[min_seculo].keys())
    min_date = sorted(processos_dict[min_seculo][min_ano], key=lambda p: p.data)[0].data

    max_seculo = max(processos_dict.keys())
    max_ano = max(processos_dict[max_seculo].keys())
    max_date = sorted(processos_dict[max_seculo][max_ano], key=lambda p: p.data, reverse=True)[0].data

    print(f'Existem processos entre {min_date} e {max_date}')

    plt.style.use('seaborn')
    plt.bar(x, y, linestyle='solid', color='green')
    plt.title('Numero de Processos por Ano')
    plt.ylabel('Numero de Processos')
    plt.xlabel('Ano')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()


def nome_apelido_seculo(seculo, processos_dict):
    nomes_proprios = {}
    apelidos = {}
    for proc in processos_dict[seculo].values():
        for p in proc:
            nome = re.split(r'\s+', p.nome)
            nome_proprio = nome[0]
            apelido = nome[-1]
            try:
                nomes_proprios[nome_proprio] += 1
            except KeyError:
                nomes_proprios[nome_proprio] = 1
            try:
                apelidos[apelido] += 1
            except KeyError:
                apelidos[apelido] = 1
    nome = list(sorted(nomes_proprios.items(), key=lambda item: item[1], reverse=True))[:5]
    apelido = list(sorted(apelidos.items(), key=lambda item: item[1], reverse=True))[:5]
    return nome, apelido


def alinea_b(processos_dict):
    nomes_proprios = {}
    apelidos = {}

    for (sec, anos_dict) in processos_dict.items():
        for (ano, proc) in anos_dict.items():
            for p in proc:
                nome = re.split(r'\s+', p.nome)
                nome_proprio = nome[0]
                apelido = nome[-1]
                try:
                    nomes_proprios[nome_proprio] += 1
                except KeyError:
                    nomes_proprios[nome_proprio] = 1
                try:
                    apelidos[apelido] += 1
                except KeyError:
                    apelidos[apelido] = 1

    print('GLOBAL')
    print('\nNomes Proprios\n')
    for (nome, freq) in list(sorted(nomes_proprios.items(), key=lambda item: item[1], reverse=True)):
        print(f'{nome} -> {freq}')
    print('\nApelidos\n')
    for (nome, freq) in list(sorted(apelidos.items(), key=lambda item: item[1], reverse=True)):
        print(f'{nome} -> {freq}')

    print('\nPOR SECULO')
    for sec in sorted(processos_dict.keys()):
        print(f'\nSeculo {sec}')
        (nome, apelido) = nome_apelido_seculo(sec, processos_dict)
        print(f'Nomes: {", ".join([x[0] for x in nome])}')
        print(f'Apelidos: {", ".join([x[0] for x in apelido])}')


def alinea_c(processos_dict):
    parentes = {'Irmao': 0, 'Tio': 0, 'Primo': 0}
    r = 0
    for (sec, anos_dict) in processos_dict.items():
        for (ano, proc) in anos_dict.items():
            for p in proc:
                tem_parente = False
                if irmaos := re.findall(r'(?i:irmaos?)', p.obs):
                    parentes['Irmao'] += len(irmaos)
                    tem_parente = True
                if tios := re.findall(r'(?i:tio)', p.obs):
                    parentes['Tio'] += len(tios)
                    tem_parente = True
                if primos := re.findall(r'(?i:primo)', p.obs):
                    parentes['Primo'] += len(primos)
                    tem_parente = True
                if tem_parente:
                    r += 1
    print(f'{r} candidatos tem parentes eclesiasticos')
    print(
        f'O grau de parentesco mais comum e {list(sorted(parentes.items(), key=lambda item: item[1], reverse=True))[0][0]}')

    x = list(parentes.keys())
    y = list(parentes.values())
    plt.style.use('seaborn')
    plt.bar(x, y, linestyle='solid', color='green')
    plt.title('Grau de Parentesco Mais Comum')
    plt.xlabel('Grau de Parentesco')
    plt.ylabel('Frequencia')
    plt.tight_layout()
    plt.show()


def alinea_d_pai(pai, processos_dict):
    n = 0
    for (sec, anos_dict) in processos_dict.items():
        for (ano, proc) in anos_dict.items():
            for p in proc:
                if p.pai == pai:
                    n += 1
                    if n > 1:
                        print(f'{pai} tem mais do que um filho candidato')
                        return
    print(f'{pai} nao tem mais do que um filho candidato')


def alinea_d_mae(mae, processos_dict):
    n = 0
    for (sec, anos_dict) in processos_dict.items():
        for (ano, proc) in anos_dict.items():
            for p in proc:
                if p.mae == mae:
                    n += 1
                    if n > 1:
                        print(f'{mae} tem mais do que um filho candidato')
                        return
    print(f'{mae} nao tem mais do que um filho candidato')


def alinea_e(ano, processos_dict):
    seculo = ano // 100 + 1
    f = open('arvore_genealogica.dot', 'w')
    f.write('digraph arvore_genealogica {\n')
    try:
        for p in processos_dict[seculo][ano]:
            if p.mae:
                f.write(f'\t{p.mae.replace(" ", "")} -> {p.nome.replace(" ", "")};\n')
            if p.pai:
                f.write(f'\t{p.pai.replace(" ", "")} -> {p.nome.replace(" ", "")};\n')
        f.write('}\n')
        f.close()
        src = Source.from_file('arvore_genealogica.dot')
        src.view()
    except KeyError:
        print('Nao existe informacao sobre esse ano')

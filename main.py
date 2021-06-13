import re
from os import system, name

from simple_term_menu import TerminalMenu

import solucoes
from processo import *


def clear():
    if name == 'nt':  # for windows
        _ = system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        _ = system('clear')


def remove_duplicates(processos_dict):
    for (sec, anos_dict) in processos_dict.items():
        for (ano, _) in anos_dict.items():
            processos_dict[sec][ano] = list(set(processos_dict[sec][ano]))
    return processos_dict


def parse_xml(lines):
    processos_dict = {}
    processos_XML = re.search(r'<processos>\s*(<processo id[\S\s]*</processo>)\s*</processos>', lines)
    processos = re.findall(r'<processo id[\S\s]*?</processo>', processos_XML.group(1))
    for p in processos:
        id = re.search(r'<processo id="(\d+)">', p).group(1)
        data = re.search(r'<data>(\d{4}-\d{2}-\d{2})</data>', p).group(1)
        nome = re.search(r'<nome>(.*)</nome>', p).group(1)
        pai = re.search(r'<pai>([\w\s]*),?\w*</pai>', p)
        if pai:
            pai = pai.group(1)
        else:
            pai = ''
        mae = re.search(r'<mae>([\w\s]*),?\w*</mae>', p)
        if mae:
            mae = mae.group(1)
        else:
            mae = ''
        obs = re.search(r'<obs>(.*)</obs>', p)
        if obs:
            obs = obs.group(1)
        else:
            obs = ''

        ano = int(data[:4])
        seculo = ano // 100 + 1

        if seculo not in processos_dict.keys():
            processos_dict[seculo] = {}

        try:
            processos_dict[seculo][ano].append(Processo(id, data, nome, pai, mae, obs))
        except KeyError:
            processos_dict[seculo][ano] = []
            processos_dict[seculo][ano].append(Processo(id, data, nome, pai, mae, obs))

    return remove_duplicates(processos_dict)


def main():
    with open('processos.xml', 'r', encoding='utf8') as f:
        processos_dict = parse_xml(f.read())

    main_menu_items = ['[1] Numero de processos por ano',
                       '[2] Frequencia de nomes proprios e apelidos',
                       '[3] Numero de candidatos com parentes eclesiasticos',
                       '[4] Pai com mais do que um filho candidato',
                       '[5] Mae com mais do que um filho candidato',
                       '[6] Arvores genealogicas de um certo ano',
                       '[7] Sair']
    main_menu_exit = False
    terminal_menu = TerminalMenu(main_menu_items)

    clear()

    while not main_menu_exit:
        main_sel = terminal_menu.show()
        if main_sel == 0:
            solucoes.alinea_a(processos_dict)
            inp = input('Enter para continuar')
            clear()
        elif main_sel == 1:
            solucoes.alinea_b(processos_dict)
            inp = input('Enter para continuar')
            clear()
        elif main_sel == 2:
            solucoes.alinea_c(processos_dict)
            inp = input('Enter para continuar')
            clear()
        elif main_sel == 3:
            pai = input('Pai: ')
            pai = re.sub(r'\s+', ' ', pai.title().strip())
            solucoes.alinea_d_pai(pai, processos_dict)
            inp = input('Enter para continuar')
            clear()
        elif main_sel == 4:
            mae = input('Mae: ')
            mae = re.sub(r'\s+', ' ', mae.title().strip())
            solucoes.alinea_d_mae(mae, processos_dict)
            inp = input('Enter para continuar')
            clear()
        elif main_sel == 5:
            ok = False
            while not ok:
                try:
                    ano = int(input('Ano: '))
                    ok = True
                except ValueError:
                    print('Valor Invalido')
            solucoes.alinea_e(ano, processos_dict)
            inp = input('Enter para continuar')
            clear()
        elif main_sel == 6:
            main_menu_exit = True


if __name__ == '__main__':
    main()

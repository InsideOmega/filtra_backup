import datetime
import re

def carregar_clientes_do_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        clientes = arquivo.readlines()
    return clientes

def extrair_nome_cliente(linha):
    match = re.search(r'Service(\w+)/Service\1_backup', linha, re.IGNORECASE)
    if match:
        nome_cliente = match.group(1).strip()
        return nome_cliente
    return None

def manter_linhas_com_texto(nome_arquivo, nome_arquivo_clientes):
    linhas_filtradas = []
    data_atual = datetime.datetime.now()
    dia_atual = data_atual.strftime('%Y_%m_%d')
    dia_anterior = (data_atual - datetime.timedelta(days=1)).strftime('%Y_%m_%d')

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if '.FULL_bak' in linha and (dia_atual in linha or dia_anterior in linha):
                linhas_filtradas.append(linha)

    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas_filtradas)

    clientes = carregar_clientes_do_arquivo(nome_arquivo_clientes)
    clientes_no_resultado = set()

    for linha in linhas_filtradas:
        nome_cliente = extrair_nome_cliente(linha)

        if nome_cliente and any(nome_cliente.lower() in cliente.strip().lower() for cliente in clientes):
            clientes_no_resultado.add(nome_cliente.lower())

    clientes_faltantes = set(cliente.strip().lower() for cliente in clientes) - clientes_no_resultado

    print("Arquivo ajustado com sucesso!")

    if clientes_faltantes:
        print("Clientes não presentes no resultado:")
        for cliente in clientes_faltantes:
            print(cliente.strip())
    else:
        print("Todos os clientes encontrados!")
    input("Processo finalizado! Aperte 'Enter' para sair!")

manter_linhas_com_texto('c:/RelatórioBackup.txt', 'c:/Clientes.txt')

import os
from datetime import datetime

def salvandoLog(mensagem):
    # Obtendo a data e hora atual
    agora = datetime.now()
    ano_atual = agora.year
    mes_atual = agora.month
    dia_atual = agora.day
    data_formatada = agora.strftime("%Y-%m-%d_%H-%M-%S")  # Nome do arquivo formatado sem caracteres inválidos

    # mes
    mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    # Caminho completo onde o arquivo será salvo
    caminho = f"C:\\AvisoRede\\{ano_atual}\\{mes[mes_atual]}\\{dia_atual}"
    nome_arquivo = f"{data_formatada}.txt"

    # Verifica se o caminho existe e, se não, cria as pastas necessárias
    os.makedirs(caminho, exist_ok=True)

    # Caminho completo do arquivo
    caminho_completo = os.path.join(caminho, nome_arquivo)

    # Escrevendo a mensagem no arquivo
    with open(caminho_completo, "w") as arquivo:
        arquivo.write(f"{mensagem}")

    print(f"Arquivo criado com sucesso em: {caminho_completo}")


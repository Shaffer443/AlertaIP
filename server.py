from flask import Flask, request, jsonify
from win10toast import ToastNotifier
from datetime import datetime, date
from waitress import serve
import logging
import os
import pytz

app = Flask(__name__)

# Inicializando notificações
toaster = ToastNotifier()

# Definir o fuso horário de Recife
fuso_recife = pytz.timezone("America/Recife")


def get_data_hora_atual():
    """Retorna a data e hora atual formatada para Recife"""
    agora = datetime.now(fuso_recife)
    return agora.strftime("%d/%m/%Y - %H:%M:%S")


def get_pastas_log():
    """Retorna os diretórios organizados por Ano/Mês/Dia"""
    dadosData = date.today()
    nomeMes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    pastaAno = str(dadosData.year)
    pastaMes = nomeMes[dadosData.month - 1]
    pastaDia = str(dadosData.day)

    caminho_base = r"C:\LogAvisoRede"
    log_directory = os.path.join(caminho_base, pastaAno, pastaMes, pastaDia)
    os.makedirs(log_directory, exist_ok=True)  # Cria os diretórios se não existirem

    return os.path.join(log_directory, "notificacoes.log")


# Caminho do arquivo de log
log_file_path = get_pastas_log()

# Configuração do logger
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info("Servidor Flask iniciado com sucesso!")


@app.route('/notificar', methods=['POST'])
def notificar():
    """Recebe mensagens via POST e exibe notificação"""
    data = request.get_json()
    mensagem = data.get("mensagem", "")
    horario = get_data_hora_atual()

    if not mensagem:
        return jsonify({"status": "erro", "mensagem": "Nenhuma mensagem recebida"}), 400

    print(f"Mensagem recebida: {mensagem} - {horario}")
    logging.info(f"Mensagem recebida: {mensagem} - {horario}")

    # Enviar notificação no Windows
    toaster.show_toast(f"Monitoramento de Rede {horario}", mensagem, duration=20)

    return jsonify({"status": "sucesso", "mensagem_recebida": mensagem, "horario": horario}), 200


@app.route("/")
def home():
    """Verifica se o servidor está ativo"""
    horario = get_data_hora_atual()
    return f"Servidor Flask para notificações de falha na rede está ativo! {horario}", 200


if __name__ == '__main__':
    print("\n🔥 Servidor Flask rodando! Acesse via http://127.0.0.1:5000 ou pelo IP da rede.")
    print("📌 Aguarde notificações... O log está sendo salvo em:", log_file_path)
    print("🔄 Pressione CTRL+C para parar o servidor.\n")
    # Utilizando Waitress para rodar o Flask de forma mais estável
    serve(app, host="0.0.0.0", port=5000)

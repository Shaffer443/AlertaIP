from flask import Flask, request, jsonify
from win10toast import ToastNotifier
from datetime import datetime
import logging
import os

app = Flask(__name__)

#-----------------
#    Inicializando notificações
toaster = ToastNotifier()

# Obtém a data e o horário atual
agora = datetime.now()

# Formata a data e o horário no formato desejado
formato = agora.strftime("%d/%m/%Y - %H:%M:%S")
#------

# Diretório onde o log será salvo
log_directory = r"C:\LogAvisoRede"
os.makedirs(log_directory, exist_ok=True)  # Cria o diretório se não existir

# Caminho completo do arquivo de log
log_file_path = os.path.join(log_directory, "notificacoes.log")

# Configuração do logger
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Exemplo de log
logging.info("Arquivo de log configurado com sucesso!")

#logging.basicConfig(
#    filename='notificacoes.log',
#    level=logging.INFO,
#    format='%(asctime)s - %(message)s'
#)

@app.route('/notificar', methods=['POST'])
def notificar():
    data = request.get_json()
    mensagem = data.get("mensagem", "")
    print(f"Mensagem recebida: {mensagem} - {formato}")
    # Enviar notificação no Windows
    logging.info(f"Mensagem recebida: {mensagem} - {formato}")
    toaster.show_toast(f"Monitoramento de Rede {formato}", mensagem, duration=20)
    return jsonify({"status": "sucesso", f"mensagem_recebida - {formato}": mensagem}), 200

@app.route("/")
def home():
    return f"Servidor Flask para notificações de falha na rede está ativo! {formato}", 200


#logging.basicConfig(
#    filename='app.log',
#    level=logging.INFO,
#    format='%(asctime)s - %(message)s'
#)
#logging.info('Aplicação iniciada com sucesso.')
# Coloque logs adicionais ao longo do código.


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo

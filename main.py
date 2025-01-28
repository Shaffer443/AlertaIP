from flask import Flask, request, jsonify
from win10toast import ToastNotifier
#import logging

app = Flask(__name__)

#    Inicializando notificações
toaster = ToastNotifier()

import logging

logging.basicConfig(
    filename='notificacoes.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/notificar', methods=['POST'])
def notificar():
    data = request.get_json()
    mensagem = data.get("mensagem", "")
    print(f"Mensagem recebida: {mensagem}")
    # Enviar notificação no Windows
    logging.info(f"Mensagem recebida: {mensagem}")
    toaster.show_toast("Monitoramento de Rede", mensagem, duration=20)
    return jsonify({"status": "sucesso", "mensagem_recebida": mensagem}), 200

@app.route("/")
def home():
    return "Servidor Flask para notificações de falha na rede está ativo!", 200


#logging.basicConfig(
#    filename='app.log',
#    level=logging.INFO,
#    format='%(asctime)s - %(message)s'
#)
#logging.info('Aplicação iniciada com sucesso.')
# Coloque logs adicionais ao longo do código.


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo

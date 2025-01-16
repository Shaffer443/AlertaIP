from flask import Flask, request, jsonify
from win10toast import ToastNotifier

app = Flask(__name__)

# Inicializando notificações
toaster = ToastNotifier()

@app.route('/notificar', methods=['POST'])
def notificar():
    data = request.get_json()
    mensagem = data.get("mensagem", "")
    print(f"Mensagem recebida: {mensagem}")
    # Enviar notificação no Windows
    toaster.show_toast("Monitoramento de Rede", mensagem, duration=20)
    return jsonify({"status": "sucesso", "mensagem_recebida": mensagem}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo

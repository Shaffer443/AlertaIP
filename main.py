import time
from ping3 import ping
from win10toast import ToastNotifier

# Lista de IPs para monitorar
ips = ["10.4.0.1", "8.8.8.8", "10.4.0.40", "10.4.0.7", "10.4.0.6", "10.4.0.8"]

# Inicializando notificações
toaster = ToastNotifier()

def verificar_conectividade():
    for ip in ips:
        resultado = ping(ip, timeout=2)  # Timeout de 2 segundos
        if resultado is None:
            mensagem = f"Atenção! O IP {ip} está inacessível."
            print(mensagem)
            # Enviar notificação no Windows
            toaster.show_toast("Monitoramento de Rede", mensagem, duration=10)

# Loop de monitoramento
try:
    while True:
        print("Verificando conectividade...")
        verificar_conectividade()
        print("Aguardando 2 minutos...")
        time.sleep(120)  # Aguarda 2 minutos
except KeyboardInterrupt:
    print("Monitoramento encerrado.")

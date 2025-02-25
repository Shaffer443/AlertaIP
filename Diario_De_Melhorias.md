# 25/02/2025

Seu script Flask no Windows já está bem estruturado para receber notificações do Linux e exibir alertas no sistema. No entanto, há alguns pontos que podem ser melhorados:  

1. **Correção no horário da notificação** (ele está sendo fixado na inicialização do script).  
2. **Uso do Waitress** para um servidor mais estável.  
3. **Evitar variáveis globais desnecessárias** para data e hora.  

---

### **🔧 Melhorias no Código**
Aqui está o código atualizado com as melhorias mencionadas:

```python
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
    # Utilizando Waitress para rodar o Flask de forma mais estável
    serve(app, host="0.0.0.0", port=5000)
```

---

### **🛠️ O que foi melhorado?**
1. **Data e Hora são atualizadas dinamicamente**  
   - Antes: A variável `formato` era definida apenas na inicialização do script, mantendo o mesmo horário.  
   - Agora: Cada notificação recebe a **hora exata** no momento do evento.  

2. **Organização das pastas de log**  
   - Criada a função `get_pastas_log()` para gerar dinamicamente os diretórios `Ano/Mês/Dia`.  
   - Isso evita código repetitivo e melhora a organização.  

3. **Servidor mais estável com Waitress**  
   - **Antes:** `app.run(...)` (servidor de desenvolvimento).  
   - **Agora:** `serve(app, host="0.0.0.0", port=5000)` (Waitress, recomendado para produção no Windows).  

---

### **🚀 Como Executar?**
Após salvar o arquivo como `main.py`, rode:  

```bash
python main.py
```

Ou, se quiser transformar em um **executável**:  

```bash
pyinstaller --onefile main.py
```

Isso gerará um `.exe` na pasta `dist/`, pronto para ser usado.  

---

### **✅ Como Testar do Linux?**
No seu **servidor Linux**, envie notificações com `curl` ou Python:

```bash
curl -X POST http://192.168.1.100:5000/notificar -H "Content-Type: application/json" -d '{"mensagem": "Falha na rede detectada!"}'
```

📌 Substitua `192.168.1.100` pelo IP do seu Windows.

Agora seu sistema está pronto para monitorar notificações de rede e exibi-las no Windows com mais confiabilidade! 🚀

---
Sim! Você pode exibir uma mensagem no **cmd** quando o servidor Flask iniciar. Para isso, basta adicionar um `print()` no final do script.  

---

### **🛠️ Como Fazer?**  
Adicione esta linha logo antes de `serve(app, host="0.0.0.0", port=5000)`:

```python
print("🔥 Servidor Flask rodando! Acesse via http://127.0.0.1:5000 ou pelo IP da rede.")
```

---

### **🔄 Código Atualizado:**
```python
if __name__ == '__main__':
    print("\n🔥 Servidor Flask rodando! Acesse via http://127.0.0.1:5000 ou pelo IP da rede.")
    print("📌 Aguarde notificações... O log está sendo salvo em:", log_file_path)
    print("🔄 Pressione CTRL+C para parar o servidor.\n")
    
    # Utilizando Waitress para rodar o Flask de forma mais estável
    serve(app, host="0.0.0.0", port=5000)
```

---

### **📌 O que acontece agora?**  
Quando você rodar `python main.py`, verá algo assim no terminal:  

```
🔥 Servidor Flask rodando! Acesse via http://127.0.0.1:5000 ou pelo IP da rede.
📌 Aguarde notificações... O log está sendo salvo em: C:\LogAvisoRede\2025\Fevereiro\25\notificacoes.log
🔄 Pressione CTRL+C para parar o servidor.
```

Agora você tem uma **confirmação visual** de que o servidor está ativo no Windows! 🚀
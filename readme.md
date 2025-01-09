Sim, é possível criar um script em Python para monitorar os IPs e gerar notificações no Windows 11. Aqui está um exemplo funcional que verifica os IPs mencionados a cada 2 minutos. Ele utiliza o módulo `ping3` para verificar a conectividade e a biblioteca `win10toast` para enviar notificações no Windows.

### Instalação de Dependências
Antes de usar o script, instale as bibliotecas necessárias:
```bash
pip install ping3 win10toast
```

### Código do Script
```python
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
```

### Funcionamento
1. **Monitoramento**: O script verifica a conectividade dos IPs listados enviando pings.
2. **Notificações**: Quando um IP não responde, uma notificação do Windows 11 é exibida.
3. **Intervalo**: A verificação é realizada a cada 2 minutos (configurado com `time.sleep(120)`).
4. **Encerramento**: O script pode ser interrompido pressionando `Ctrl+C`.

### Personalizações
- **Timeout do ping**: Ajuste o valor de `timeout` na função `ping` para alterar o tempo limite de resposta.
- **Duração da notificação**: Modifique o parâmetro `duration` na função `toaster.show_toast` para alterar o tempo de exibição da notificação.

No Windows 11, as notificações exibidas pelo `win10toast` ficam visíveis por um tempo configurado pelo parâmetro `duration` (em segundos). No script fornecido, a duração está definida como `10` segundos:

```python
toaster.show_toast("Monitoramento de Rede", mensagem, duration=10)
```

Isso significa que a notificação será exibida por **10 segundos** e desaparecerá automaticamente após esse período.

Se desejar alterar esse tempo:
- **Aumente ou diminua o valor de `duration`** conforme necessário.
- Exemplo para 20 segundos:
  ```python
  toaster.show_toast("Monitoramento de Rede", mensagem, duration=20)
  ```

### Nota
Se o usuário interagir com a notificação (clicar ou fechá-la manualmente), ela desaparecerá antes do tempo configurado.

--------------------
Para criar um executável que você possa clicar e deixar rodando no Windows 11, você pode usar a biblioteca `pyinstaller`. Com isso, o script Python será convertido em um arquivo `.exe`. Aqui estão as etapas para fazer isso:

---

### 1. **Instalar o PyInstaller**
Abra o terminal ou prompt de comando e execute:
```bash
pip install pyinstaller
```

---

### 2. **Gerar o Executável**
No diretório onde o script está salvo (exemplo: `monitor_rede.py`), execute o seguinte comando:

```bash
pyinstaller --onefile --noconsole monitor_rede.py
```

- `--onefile`: Cria um único arquivo `.exe`.
- `--noconsole`: Remove a janela do console, ideal para scripts com notificações que não precisam de saída no terminal.

Isso criará uma pasta chamada `dist` contendo o arquivo executável `monitor_rede.exe`.

---

### 3. **Mover o Executável**
- Localize o arquivo gerado em `dist/monitor_rede.exe`.
- Mova-o para uma pasta de sua escolha (como a área de trabalho).

---

### 4. **Rodar o Programa**
- Clique duas vezes no arquivo `.exe` para iniciar o monitoramento.
- Ele rodará em segundo plano, e você receberá notificações no desktop conforme configurado.

---

### 5. **Rodar Automaticamente na Inicialização do Windows (Opcional)**
Para iniciar automaticamente quando o computador ligar:
1. Pressione `Win + R`, digite `shell:startup` e pressione Enter.
2. Cole o arquivo `.exe` gerado na pasta que abrir.

Agora, o programa será executado automaticamente sempre que o Windows inicializar.

---

Se o executável gerado pelo PyInstaller não estiver funcionando ao ser clicado, isso pode ocorrer por alguns motivos. Vamos resolver passo a passo:

---

### **1. Testar no Terminal**
Antes de tudo, verifique se há algum erro executando o `.exe` pelo terminal:
1. Abra o Prompt de Comando (pressione `Win + R`, digite `cmd` e pressione Enter).
2. Navegue até o diretório onde o `.exe` foi gerado usando o comando `cd`:
   ```cmd
   cd caminho\para\a\pasta\dist
   ```
3. Execute o arquivo `.exe` no terminal:
   ```cmd
   monitor_rede.exe
   ```

Se houver algum problema, o terminal exibirá mensagens de erro. Compartilhe essa mensagem se precisar de ajuda para resolvê-la.

---

### **2. Verificar Dependências**
Certifique-se de que as bibliotecas usadas no script (`ping3` e `win10toast`) estão sendo corretamente incluídas. Recompile o script com PyInstaller usando o comando abaixo para garantir isso:

```bash
pyinstaller --onefile --hidden-import ping3 --hidden-import win10toast monitor_rede.py
```

---

### **3. Rodar com Console (Modo Debug)**
Ao compilar, remova o parâmetro `--noconsole` para manter a janela do console aberta. Isso permite ver mensagens ou erros enquanto o programa está rodando:
```bash
pyinstaller --onefile monitor_rede.py
```

Após gerar o `.exe`, execute-o novamente e observe o comportamento.

---

### **4. Dependências do Windows**
O PyInstaller embute o Python no executável, mas, em alguns casos, bibliotecas do sistema operacional podem estar ausentes. Certifique-se de que você tem:
- Microsoft Visual C++ Redistributable (versão mais recente).

Você pode baixar no site oficial da Microsoft, caso necessário.

---

### **5. Configuração do Script**
Se você usou `--noconsole` e o script não exibe nenhuma janela ou notificação, talvez ele esteja rodando corretamente, mas as notificações não estão visíveis. Certifique-se de:
- Testar o script diretamente como `.py` antes de compilar para confirmar que ele está funcionando.
- Alterar o tempo de verificação para algo menor (exemplo: 10 segundos) para ver rapidamente se as notificações aparecem.

---

### **6. Tentar Outro Método de Notificação**
Se o problema for com a biblioteca `win10toast`, tente usar `plyer`, que também envia notificações no Windows:
```bash
pip install plyer
```

Modifique o trecho de notificação no script:
```python
from plyer import notification

# Notificação usando plyer
notification.notify(
    title="Monitoramento de Rede",
    message=mensagem,
    timeout=10  # Duração em segundos
)
```

Recompile com PyInstaller e teste novamente.

---

Se persistir o problema, compartilhe o que aparece ao rodar o `.exe` no terminal. Com isso, posso ajudar a identificar a causa e corrigir! 😊
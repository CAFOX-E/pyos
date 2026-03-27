import os
import datetime
import sys
import shutil
import stat
import subprocess
import json
import time
import csv
import math
import re
import google.generativeai as genai
import http.server
import socketserver
import socket
import base64
import hashlib
from cryptography.fernet import Fernet
import psutil
import random
import urllib.request
import unicodedata

def limpar_tela():
    # Limpa a tela dependendo do sistema operacional real do usuário
    os.system('cls' if os.name == 'nt' else 'clear')

def iniciar_pyos():
    os.system('')
    limpar_tela()
    
    # --- NOVO SISTEMA DE LOGIN COM PALAVRA-PASSE E BASE DE DADOS ---
    arquivo_db = "usuarios_db.json"
    
    # 1. Carrega a base de dados se ela existir, senão cria uma lista (dicionário) vazia
    if os.path.exists(arquivo_db):
        with open(arquivo_db, 'r', encoding='utf-8') as f:
            banco_usuarios = json.load(f)
    else:
        banco_usuarios = {}

    print("A iniciar o PyOS...")
    usuario = ""
    while not usuario:
        usuario = input("Login (Digite o seu nome de utilizador): ").strip()
        
    # 2. Verifica se o utilizador já existe na nossa base de dados
    if usuario in banco_usuarios:
        senha_correta = banco_usuarios[usuario]
        senha_digitada = ""
        
        # Fica em loop até o utilizador acertar a palavra-passe
        while senha_digitada != senha_correta:
            senha_digitada = input("Palavra-passe: ")
            if senha_digitada != senha_correta:
                print("Palavra-passe incorreta. Tente novamente.")
    else:
        # 3. Se não existir, cria uma conta nova e guarda no ficheiro JSON
        print(f"\nUtilizador '{usuario}' não encontrado. A criar uma nova conta...")
        nova_senha = input("Crie uma palavra-passe para o seu utilizador: ")
        banco_usuarios[usuario] = nova_senha
        
        # Guarda a atualização no ficheiro
        with open(arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(banco_usuarios, f, indent=4)
        print("Conta criada com sucesso! A entrar no sistema...")
    # ---------------------------------------------------------------

    # --- NOVO: CARREGAR CONFIGURAÇÕES DE COR DO USUÁRIO ---
    arquivo_config = "config_db.json"
    if os.path.exists(arquivo_config):
        with open(arquivo_config, 'r', encoding='utf-8') as f:
            banco_cores = json.load(f)
    else:
        banco_cores = {}

    # Dicionário de cores para o carregamento inicial
    cores_iniciais = {
        "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
        "blue": "\033[34m", "purple": "\033[35m", "cyan": "\033[36m",
        "white": "\033[37m", "default": "\033[0m"
    }
    
    # Pega a cor salva do usuário (ou usa 'restaurar' se for a primeira vez)
    cor_salva = banco_cores.get(usuario, "default")
    print(cores_iniciais[cor_salva], end="")
    # ------------------------------------------------------

    limpar_tela()
    print("=================================================")
    print(f" Bem-vindo ao PyOS, {usuario}! ")
    print(" Digite 'help' para ver os comandos disponíveis.")
    print("=================================================")

    while True:
        # Prompt de comando do nosso sistema
        entrada = input(f"\n{usuario}@PyOS> ").strip()
        
        if not entrada:
            continue
            
        # Separa o comando dos argumentos (ex: 'eco ola' -> comando='eco', arg='ola')
        partes = entrada.split(" ", 1)
        comando = partes[0].lower()
        argumento = partes[1] if len(partes) > 1 else ""

        # Lógica dos comandos
        if comando == "quit":
            print("Desligando o PyOS... Até logo!")
            sys.exit()
            
        elif comando == "help":
            print("\n--- Comandos de Ajuda ---")
            print("  help-basics    : Exibe os comandos básicos do programa")
            print("  help-archives  : Exibe os comandos de exploração de arquivos")
            print("  help-office    : Exibe os comandos de criação e edição de arquivos de textos e planilhas")
            print("  help-config    : Exibe os comandos de configurações de usuários e outros")
            print("  quit           : Desliga o sistema")

        elif comando == "help-basics":
            print("\n--- Comandos Disponíveis ---")
            print("  help           : Mostra esta lista de comandos de ajuda")
            print("  logout         : Encerra a sessão atual e volta para a tela de login")
            print("  date           : Exibe a data e hora atuais")
            print("  ping           : Testa a conexão de rede com um site ou IP (ex: ping google.com)")
            print("  clear          : Limpa a tela do terminal")
            print("  list           : Lista os arquivos na pasta atual")
            print("  print          : Repete o que você digitar (ex: print Hello World!)")
            print("  calc           : Uma calculadora simples (ex: calc 5 + 5)")
            print("  play           : Abre o menu de mini-jogos do PyOS para relaxar")
            print("  ai             : Inicia uma conversa com a Inteligência Artificial (ex: ai)")
            print("  server         : Inicia o compartilhamento (ex: server web OU server ftp)")

        elif comando == "help-archives":
            print("\n--- Comandos Disponíveis ---")
            print("  cd             : Navega entre as pastas (ex: cd nome_da_pasta ou cd .. para voltar)")
            print("  search         : Busca arquivos e pastas pelo nome (ex: search projeto)")
            print("  mkdir          : Cria uma nova pasta (ex: mkdir nova_pasta)")
            print("  rmdir          : Deleta uma pasta (ex: rmdir pasta_antiga)")
            print("  open           : Executa um arquivo com o programa padrão do seu computador (ex: open foto.jpg)")
            print("  delete         : Deleta um arquivo específico (ex: delete texto.txt)")
            print("  empty          : Apaga TODOS os arquivos de uma pasta de uma vez (ex: empty minha_pasta)")
            print("  lock           : Criptografa um arquivo com senha (ex: lock segredo.txt)")
            print("  unlock         : Descriptografa um arquivo bloqueado (ex: unlock segredo.txt.lock)")
            
        elif comando == "help-office":
            print("  txt_read       : Exibe o texto de um arquivo no terminal (ex: read notas.txt)")
            print("  txt_write      : Cria/edita um arquivo de texto (ex: write notas.txt)")
            print("  txt_edit       : Edita um arquivo de texto já existente (ex: edit notas.txt)")
            print("  csv_write      : Cria uma nova planilha (ex: planilha_criar dados.csv)")
            print("  csv_add        : Adiciona uma linha de dados à planilha (ex: planilha_add dados.csv)")
            print("  csv_read       : Lê e exibe uma planilha em formato de tabela (ex: planilha_ler dados.csv)")

        elif comando == "help-config":
            print("\n--- Comandos Disponíveis ---")
            print("  disk           : Analisa o espaço de armazenamento do disco atual")
            print("  status         : Mostra o uso de CPU, RAM e Bateria em tempo real")
            print("  devices        : Lista os adaptadores de rede e dispositivos USB conectados")
            print("  adduser        : Adiciona um novo usuário ao sistema (ex: adduser maria)")
            print("  dltuser        : Deleta um usuário do sistema (ex: dltuser joao)")
            print("  color          : Muda a cor do terminal (ex: color green, color default)")
            
# Comando logout
        elif comando == "logout":
            print(f"\nEncerrando a sessão de '{usuario}'...")
            
            # Restaura a cor para o padrão (branco/cinza) antes de voltar para a tela inicial
            print("\033[0m", end="")
            
            # Aguarda 1 segundinho para dar uma sensação mais realista de sistema fechando
            import time
            time.sleep(1)
            
            # Chama a função principal de novo, reiniciando o ciclo de login!
            return iniciar_pyos()

# Comando date
        elif comando == "date":
            agora = datetime.datetime.now()
            print(f"Data e hora do sistema: {agora.strftime('%d/%m/%Y %H:%M:%S')}")

# Comando ping
        elif comando == "ping":
            if argumento:
                print(f"\nDisparando pulsos de rede para '{argumento}'...")
                print("Aguarde a resposta do servidor...\n")
                
                try:
                    # O Windows usa '-n' para definir o número de pacotes. Mac/Linux usam '-c'.
                    # Vamos configurar para enviar 4 pacotes (para não ficar rodando para sempre no Linux/Mac)
                    parametro = '-n' if sys.platform == 'win32' else '-c'
                    
                    # Monta o comando exato que o sistema real precisa
                    comando_ping = ['ping', parametro, '4', argumento]
                    
                    # Executa o comando e mostra o resultado direto na tela do PyOS
                    subprocess.call(comando_ping)
                    
                    print("\nTeste de conexão finalizado.")
                except Exception as e:
                    print(f"Erro ao tentar acessar a rede: {e}")
            else:
                print("Por favor, digite o endereço de um site ou IP. Exemplo: ping google.com")
            
# Comando clear
        elif comando == "clear":
            limpar_tela()
# Comando list
        elif comando == "list":
            print(f"\nConteúdo do diretório atual ({os.getcwd()}):")
            try:
                # Pega todos os itens (pastas e arquivos)
                itens = os.listdir('.')
                
                # Primeiro, mostramos as pastas
                for item in itens:
                    if os.path.isdir(item):
                        print(f" [PASTA]   {item}")
                        
                # Depois, mostramos os arquivos
                for item in itens:
                    if os.path.isfile(item):
                        print(f" [ARQUIVO] {item}")
                        
                if not itens:
                    print(" (A pasta está vazia)")
                    
            except Exception as e:
                print(f"Erro ao ler diretório: {e}")
                
# Comando print
        elif comando == "print":
            print(argumento)
# Comando calc
        elif comando == "calc":
            # Criamos um "dicionário seguro" com as funções matemáticas permitidas.
            # Isso deixa o eval() muito mais seguro e poderoso!
            funcoes_matematicas = {
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, 
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e, "abs": abs
            }
            
            def resolver_conta(expressao):
                try:
                    # 1. Transforma a palavra "de" em multiplicação (Ex: 50% de 100 vira 50% * 100)
                    expressao_ajustada = expressao.replace(' de ', ' * ')
                    
                    # 2. Transforma o número com % em divisão (Ex: 50% vira (50/100))
                    # O 're.sub' procura números seguidos de % e faz a troca matematicamente correta
                    expressao_ajustada = re.sub(r'([0-9.]+)%', r'(\1/100)', expressao_ajustada)
                    
                    resultado = eval(expressao_ajustada, {"__builtins__": None}, funcoes_matematicas)
                    return resultado
                except ZeroDivisionError:
                    return "Erro: Divisão por zero não é permitida."
                except Exception:
                    return "Erro de sintaxe. Verifique a expressão digitada."

            # Se o usuário digitou a conta direto na linha (ex: calc 10 * 2)
            if argumento:
                print(f"Resultado: {resolver_conta(argumento)}")
                
            # Se o usuário digitou apenas 'calc', abrimos o Modo Interativo
            else:
                print("\n--- Calculadora Científica PyOS ---")
                print("Operadores básicos: + (soma), - (subtração), * (multiplicação), / (divisão), ** (potência)")
                print("Funções avançadas: sqrt(x), sin(x), cos(x), log(x), pi, e")
                print("DICA: Digite ':q' ou 'sair' para voltar ao sistema.")
                print("-" * 35)
                
                while True:
                    conta = input("calc> ").strip().lower()
                    
                    if conta in [':q', 'sair']:
                        print("Fechando calculadora...")
                        break
                    if not conta:
                        continue
                        
                    resultado = resolver_conta(conta)
                    print(f" = {resultado}")

# Comando play
        elif comando == "play":
            while True:
                print("\n=== 🕹️ Salão de Jogos PyOS ===")
                print("1. Adivinha o Número")
                print("2. Pedra, Papel e Tesoura")
                print("3. Jogo da Forca")
                print("0. Sair dos jogos")
                print("================================")
                
                escolha = input("Escolha um jogo (0, 1, 2 ou 3): ").strip()
                
                if escolha == '0':
                    print("A sair do Salão de Jogos. De volta ao trabalho!")
                    
                    # --- NOVO: LIMPEZA DE ARQUIVOS TEMPORÁRIOS ---
                    arquivo_dicionario = "dicionario_br.txt"
                    if os.path.exists(arquivo_dicionario):
                        try:
                            os.remove(arquivo_dicionario)
                            print("[Sistema] Dicionário temporário apagado. Pasta limpa!")
                        except Exception as e:
                            pass
                    # ---------------------------------------------
                    break
                    
                elif escolha == '1':
                    print("\n--- Adivinha o Número ---")
                    numero_secreto = random.randint(1, 100)
                    tentativas = 0
                    print("O PyOS pensou num número entre 1 e 100. Tenta adivinhar!")
                    
                    while True:
                        palpite = input("O teu palpite (ou ':q' para sair): ").strip()
                        if palpite.lower() == ':q': break
                        if not palpite.isdigit(): continue
                            
                        palpite = int(palpite)
                        tentativas += 1
                        
                        if palpite < numero_secreto: print("🔺 Mais alto!")
                        elif palpite > numero_secreto: print("🔻 Mais baixo!")
                        else:
                            print(f"🎉 Parabéns! Acertaste em cheio no {numero_secreto} com {tentativas} tentativa(s)!")
                            break
                            
                elif escolha == '2':
                    print("\n--- Pedra, Papel e Tesoura ---")
                    opcoes = ["pedra", "papel", "tesoura"]
                    
                    while True:
                        jogada = input("Escolhe: pedra, papel, tesoura (ou ':q' para sair): ").strip().lower()
                        if jogada == ':q': break
                        if jogada not in opcoes: continue
                            
                        pc_jogada = random.choice(opcoes)
                        print(f"💻 O computador escolheu: {pc_jogada.upper()}")
                        
                        if jogada == pc_jogada: print("🤝 Empate!")
                        elif (jogada == 'pedra' and pc_jogada == 'tesoura') or \
                             (jogada == 'papel' and pc_jogada == 'pedra') or \
                             (jogada == 'tesoura' and pc_jogada == 'papel'):
                            print("🏆 Ganhaste esta ronda!")
                        else: print("💀 Perdeste! O computador foi mais esperto.")
                        
                # --- NOVO: JOGO DA FORCA (PALAVRAS COM 5+ LETRAS) ---
                elif escolha == '3':
                    print("\n--- Jogo da Forca ---")
                    
                    arquivo_dicionario = "dicionario_br.txt"
                    # Lista de emergência atualizada apenas com palavras maiores
                    palavras = ["python", "computador", "teclado", "internet", "criptografia"] 
                    
                    # 1. Verifica se o dicionário já foi descarregado
                    if not os.path.exists(arquivo_dicionario):
                        print("A descarregar o dicionário completo de Português (aguarde uns segundos)...")
                        try:
                            url = "https://raw.githubusercontent.com/pythonprobr/palavras/master/palavras.txt"
                            urllib.request.urlretrieve(url, arquivo_dicionario)
                            print("Dicionário descarregado com sucesso!")
                        except Exception as e:
                            print(f"Erro ao descarregar: {e}. A usar lista de emergência.")
                    
                    # 2. Lê as palavras do ficheiro
                    try:
                        if os.path.exists(arquivo_dicionario):
                            with open(arquivo_dicionario, 'r', encoding='utf-8') as f:
                                # AQUI ESTÁ A MUDANÇA: Filtra para usar APENAS palavras com 5 ou mais letras!
                                palavras = [p.strip() for p in f.readlines() if len(p.strip()) >= 5]
                    except Exception:
                        pass
                        
                    # 3. Sorteia a palavra
                    palavra_original = random.choice(palavras).lower()
                    
                    # 4. Remove os acentos (ex: "computação" vira "computacao")
                    palavra_secreta = "".join(c for c in unicodedata.normalize('NFD', palavra_original) if unicodedata.category(c) != 'Mn')
                    
                    letras_descobertas = []
                    erros_permitidos = 6
                    
                    print(f"DICA: A palavra tem {len(palavra_secreta)} letras!")
                    
                    while True:
                        palavra_oculta = ""
                        for letra in palavra_secreta:
                            if letra in letras_descobertas:
                                palavra_oculta += letra + " "
                            else:
                                palavra_oculta += "_ "
                                
                        print(f"\nPalavra: {palavra_oculta}")
                        print(f"Tentativas restantes: {erros_permitidos}")
                        
                        if "_" not in palavra_oculta:
                            print(f"🎉 Parabéns! Escapaste da forca! A palavra era {palavra_original.upper()}.")
                            break
                            
                        if erros_permitidos == 0:
                            print(f"💀 Fim de jogo! Foste enforcado. A palavra era: {palavra_original.upper()}")
                            break
                            
                        letra_digitada = input("Digita uma letra (ou ':q' para sair): ").strip().lower()
                        
                        if letra_digitada == ':q': break
                        if len(letra_digitada) != 1 or not letra_digitada.isalpha():
                            print("Por favor, digita apenas uma letra válida.")
                            continue
                            
                        # Remove o acento também da letra digitada
                        letra_digitada = "".join(c for c in unicodedata.normalize('NFD', letra_digitada) if unicodedata.category(c) != 'Mn')
                            
                        if letra_digitada in letras_descobertas:
                            print("Já tentaste essa letra! Tenta outra.")
                            continue
                            
                        letras_descobertas.append(letra_digitada)
                        
                        if letra_digitada in palavra_secreta:
                            print("✅ Boa! Acertaste numa letra.")
                        else:
                            print("❌ Ops! Essa letra não existe na palavra.")
                            erros_permitidos -= 1
                else:
                    print("Escolha inválida. Tenta novamente.")

# Comando ai
        elif comando == "ai":
            print("\n--- Iniciando Conexão Neural (PyOS AI) ---")
            
            arquivo_config = "config_db.json"
            # Carrega as configurações para ver se já temos a chave da API
            if os.path.exists(arquivo_config):
                with open(arquivo_config, 'r', encoding='utf-8') as f:
                    banco_config = json.load(f)
            else:
                banco_config = {}

            # Verifica se o usuário atual já salvou uma chave de API
            chave_api = banco_config.get(f"{usuario}_api_key", "")

            # Se não tem chave, pede para o usuário digitar e salva no arquivo
            if not chave_api:
                print("Para usar a IA, você precisa de uma chave gratuita do Google AI Studio.")
                print("Pegue a sua em: https://aistudio.google.com/app/apikey")
                chave_api = input("Cole sua Chave de API aqui (ou digite 'sair' para cancelar): ").strip()
                
                if chave_api.lower() == 'sair':
                    continue
                
                # Salva a chave atrelada ao usuário
                banco_config[f"{usuario}_api_key"] = chave_api
                with open(arquivo_config, 'w', encoding='utf-8') as f:
                    json.dump(banco_config, f, indent=4)
                print("Chave salva com sucesso no seu perfil!")

            try:
                # Configura a IA com a chave do usuário
                genai.configure(api_key=chave_api)
                
                print("Procurando um modelo de IA compatível nos servidores do Google...", end="\r")
                
                # --- NOVO: BUSCA AUTOMÁTICA DE MODELO ---
                nome_modelo = None
                for m in genai.list_models():
                    # Procura o primeiro modelo que suporte geração de texto ('generateContent')
                    if 'generateContent' in m.supported_generation_methods:
                        nome_modelo = m.name
                        # Vamos dar preferência para os modelos mais novos (1.5) se existirem
                        if '1.5' in nome_modelo:
                            break 
                            
                if not nome_modelo:
                    print("Erro Crítico: Nenhum modelo de texto disponível para a sua conta/chave.")
                    continue
                    
                # Inicia o modelo que o PyOS descobriu sozinho!
                modelo = genai.GenerativeModel(nome_modelo)
                # ----------------------------------------
                
                # Limpa a linha de busca
                print(" " * 60, end="\r")
                
                chat = modelo.start_chat(history=[])
                print(f"\nConexão estabelecida usando o modelo: {nome_modelo}")
                print("Você está conversando com o Assistente PyOS. Digite ':q' ou 'sair' para voltar.")
                print("-" * 65)
                
                while True:
                    pergunta = input(f"\n[{usuario}] > ")
                    
                    if pergunta.strip().lower() in [':q', 'sair']:
                        print("Encerrando a conexão neural... Voltando ao PyOS.")
                        break
                    if not pergunta.strip():
                        continue
                        
                    print("[PyOS AI] Pensando...", end="\r")
                    resposta = chat.send_message(pergunta)
                    print(" " * 20, end="\r") 
                    print(f"[PyOS AI] {resposta.text}")
                    
            except Exception as e:
                print(f"\nErro de conexão com a IA: {e}")
                print("DICA: Se a sua chave estiver inválida, abra o arquivo 'config_db.json' e apague a linha da sua API key para o sistema pedir uma nova.")

# Comando server
        elif comando == "server":
            if argumento in ["web", "ftp"]:
                # Truque para pegar o IP local
                try:
                    import socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    ip_local = s.getsockname()[0]
                    s.close()
                except Exception:
                    ip_local = "127.0.0.1"

                # --- OPÇÃO 1: SERVIDOR WEB (Navegador) ---
                if argumento == "web":
                    import http.server
                    import socketserver
                    PORTA = 8000
                    Handler = http.server.SimpleHTTPRequestHandler
                    socketserver.TCPServer.allow_reuse_address = True
                    
                    try:
                        with socketserver.TCPServer(("", PORTA), Handler) as httpd:
                            print(f"\n--- Servidor WEB PyOS Iniciado ---")
                            print(f"🔗 Acesse no navegador: http://{ip_local}:{PORTA}")
                            print("Pressione 'Ctrl + C' no terminal para desligar.")
                            httpd.serve_forever()
                    except KeyboardInterrupt:
                        print("\nServidor WEB desligado com sucesso.")
                    except Exception as e:
                        print(f"\nErro no servidor WEB: {e}")

                # --- OPÇÃO 2: SERVIDOR FTP (Explorador de Arquivos) ---
                elif argumento == "ftp":
                    try:
                        # Importa as ferramentas do pyftpdlib
                        from pyftpdlib.authorizers import DummyAuthorizer
                        from pyftpdlib.handlers import FTPHandler
                        from pyftpdlib.servers import FTPServer
                        
                        PORTA_FTP = 2121
                        
                        # Configura as permissões (lê e escreve)
                        authorizer = DummyAuthorizer()
                        # 'elradfmw' significa permissão total: ler, escrever, deletar, criar pastas
                        authorizer.add_anonymous(os.getcwd(), perm='elradfmw')
                        
                        handler = FTPHandler
                        handler.authorizer = authorizer
                        
                        # Desliga as mensagens chatas de log do FTP para não poluir sua tela
                        import logging
                        logging.getLogger("pyftpdlib").setLevel(logging.WARNING)
                        
                        server = FTPServer((ip_local, PORTA_FTP), handler)
                        
                        print(f"\n--- Servidor FTP PyOS Iniciado ---")
                        print(f"Pasta compartilhada: {os.getcwd()}")
                        print(f"Abra o Explorador de Arquivos (Windows) e digite na barra de endereços lá em cima:")
                        print(f"🔗 ftp://{ip_local}:{PORTA_FTP}")
                        print("------------------------------------------")
                        print("Pressione 'Ctrl + C' no terminal para desligar.")
                        
                        server.serve_forever()
                        
                    except ImportError:
                        print("Erro: A biblioteca 'pyftpdlib' não está instalada.")
                        print("Abra o terminal do seu PC e digite: pip install pyftpdlib")
                    except KeyboardInterrupt:
                        print("\nServidor FTP desligado com sucesso. Voltando ao PyOS.")
                    except Exception as e:
                        print(f"\nErro no servidor FTP: {e}")
            else:
                print("Por favor, escolha o modo. Exemplo: server web OU server ftp")

# Comando cd
        elif comando == "cd":
            if argumento:
                try:
                    # Muda o diretório atual para o que o usuário digitou
                    os.chdir(argumento)
                    print(f"Diretório alterado para: {os.getcwd()}")
                except FileNotFoundError:
                    print(f"Erro: A pasta '{argumento}' não foi encontrada.")
                except NotADirectoryError:
                    print(f"Erro: '{argumento}' é um arquivo, não uma pasta.")
                except Exception as e:
                    print(f"Erro ao acessar a pasta: {e}")
            else:
                print("Por favor, digite o nome da pasta. Exemplo: 'cd Documentos (ou 'cd ..' para voltar)'")

# Comando search
        elif comando == "search":
            if argumento:
                print(f"\nVasculhando pastas por '{argumento}' a partir de: {os.getcwd()}")
                print("Isso pode levar alguns segundos dependendo da quantidade de arquivos...\n")
                
                encontrados = 0
                
                # os.walk percorre a pasta atual ('.') e absolutamente todas as subpastas dentro dela
                for raiz, pastas, arquivos in os.walk('.'):
                    
                    # 1. Procura se alguma pasta tem o nome que digitamos
                    for nome_pasta in pastas:
                        # Convertendo para minúsculo para a busca não diferenciar maiúsculas/minúsculas
                        if argumento.lower() in nome_pasta.lower():
                            caminho_completo = os.path.join(raiz, nome_pasta)
                            print(f" [PASTA]   {caminho_completo}")
                            encontrados += 1
                            
                    # 2. Procura se algum arquivo tem o nome que digitamos
                    for nome_arquivo in arquivos:
                        if argumento.lower() in nome_arquivo.lower():
                            caminho_completo = os.path.join(raiz, nome_arquivo)
                            print(f" [ARQUIVO] {caminho_completo}")
                            encontrados += 1
                
                if encontrados == 0:
                    print(f"Nenhum item contendo '{argumento}' foi encontrado por aqui.")
                else:
                    print(f"\nBusca concluída: {encontrados} item(s) encontrado(s).")
            else:
                print("Por favor, digite o nome ou parte do nome para buscar. Exemplo: procurar relatorio")

# Comando mkdir
        elif comando == "mkdir":
            if argumento:
                try:
                    os.mkdir(argumento)
                    print(f"Pasta '{argumento}' criada com sucesso!")
                except FileExistsError:
                    print(f"Erro: A pasta '{argumento}' já existe.")
                except Exception as e:
                    print(f"Erro ao criar a pasta: {e}")
            else:
                print("Por favor, digite o nome da pasta. Exemplo: 'mkdir arquivos_importantes'")
                
# Comando rmdir
        elif comando == "rmdir":
            if argumento:
                # Esta função ajuda a burlar o erro de "Acesso Negado" em arquivos protegidos
                def forcar_exclusao(funcao, caminho, informacoes_erro):
                    os.chmod(caminho, stat.S_IWRITE)
                    funcao(caminho)

                try:
                    # O parâmetro 'onerror' chama nossa função caso o Windows tente bloquear a exclusão
                    shutil.rmtree(argumento, onerror=forcar_exclusao)
                    print(f"Pasta '{argumento}' e todo o seu conteúdo foram deletados com sucesso!")
                except FileNotFoundError:
                    print(f"Erro: A pasta '{argumento}' não foi encontrada.")
                except NotADirectoryError:
                    print(f"Erro: '{argumento}' é um arquivo, não uma pasta. Use um comando para deletar arquivos.")
                except PermissionError:
                    print(f"Erro Crítico: Acesso negado. Certifique-se de que você não está DENTRO da pasta (use 'cd ..' para sair) e que nenhum programa está usando os arquivos.")
                except Exception as e:
                    print(f"Erro ao deletar a pasta: {e}")
            else:
                print("Por favor, digite o nome da pasta. Exemplo: 'rmdir pasta_antiga'")

# Comando open
        elif comando == "open":
            if argumento:
                if os.path.exists(argumento):
                    try:
                        # Verifica qual é o sistema operacional real do usuário para usar o comando certo
                        if sys.platform == "win32":
                            os.startfile(argumento)  # Comando específico para Windows
                        elif sys.platform == "darwin":
                            subprocess.call(["open", argumento])  # Comando específico para Mac
                        else:
                            subprocess.call(["xdg-open", argumento])  # Comando específico para Linux
                            
                        print(f"Abrindo '{argumento}'...")
                    except Exception as e:
                        print(f"Erro ao tentar abrir o arquivo: {e}")
                else:
                    print(f"Erro: O arquivo '{argumento}' não foi encontrado na pasta atual.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: 'open documento.pdf'")

# Comando delete
        elif comando == "delete":
            if argumento:
                # 1. Verifica se o que o usuário digitou realmente é um arquivo
                if os.path.isfile(argumento):
                    try:
                        # os.remove é a função do Python para deletar arquivos
                        os.remove(argumento)
                        print(f"Arquivo '{argumento}' deletado com sucesso!")
                    except PermissionError:
                        print(f"Erro: Acesso negado. O arquivo '{argumento}' pode estar aberto em outro programa ou ser protegido.")
                    except Exception as e:
                        print(f"Erro ao deletar o arquivo: {e}")
                        
                # 2. Se for uma pasta, avisa o usuário para usar o comando certo
                elif os.path.isdir(argumento):
                    print(f"Erro: '{argumento}' é uma pasta. Para deletar pastas, use o comando 'rmdir'.")
                    
                # 3. Se não for nenhum dos dois, o arquivo não existe ali
                else:
                    print(f"Erro: O arquivo '{argumento}' não foi encontrado na pasta atual.")
            else:
                print("Por favor, digite o nome do arquivo que deseja deletar. Exemplo: delete notas.txt")

# Comando empty
        elif comando == "empty":
            if argumento:
                try:
                    # Verifica se a pasta realmente existe e é um diretório
                    if os.path.isdir(argumento):
                        arquivos = os.listdir(argumento)
                        contador = 0
                        
                        for item in arquivos:
                            # Monta o caminho completo do arquivo
                            caminho_item = os.path.join(argumento, item)
                            
                            # Verifica se é um arquivo (para não tentar deletar uma subpasta sem querer)
                            if os.path.isfile(caminho_item):
                                os.remove(caminho_item)
                                contador += 1
                                
                        print(f"Sucesso: {contador} arquivo(s) deletado(s) da pasta '{argumento}'.")
                    else:
                        print(f"Erro: '{argumento}' não foi encontrada ou não é uma pasta.")
                except Exception as e:
                    print(f"Erro ao tentar esvaziar a pasta: {e}")
            else:
                print("Por favor, digite o nome da pasta. Exemplo: 'empty arquivos_velhos'")
                
# Comando lock  
        elif comando == "lock":
            if argumento:
                if os.path.exists(argumento):
                    senha = input(f"Crie uma senha para trancar '{argumento}': ")
                    
                    try:
                        # 1. Transforma a sua senha comum numa chave criptográfica forte de 32 bytes
                        chave = base64.urlsafe_b64encode(hashlib.sha256(senha.encode('utf-8')).digest())
                        fernet = Fernet(chave)
                        
                        # 2. Lê os dados originais do arquivo
                        with open(argumento, 'rb') as f:
                            dados_originais = f.read()
                            
                        # 3. Embaralha tudo usando a chave
                        dados_criptografados = fernet.encrypt(dados_originais)
                        
                        # 4. Salva o arquivo com um novo nome ".lock" e apaga o original
                        novo_nome = argumento + ".lock"
                        with open(novo_nome, 'wb') as f:
                            f.write(dados_criptografados)
                            
                        os.remove(argumento) # Apaga o arquivo desprotegido
                        print(f"🔒 Sucesso! Arquivo protegido salvo como '{novo_nome}'.")
                        print("ATENÇÃO: Se esquecer a senha, o arquivo será perdido para sempre!")
                        
                    except Exception as e:
                        print(f"Erro ao criptografar: {e}")
                else:
                    print(f"Erro: Arquivo '{argumento}' não encontrado.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: travar diario.txt")

# Comando unlock
        elif comando == "unlock":
            if argumento:
                if os.path.exists(argumento):
                    if not argumento.endswith('.lock'):
                        print("Aviso: O arquivo não tem a extensão '.lock'. Tem certeza de que está criptografado?")
                        
                    senha = input(f"Digite a senha para destravar '{argumento}': ")
                    
                    try:
                        # 1. Recria a chave usando a senha que você digitou
                        chave = base64.urlsafe_b64encode(hashlib.sha256(senha.encode('utf-8')).digest())
                        fernet = Fernet(chave)
                        
                        # 2. Lê os dados trancados
                        with open(argumento, 'rb') as f:
                            dados_criptografados = f.read()
                            
                        # 3. Tenta desembaralhar (se a senha estiver errada, a matemática falha e cai no except)
                        dados_originais = fernet.decrypt(dados_criptografados)
                        
                        # 4. Remove a extensão ".lock" do nome para voltar ao normal
                        nome_original = argumento.replace('.lock', '')
                        # Se por acaso o arquivo não tivesse .lock no nome, adiciona um sufixo para não sobrescrever errado
                        if nome_original == argumento: 
                            nome_original = "destravado_" + argumento
                            
                        # 5. Salva o arquivo legível e apaga a versão trancada
                        with open(nome_original, 'wb') as f:
                            f.write(dados_originais)
                            
                        os.remove(argumento)
                        print(f"🔓 Sucesso! Arquivo destravado e salvo como '{nome_original}'.")
                        
                    except Exception:
                        # O erro padrão da biblioteca para senha errada é o InvalidToken, mas tratamos de forma geral
                        print("❌ Erro: Senha incorreta ou arquivo corrompido! Acesso negado.")
                else:
                    print(f"Erro: Arquivo '{argumento}' não encontrado.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: destravar diario.txt.lock")

# Comando read
        elif comando == "txt_read":
            if argumento:
                # Verifica se o que o usuário digitou é realmente um arquivo
                if os.path.isfile(argumento):
                    try:
                        # Abre o arquivo em modo de leitura ('r') com suporte a acentos (utf-8)
                        with open(argumento, 'r', encoding='utf-8') as arquivo:
                            conteudo = arquivo.read()
                            print(f"\n--- Lendo: {argumento} ---\n")
                            print(conteudo)
                            print(f"\n--- Fim de {argumento} ---")
                    except UnicodeDecodeError:
                        print("Erro: Este não parece ser um arquivo de texto comum (não é possível ler).")
                    except Exception as e:
                        print(f"Erro ao ler o arquivo: {e}")
                else:
                    print(f"Erro: '{argumento}' não foi encontrado ou não é um arquivo válido.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: 'read notas.txt'")
                
# Comando write
        elif comando == "txt_write":
            if argumento:
                print(f"\n--- Escrevendo em: {argumento} ---")
                print("DICA: Digite ':q' para salvar/sair, ou ':u' para apagar a linha anterior.")
                print("-" * 65)
                
                linhas = []
                while True:
                    # Mostra o número da linha atual para facilitar
                    linha = input(f"{len(linhas) + 1} | ")
                    
                    if linha.strip() == ':q':
                        break
                    elif linha.strip() == ':u':
                        if len(linhas) > 0:
                            removida = linhas.pop() # Remove a última linha da lista
                            print(f"   [Linha '{removida}' apagada]")
                        else:
                            print("   [O arquivo já está vazio]")
                        continue
                        
                    linhas.append(linha)
                
                try:
                    with open(argumento, 'w', encoding='utf-8') as arquivo:
                        arquivo.write('\n'.join(linhas))
                    print(f"Arquivo '{argumento}' salvo com sucesso!")
                except Exception as e:
                    print(f"Erro ao salvar o arquivo: {e}")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: 'write notas.txt'")

# Comando edit
        elif comando == "txt_edit":
            if argumento:
                # Verifica se o arquivo existe antes de tentar editar
                if os.path.isfile(argumento):
                    try:
                        # 1. Abre o arquivo e lê as linhas que já existem lá dentro
                        with open(argumento, 'r', encoding='utf-8') as arquivo:
                            linhas = arquivo.read().splitlines()
                            
                        print(f"\n--- Editando: {argumento} ---")
                        print("Texto atual:")
                        
                        # Mostra o texto com os números das linhas
                        for i, l in enumerate(linhas):
                            print(f"{i + 1} | {l}")
                            
                        print("-" * 65)
                        print("Continue digitando para adicionar. Use ':q' para salvar ou ':u' para apagar.")
                        
                        # 2. Entra no mesmo loop de digitação do "escrever"
                        while True:
                            linha = input(f"{len(linhas) + 1} | ")
                            
                            if linha.strip() == ':q':
                                break
                            elif linha.strip() == ':u':
                                if len(linhas) > 0:
                                    removida = linhas.pop()
                                    print(f"   [Linha '{removida}' apagada]")
                                else:
                                    print("   [O arquivo já está vazio]")
                                continue
                                
                            linhas.append(linha)
                            
                        # 3. Salva o arquivo sobrescrevendo com a lista atualizada
                        with open(argumento, 'w', encoding='utf-8') as arquivo:
                            arquivo.write('\n'.join(linhas))
                        print(f"Arquivo '{argumento}' atualizado com sucesso!")
                        
                    except Exception as e:
                        print(f"Erro ao editar o arquivo: {e}")
                else:
                    print(f"Erro: '{argumento}' não foi encontrado. Se quiser criar um novo, use o comando 'write'.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: 'edit notas.txt'")

# Comando csv_write
        elif comando == "csv_write":
            if argumento:
                # Garante que o arquivo tenha a extensão correta
                if not argumento.endswith('.csv'):
                    argumento += '.csv'
                    
                if os.path.exists(argumento):
                    print(f"Erro: O arquivo '{argumento}' já existe. Use 'planilha_add' para inserir dados.")
                else:
                    print(f"\n--- Criando Planilha: {argumento} ---")
                    colunas = input("Digite o nome das colunas separados por vírgula (ex: Nome, Idade, Email): ")
                    
                    # Limpa os espaços extras em volta dos nomes das colunas
                    cabecalhos = [c.strip() for c in colunas.split(',')]
                    
                    try:
                        # Abre em modo 'w' para escrever a primeira linha (cabeçalhos)
                        with open(argumento, 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(cabecalhos)
                        print(f"Planilha '{argumento}' criada com as colunas: {', '.join(cabecalhos)}")
                    except Exception as e:
                        print(f"Erro ao criar planilha: {e}")
            else:
                print("Por favor, digite o nome da planilha. Exemplo: planilha_criar clientes.csv")

# Comando csv_add
        elif comando == "csv_add":
            if argumento:
                if not argumento.endswith('.csv'):
                    argumento += '.csv'
                    
                if os.path.exists(argumento):
                    try:
                        # Primeiro, lê o arquivo só para descobrir quais são as colunas
                        with open(argumento, 'r', encoding='utf-8') as f:
                            reader = csv.reader(f)
                            cabecalhos = next(reader, None) # Pega apenas a primeira linha
                        
                        if cabecalhos:
                            print(f"\n--- Adicionando dados em: {argumento} ---")
                            nova_linha = []
                            
                            # Pergunta o valor específico para cada coluna dinamicamente
                            for coluna in cabecalhos:
                                valor = input(f"Digite o valor para '{coluna}': ")
                                nova_linha.append(valor)
                            
                            # Agora abre em modo 'a' (append) para colar a nova linha no final
                            with open(argumento, 'a', newline='', encoding='utf-8') as f:
                                writer = csv.writer(f)
                                writer.writerow(nova_linha)
                            print("Dados adicionados com sucesso!")
                        else:
                            print("Erro: A planilha está vazia e não possui colunas definidas.")
                    except Exception as e:
                        print(f"Erro ao editar planilha: {e}")
                else:
                    print(f"Erro: Planilha '{argumento}' não encontrada. Crie primeiro com 'planilha_criar'.")
            else:
                print("Por favor, digite o nome da planilha. Exemplo: planilha_add clientes.csv")

# Comando csv_read
        elif comando == "csv_read":
            if argumento:
                if not argumento.endswith('.csv'):
                    argumento += '.csv'
                    
                if os.path.exists(argumento):
                    try:
                        with open(argumento, 'r', encoding='utf-8') as f:
                            reader = csv.reader(f)
                            dados = list(reader) # Transforma tudo numa lista do Python
                            
                            if not dados:
                                print("A planilha está vazia.")
                            else:
                                print(f"\n--- Lendo Planilha: {argumento} ---\n")
                                
                                # Encontra a maior palavra de cada coluna para alinhar a tabela perfeitamente
                                tamanhos = [max(len(str(item)) for item in coluna) for coluna in zip(*dados)]
                                
                                for i, linha in enumerate(dados):
                                    # Justifica o texto à esquerda baseado no tamanho máximo da coluna
                                    linha_formatada = " | ".join(str(item).ljust(tamanho) for item, tamanho in zip(linha, tamanhos))
                                    print(linha_formatada)
                                    
                                    # Imprime uma linha divisória logo abaixo do cabeçalho
                                    if i == 0:
                                        print("-" * len(linha_formatada))
                                        
                                print("\n--- Fim da Planilha ---")
                    except Exception as e:
                        print(f"Erro ao ler planilha: {e}")
                else:
                    print(f"Erro: Planilha '{argumento}' não encontrada.")
            else:
                print("Por favor, digite o nome da planilha. Exemplo: planilha_ler clientes.csv")

# Comando disk
        elif comando == "disk":
            try:
                # Analisa o disco com base no diretório em que estamos
                caminho_atual = os.getcwd()
                total, usado, livre = shutil.disk_usage(caminho_atual)
                
                # Converte os valores de bytes para Gigabytes (GB)
                gb = 1024 ** 3
                
                print(f"\nAnálise de Armazenamento do disco atual:")
                print(f" -> Espaço Total : {total // gb} GB")
                print(f" -> Espaço Usado : {usado // gb} GB")
                print(f" -> Espaço Livre : {livre // gb} GB")
            except Exception as e:
                print(f"Erro ao analisar o disco: {e}")

# Comando status
        elif comando == "status":
            print("\n--- Monitor de Hardware PyOS ---")
            print("Analisando sensores do sistema... (aguarde 1 segundo)\n")
            
            try:
                # Função interna para desenhar a barra de progresso visual
                def gerar_barra(porcentagem, tamanho=30):
                    preenchido = int(tamanho * porcentagem // 100)
                    vazio = tamanho - preenchido
                    return f"[{'█' * preenchido}{'-' * vazio}]"

                # 1. Lê a CPU (interval=1 faz o Python esperar 1 segundo para medir a velocidade real)
                cpu_uso = psutil.cpu_percent(interval=1)
                
                # 2. Lê a Memória RAM
                memoria = psutil.virtual_memory()
                ram_uso = memoria.percent
                ram_total = memoria.total / (1024**3) # Converte de bytes para Gigabytes (GB)
                ram_usada = memoria.used / (1024**3)
                
                # 3. Lê a Bateria (se for um notebook)
                bateria = psutil.sensors_battery()

                # Imprime os resultados com as barras
                print(f"CPU: {gerar_barra(cpu_uso)} {cpu_uso}%")
                print(f"RAM: {gerar_barra(ram_uso)} {ram_uso}% ({ram_usada:.1f}GB / {ram_total:.1f}GB)")
                
                # Verifica se o computador tem sensor de bateria
                if bateria:
                    status_tomada = "🔌 Conectado" if bateria.power_plugged else "🔋 Na Bateria"
                    print(f"BAT: {gerar_barra(bateria.percent)} {bateria.percent}% ({status_tomada})")
                else:
                    print("BAT: [ Sensor de bateria não detectado (Computador de Mesa?) ]")
                    
                print("-" * 32)
                
            except Exception as e:
                print(f"Erro ao ler os sensores de hardware: {e}")

# Comando devices
        elif comando == "devices":
            print("\n--- Gerenciador de Dispositivos PyOS ---")
            
            # 1. Lista Placas e Adaptadores de Rede
            print("🌐 Adaptadores de Rede:")
            try:
                redes = psutil.net_if_addrs()
                for placa in redes.keys():
                    # Ignora adaptadores virtuais estranhos do Windows para manter a lista limpa
                    if "Loopback" not in placa and "Pseudo" not in placa:
                        print(f"   [+] {placa}")
            except Exception as e:
                print(f"   Erro ao ler rede: {e}")

            print("\n🔌 Dispositivos USB Conectados:")
            print("   (Lendo portas, aguarde alguns segundos...)\n")
            
            # 2. Lista Dispositivos USB usando comandos nativos do sistema
            try:
                dispositivos_usb = []
                
                if sys.platform == 'win32':
                    # Pede para o PowerShell do Windows listar apenas os USBs ativos e com nome
                    cmd = ['powershell', '-Command', "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' -and $_.FriendlyName } | Select-Object -ExpandProperty FriendlyName"]
                    # errors='ignore' evita que caracteres com acento quebrem o código
                    output = subprocess.check_output(cmd, encoding='cp850', errors='ignore')
                    
                    # Limpa a lista e remove os "Hubs" genéricos que o Windows duplica
                    linhas = [linha.strip() for linha in output.split('\n') if linha.strip() and "Hub" not in linha]
                    dispositivos_usb = list(set(linhas)) # set() remove duplicatas
                    
                elif sys.platform == 'linux':
                    # Usa o comando lsusb do Linux
                    output = subprocess.check_output(['lsusb'], text=True)
                    dispositivos_usb = [linha.split(':', 2)[-1].strip() for linha in output.split('\n') if linha.strip()]
                    
                elif sys.platform == 'darwin':
                    # Usa o system_profiler do Mac
                    output = subprocess.check_output(['system_profiler', 'SPUSBDataType'], text=True)
                    dispositivos_usb = [linha.strip().replace(':', '') for linha in output.split('\n') if linha.startswith('        ') and ':' in linha and '0x' not in linha]
                
                # Imprime os resultados encontrados
                if dispositivos_usb:
                    for d in dispositivos_usb:
                        print(f"   [USB] {d}")
                else:
                    print("   Nenhum dispositivo USB nomeado encontrado.")
                    
            except Exception as e:
                print(f"   [Erro ao ler portas USB: O sistema bloqueou a varredura]")
                
            print("-" * 42)

# Comando adduser
        elif comando == "adduser":
            if argumento:
                arquivo_db = "usuarios_db.json"
                try:
                    # Carrega o banco de dados atual
                    with open(arquivo_db, 'r', encoding='utf-8') as f:
                        banco_usuarios = json.load(f)
                    
                    # Verifica se o usuário já existe
                    if argumento in banco_usuarios:
                        print(f"Erro: O usuário '{argumento}' já existe no sistema.")
                    else:
                        # Pede a senha para o novo usuário
                        nova_senha = input(f"Crie uma senha para o usuário '{argumento}': ")
                        banco_usuarios[argumento] = nova_senha
                        
                        # Salva a atualização no arquivo JSON
                        with open(arquivo_db, 'w', encoding='utf-8') as f:
                            json.dump(banco_usuarios, f, indent=4)
                        print(f"Usuário '{argumento}' criado com sucesso!")
                except Exception as e:
                    print(f"Erro ao gerenciar usuários: {e}")
            else:
                print("Por favor, digite o nome do novo usuário. Exemplo: adduser visitante")

# Comando dltuser
        elif comando == "dltuser":
            if argumento:
                # Trava de segurança: impede o suicídio digital!
                if argumento == usuario:
                    print("Erro Crítico: Você não pode deletar o seu próprio usuário enquanto está logado!")
                else:
                    arquivo_db = "usuarios_db.json"
                    arquivo_config = "config_db.json"
                    try:
                        with open(arquivo_db, 'r', encoding='utf-8') as f:
                            banco_usuarios = json.load(f)
                        
                        if argumento in banco_usuarios:
                            # Deleta o usuário do dicionário e salva
                            del banco_usuarios[argumento]
                            with open(arquivo_db, 'w', encoding='utf-8') as f:
                                json.dump(banco_usuarios, f, indent=4)
                            
                            # Limpeza extra: apaga as configurações de cor desse usuário, se existirem
                            if os.path.exists(arquivo_config):
                                with open(arquivo_config, 'r', encoding='utf-8') as f:
                                    banco_cores = json.load(f)
                                if argumento in banco_cores:
                                    del banco_cores[argumento]
                                    with open(arquivo_config, 'w', encoding='utf-8') as f:
                                        json.dump(banco_cores, f, indent=4)
                                        
                            print(f"Usuário '{argumento}' deletado do sistema com sucesso!")
                        else:
                            print(f"Erro: O usuário '{argumento}' não existe no banco de dados.")
                    except Exception as e:
                        print(f"Erro ao gerenciar usuários: {e}")
            else:
                print("Por favor, digite o nome do usuário que deseja deletar. Exemplo: dltuser visitante")

# Comando color
        elif comando == "color":
            cores = {
                "red": "\033[31m",
                "green": "\033[32m",
                "yellow": "\033[33m",
                "blue": "\033[34m",
                "purple": "\033[35m",
                "cyan": "\033[36m",
                "white": "\033[37m",
                "default": "\033[0m"
            }
            
            if argumento:
                cor_escolhida = argumento.lower()
                
                if cor_escolhida in cores:
                    # Aplica a cor na tela
                    print(cores[cor_escolhida], end="")
                    
                    if cor_escolhida == "default":
                        print("Cor restaurada para o padrão do sistema.")
                    else:
                        print(f"Cor alterada para {cor_escolhida}! Configuração salva.")
                        
                    # --- NOVO: Salvar no banco de dados de configurações ---
                    arquivo_config = "config_db.json"
                    if os.path.exists(arquivo_config):
                        with open(arquivo_config, 'r', encoding='utf-8') as f:
                            banco_cores = json.load(f)
                    else:
                        banco_cores = {}
                        
                    # Salva a cor escolhida associada ao nome do usuário logado
                    banco_cores[usuario] = cor_escolhida
                    
                    with open(arquivo_config, 'w', encoding='utf-8') as f:
                        json.dump(banco_cores, f, indent=4)
                    # -------------------------------------------------------
                else:
                    print("Cor inválida. As opções são:")
                    print(" -> red, green, yellow, blue, purple, cyan, white e default")
            else:
                print("Por favor, digite uma cor. Exemplo: 'color green'")

        else:
            print(f"Comando '{comando}' não reconhecido. Digite 'help' para ver a lista.")

if __name__ == "__main__":
    iniciar_pyos()
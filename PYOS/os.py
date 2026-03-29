# ==========================================
# MÓDULOS NATIVOS DO PYTHON (Já vêm instalados)
# ==========================================
import os, sys, shutil, stat, subprocess, time, datetime, threading
import json, csv, math, random, re, textwrap, unicodedata
import socket, socketserver, http.server
import urllib.request, urllib.parse, xml.etree.ElementTree as ET
import base64, hashlib

# ==========================================
# MÓDULOS DE TERCEIROS (Instalados via PIP)
# ==========================================
import psutil
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pyttsx3
import google.generativeai as genai
from bs4 import BeautifulSoup
from PIL import Image
from cryptography.fernet import Fernet
from deep_translator import GoogleTranslator

def limpar_tela():
    # Limpa a tela dependendo do sistema operacional real do usuário
    os.system('cls' if os.name == 'nt' else 'clear')

def iniciar_pyos():
    os.system('')
    limpar_tela()
    
    # --- NOVO: PREPARA O BANCO DE DADOS ---
    FOLDER_DATAS = "database"
    if not os.path.exists(FOLDER_DATAS):
        os.makedirs(FOLDER_DATAS)
    # --------------------------------------

    # --- NOVO SISTEMA DE LOGIN COM PALAVRA-PASSE E BASE DE DADOS ---
    arquivo_db = os.path.join(FOLDER_DATAS, "usuarios_db.json")
    
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
    arquivo_config = os.path.join(FOLDER_DATAS, "config_db.json")
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
    print(" Projeto feito por \033[1;31mCAFOX-E\033[0m com carinho")
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
            print("  help-web       : Exibe os comandos basicos para uso web")
            print("  help-archives  : Exibe os comandos de exploração de arquivos")
            print("  help-office    : Exibe os comandos de criação e edição de arquivos de textos e planilhas")
            print("  help-config    : Exibe os comandos de configurações de usuários e outros")
            print("  quit           : Desliga o sistema")
            print("  \033[1;31mself-destruct\033[0m  : Inicia o Protocolo Ômega (Apaga todos os dados e encerra o PyOS)")

        elif comando == "help-basics":
            print("\n--- Comandos Disponíveis ---")
            print("  help           : Mostra esta lista de comandos de ajuda")
            print("  logout         : Encerra a sessão atual e volta para a tela de login")
            print("  date           : Exibe a data e hora atuais")
            print("  time           : Mostra a previsão do tempo em ASCII Art (ex: time, ou time lisboa)")
            print("  ping           : Testa a conexão de rede com um site ou IP (ex: ping google.com)")
            print("  clear          : Limpa a tela do terminal")
            print("  rmnder         : Define um alarme falante em minutos (ex: lembrete 1 Tirar a pizza)")
            print("  print          : Repete o que você digitar (ex: print Hello World!)")
            print("  speak          : Faz o sistema ler um texto em voz alta (ex: speak Hello World!)")
            print("  calc           : Uma calculadora simples (ex: calc 5 + 5)")
            print("  play           : Abre o menu de mini-jogos do PyOS para relaxar")
            print("  task           : Gerencia as suas tarefas diárias (ex: task add, task read, task ok)")
            print("  banner         : Gera um letreiro gigante em ASCII art (ex: banner PyOS)")
            print("  listen         : Abre uma porta na sua rede e aguarda uma conexão secreta")
            print("  conect         : Conecta a um rádio PyOS que esteja a escutar (ex: conectar 192.168.0.15)")

        elif comando == "help-web":
            print("  news           : Exibe as 5 principais manchetes do momento")
            print("  price          : Mostra o valor do Dólar, Euro e Bitcoin em Reais (ex: price ou price btc)")
            print("  browse         : Lê o texto de um site diretamente no terminal (ex: browse pt.wikipedia.org/wiki/Linux)")
            print("  track          : Triangula a localização geográfica de um IP ou Site (ex: track google.com)")
            print("  wiki           : Consulta o Oráculo da Wikipédia sobre qualquer assunto (ex: wiki Buraco negro)")
            print("  translate      : Traduz textos entre idiomas (ex: traduzir en-pt Hello world)")
            print("  server         : Inicia o compartilhamento (ex: server web OU server ftp)")
            print("  ai             : Inicia uma conversa com a Inteligência Artificial (ex: ai)")

        elif comando == "help-archives":
            print("\n--- Comandos Disponíveis ---")
            print("  list           : Lista os arquivos na pasta atual")
            print("  cd             : Navega entre as pastas (ex: cd nome_da_pasta ou cd .. para voltar)")
            print("  search         : Busca arquivos e pastas pelo nome (ex: search projeto)")
            print("  mkdir          : Cria uma nova pasta (ex: mkdir nova_pasta)")
            print("  rmdir          : Deleta uma pasta (ex: rmdir pasta_antiga)")
            print("  tree           : Desenha o mapa visual de arquivos e pastas (ex: tree ou tree banco_de_dados)")
            print("  open           : Executa um arquivo com o programa padrão do seu computador (ex: open foto.jpg)")
            print("  delete         : Deleta um arquivo específico (ex: delete texto.txt)")
            print("  empty          : Apaga TODOS os arquivos de uma pasta de uma vez (ex: empty minha_pasta)")
            print("  lock           : Criptografa um arquivo com senha (ex: lock segredo.txt)")
            print("  unlock         : Descriptografa um arquivo bloqueado (ex: unlock segredo.txt.lock)")
            print("  hide           : Oculta um texto secreto dentro dos pixels de uma imagem (ex: hide foto.png A senha é 123)")
            print("  reveal         : Extrai a mensagem secreta escondida numa imagem (ex: reveal foto.png)")
            print("  base64         : Codifica ou decodifica textos no formato Base64 (ex: base64 encode texto)")
            print("  password       : Cofre criptografado de senhas (ex: password generate, password save, password read)")
            
        elif comando == "help-office":
            print("  txt_read       : Exibe o texto de um arquivo no terminal (ex: txt_read notas.txt)")
            print("  txt_write      : Cria/edita um arquivo de texto (ex: txt_write notas.txt)")
            print("  txt_edit       : Edita um arquivo de texto já existente (ex: txt_edit notas.txt)")
            print("  csv_write      : Cria uma nova planilha (ex: csv_write dados.csv)")
            print("  csv_add        : Adiciona uma linha de dados à planilha (ex: csv_add dados.csv)")
            print("  csv_read       : Lê e exibe uma planilha em formato de tabela (ex: csv_read dados.csv)")
            print("  open_image     : Abre e desenha uma imagem direto no terminal (ex: open_image foto.jpg)")
            print("  audio          : Reprodutor de música em segundo plano (ex: audio musica.mp3, audio pause, audio stop)")

        elif comando == "help-config":
            print("\n--- Comandos Disponíveis ---")
            print("  disk           : Analisa o espaço de armazenamento do disco atual")
            print("  status         : Mostra o uso de CPU, RAM e Bateria em tempo real")
            print("  devices        : Lista os adaptadores de rede e dispositivos USB conectados")
            print("  scan           : Mapeia a sua rede Wi-Fi local e lista os aparelhos conectados")
            print("  adduser        : Adiciona um novo usuário ao sistema (ex: adduser maria)")
            print("  dltuser        : Deleta um usuário do sistema (ex: dltuser joao)")
            
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

# Comando time
        elif comando == "time":          
            print("\n--- Satélite Meteorológico PyOS ---")
            print("Conectando à estação climática espacial... 🛰️\n")
            
            try:
                # Se o usuário digitou uma cidade (ex: clima curitiba), codifica os espaços e acentos
                cidade = urllib.parse.quote(argumento.strip()) if argumento else ""
                
                # O '?0' no final da URL diz ao servidor para mandar apenas o clima de AGORA (para não poluir a tela)
                url = f"https://wttr.in/{cidade}?0"
                
                # O Truque: Disfarçamos o Python de 'curl' (um comando de terminal de raiz) 
                # para o site nos devolver as cores ANSI em vez de um site HTML normal.
                requisicao = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
                
                with urllib.request.urlopen(requisicao) as resposta:
                    clima_ascii = resposta.read().decode('utf-8')
                    print(clima_ascii)
                    
            except Exception as e:
                print(f"Erro ao obter a leitura do satélite: {e}")
                print("DICA: Verifique a sua conexão com a internet.")

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

# Comando rmnder
        elif comando == "rmnder":
            # Verifica se o usuário digitou o tempo e a mensagem (ex: "5 Tirar a pizza")
            partes = argumento.split(" ", 1)
            
            if len(partes) >= 2 and partes[0].replace('.', '', 1).isdigit():
                minutos = float(partes[0])
                mensagem = partes[1]
                
                # Esta é a função que vai rodar escondida no fundo do sistema
                def iniciar_cronometro(tempo_minutos, texto_lembrete, nome_usuario):
                    import time
                    # Converte minutos para segundos e pausa a thread invisível
                    time.sleep(tempo_minutos * 60)
                    
                    # Quando o tempo acaba, ele "invade" o terminal para te avisar
                    print(f"\n\n⏰ [LEMBRETE DO SISTEMA]: {texto_lembrete.upper()}!")
                    # Reimprime o cursor do terminal para não bagunçar a sua tela
                    print(f"[{nome_usuario}] > ", end="", flush=True)
                    
                    # Tenta falar em voz alta usando o motor de voz do PyOS
                    try:
                        import pyttsx3
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 170)
                        engine.say(f"Atenção, lembrete: {texto_lembrete}")
                        engine.runAndWait()
                    except Exception:
                        pass

                # Prepara a "dimensão paralela" (Thread) com a nossa função
                thread_alarme = threading.Thread(target=iniciar_cronometro, args=(minutos, mensagem, usuario))
                
                # O daemon=True faz com que o alarme seja destruído automaticamente se você fechar o PyOS
                thread_alarme.daemon = True 
                
                # Dá o "play" no cronômetro invisível!
                thread_alarme.start()
                
                print(f"⏰ Lembrete configurado com sucesso para daqui a {minutos} minuto(s).")
                print("Pode continuar a usar o sistema normalmente!")
            else:
                print("Formato inválido. Use: lembrete [minutos] [mensagem]")
                print("Exemplo: lembrete 2.5 Olhar o pão no forno")

# Comando print
        elif comando == "print":
            print(argumento)

# Comando speak
        elif comando == "speak":
            if argumento:
                print(f"🗣️ PyOS diz: {argumento}")
                try:
                    # 1. Inicia o motor de voz
                    engine = pyttsx3.init()
                    
                    # 2. Configura a velocidade da voz (opcional, 150 a 200 é uma boa velocidade natural)
                    engine.setProperty('rate', 170)
                    
                    # 3. Faz o sistema falar!
                    engine.say(argumento)
                    
                    # 4. Espera a fala terminar antes de liberar o terminal de volta para você
                    engine.runAndWait()
                    
                except Exception as e:
                    print(f"Erro no módulo de voz: {e}")
                    print("DICA: Verifique se o volume do seu computador está ligado.")
            else:
                print("Por favor, digite o que eu devo falar. Exemplo: falar Sistema operacional ativado com sucesso.")

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

# Comando task
        elif comando == "task":
            
            # O ficheiro onde o PyOS vai guardar a sua vida
            arquivo_tarefas = os.path.join(FOLDER_DATAS, "tarefas_pyos.json")
            
            # 1. Carrega as tarefas existentes (se o ficheiro já existir)
            tarefas = []
            if os.path.exists(arquivo_tarefas):
                try:
                    with open(arquivo_tarefas, 'r', encoding='utf-8') as f:
                        tarefas = json.load(f)
                except Exception:
                    pass
            
            # Se o utilizador digitou apenas "task", mostramos o manual de uso
            if not argumento:
                print("\n\033[1;36m========== 📋 GERENCIADOR DE TAREFAS ==========\033[0m")
                print("Comandos disponíveis:")
                print("  \033[1;33mtask add [texto]\033[0m : Adiciona uma nova tarefa")
                print("  \033[1;33mtask read\033[0m        : Lista todas as suas tarefas")
                print("  \033[1;33mtask ok [numero]\033[0m : Marca uma tarefa como concluída")
                print("  \033[1;33mtask del [numero]\033[0m: Apaga uma tarefa da lista")
                print("\033[1;36m===============================================\033[0m\n")
                continue # Volta para o início do loop sem dar erro

            # Divide o que o utilizador digitou (ex: "add" e "Estudar Python")
            partes = argumento.split(" ", 1)
            acao = partes[0].lower()
            detalhe = partes[1] if len(partes) > 1 else ""

            # --- LÓGICA DE CRUD (Create, Read, Update, Delete) ---
            if acao == "add" and detalhe:
                tarefas.append({"texto": detalhe, "concluida": False})
                print(f"✅ \033[1;32mTarefa adicionada à base de dados:\033[0m {detalhe}")
            
            elif acao in ["read", "list"]:
                print("\n\033[1;36m========== 📋 AS SUAS TAREFAS ==========\033[0m")
                if not tarefas:
                    print("Nenhuma tarefa pendente. Você está livre! 🎮")
                else:
                    for i, t in enumerate(tarefas):
                        # Pinta o [X] de Verde e o [ ] de Vermelho
                        status = "\033[1;32m[X]\033[0m" if t["concluida"] else "\033[1;31m[ ]\033[0m"
                        # Risca o texto se estiver concluído usando código ANSI especial (\033[9m)
                        texto = f"\033[9m{t['texto']}\033[0m" if t["concluida"] else t['texto']
                        print(f" {i+1}. {status} {texto}")
                print("\033[1;36m========================================\033[0m\n")
            
            elif acao == "ok" and detalhe.isdigit():
                idx = int(detalhe) - 1
                if 0 <= idx < len(tarefas):
                    tarefas[idx]["concluida"] = True
                    print(f"🎉 \033[1;32mTarefa {idx+1} concluída!\033[0m Excelente trabalho.")
                else:
                    print("❌ Número de tarefa inválido.")
                    
            elif acao == "del" and detalhe.isdigit():
                idx = int(detalhe) - 1
                if 0 <= idx < len(tarefas):
                    removida = tarefas.pop(idx)
                    print(f"🗑️ \033[1;31mTarefa apagada:\033[0m {removida['texto']}")
                else:
                    print("❌ Número de tarefa inválido.")
            else:
                print("❌ Comando de tarefa não reconhecido. Digite apenas 'tarefa' para ajuda.")

            # 2. Salva as alterações de volta no disco rígido
            try:
                with open(arquivo_tarefas, 'w', encoding='utf-8') as f:
                    json.dump(tarefas, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Erro crítico ao salvar as tarefas: {e}")

# Comando banner
        elif comando == "banner":
            if not argumento:
                print("\n\033[1;36m========== 🎨 GERADOR DE BANNERS ==========\033[0m")
                print("❌ Uso correto: banner [texto]")
                print("Exemplo: banner Sistema Hackeado")
                print("\033[1;36m===========================================\033[0m\n")
            else:
                try:
                    import pyfiglet
                    
                    # Usa a fonte 'slant' para um visual inclinado e moderno
                    # O width=100 garante que o texto não quebre tão fácil se a tela for pequena
                    banner_ascii = pyfiglet.figlet_format(argumento, font="slant", width=100)
                    
                    # Imprime o banner em Ciano Brilhante
                    print(f"\n\033[1;36m{banner_ascii}\033[0m")
                    
                except ImportError:
                    print("❌ Biblioteca ausente. Abra o CMD normal e digite: pip install pyfiglet")
                except pyfiglet.FontNotFound:
                    print("❌ Fonte ASCII não encontrada pelo sistema.")
                except Exception as e:
                    print(f"❌ Erro ao gerar o letreiro: {e}")

# Comando listen
        elif comando == "listen":
            import socket
            import threading
            from datetime import datetime
            
            print("\n\033[1;35m========== 📻 RÁDIO FANTASMA (SERVIDOR) ==========\033[0m")
            
            arquivo_log = os.path.join(FOLDER_DATAS, "interceptacoes_radio.log")
            
            # Função invisível que grava tudo no arquivo de log
            def gravar_log(remetente, mensagem):
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                try:
                    with open(arquivo_log, "a", encoding="utf-8") as f:
                        f.write(f"[{agora}] {remetente}: {mensagem}\n")
                except:
                    pass
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                meu_ip = s.getsockname()[0]
            except:
                meu_ip = "127.0.0.1"
            finally:
                s.close()
                
            porta_secreta = 9999
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                servidor.bind(("0.0.0.0", porta_secreta))
                servidor.listen(1)
                
                print(f"📡 Torre de Rádio erguida! Frequência: \033[1;33m{porta_secreta}\033[0m")
                print(f"Diga para o seu parceiro digitar: \033[1;36mconectar {meu_ip}\033[0m")
                print("Aguardando infiltração...\n")
                
                conexao, endereco = servidor.accept()
                
                print(f"✅ \033[1;32mConexão estabelecida com o Agente {endereco[0]}!\033[0m")
                print("Chat Ponto-a-Ponto iniciado. Tudo está sendo gravado nos logs.")
                print("\033[1;35m==================================================\033[0m\n")
                
                # Marca o início da conversa no log
                gravar_log("SISTEMA", f"=== CONEXÃO INICIADA COM {endereco[0]} ===")
                
                chat_ativo = [True]
                
                def receber_mensagens(conn):
                    while chat_ativo[0]:
                        try:
                            msg = conn.recv(1024).decode('utf-8')
                            if not msg or msg.lower() == 'sair':
                                print("\n❌ \033[1;31mO parceiro cortou a linha.\033[0m Pressione Enter para voltar.")
                                gravar_log("SISTEMA", "=== O PARCEIRO DESCONECTOU ===")
                                chat_ativo[0] = False
                                break
                            
                            # Imprime na tela e grava no arquivo invisível!
                            print(f"\n\033[1;36m[Parceiro]:\033[0m \033[1;37m{msg}\033[0m")
                            gravar_log(endereco[0], msg)
                        except:
                            break
                            
                threading.Thread(target=receber_mensagens, args=(conexao,), daemon=True).start()
                
                while chat_ativo[0]:
                    try:
                        texto = input()
                        if not chat_ativo[0]: break
                        
                        if texto.lower() == 'sair':
                            conexao.send("sair".encode('utf-8'))
                            chat_ativo[0] = False
                            gravar_log("SISTEMA", "=== VOCÊ ENCERROU A CONEXÃO ===")
                            print("Desligando transmissores...")
                            break
                            
                        if texto.strip():
                            sys.stdout.write("\033[F\033[K")
                            print(f"\033[1;32m[Você]:\033[0m \033[1;37m{texto}\033[0m")
                            # Grava a sua mensagem e envia para o parceiro
                            gravar_log(meu_ip, texto)
                            conexao.send(texto.encode('utf-8'))
                    except:
                        break
                        
                conexao.close()
                servidor.close()
            except Exception as e:
                print(f"❌ Falha nos transmissores: {e}")

# Comando conect
        elif comando == "conect":
            import socket
            import threading
            from datetime import datetime
            
            if not argumento:
                print("\n\033[1;35m========== 📻 RÁDIO FANTASMA ==========\033[0m")
                print("❌ Uso correto: conectar [IP_DA_TORRE]")
                print("Exemplo: conectar 192.168.0.15")
                print("\033[1;35m=======================================\033[0m\n")
                continue
                
            ip_alvo = argumento.strip()
            porta_secreta = 9999
            
            arquivo_log = os.path.join(FOLDER_DATAS, "interceptacoes_radio.log")
            
            def gravar_log(remetente, mensagem):
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                try:
                    with open(arquivo_log, "a", encoding="utf-8") as f:
                        f.write(f"[{agora}] {remetente}: {mensagem}\n")
                except:
                    pass
            
            print(f"\n\033[1;35m========== 📻 RÁDIO FANTASMA (INFILTRADOR) ==========\033[0m")
            print(f"Tentando sintonizar na frequência do IP {ip_alvo}...")
            
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                cliente.connect((ip_alvo, porta_secreta))
                
                print(f"✅ \033[1;32mInfiltração bem sucedida!\033[0m")
                print("Chat Ponto-a-Ponto iniciado. Tudo está sendo gravado nos logs.")
                print("\033[1;35m=====================================================\033[0m\n")
                
                gravar_log("SISTEMA", f"=== VOCÊ SE INFILTROU NO IP {ip_alvo} ===")
                
                chat_ativo = [True]
                
                def receber_mensagens(conn):
                    while chat_ativo[0]:
                        try:
                            msg = conn.recv(1024).decode('utf-8')
                            if not msg or msg.lower() == 'sair':
                                print("\n❌ \033[1;31mA torre desligou a transmissão.\033[0m Pressione Enter para voltar.")
                                gravar_log("SISTEMA", "=== A TORRE DESCONECTOU ===")
                                chat_ativo[0] = False
                                break
                            print(f"\n\033[1;36m[Parceiro]:\033[0m \033[1;37m{msg}\033[0m")
                            gravar_log(ip_alvo, msg)
                        except:
                            break
                            
                threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True).start()
                
                while chat_ativo[0]:
                    try:
                        texto = input()
                        if not chat_ativo[0]: break
                        
                        if texto.lower() == 'sair':
                            cliente.send("sair".encode('utf-8'))
                            chat_ativo[0] = False
                            gravar_log("SISTEMA", "=== VOCÊ CORTOU A LINHA ===")
                            print("Desconectando da torre...")
                            break
                            
                        if texto.strip():
                            sys.stdout.write("\033[F\033[K")
                            print(f"\033[1;32m[Você]:\033[0m \033[1;37m{texto}\033[0m")
                            gravar_log("VOCÊ", texto)
                            cliente.send(texto.encode('utf-8'))
                    except:
                        break
                        
                cliente.close()
            except ConnectionRefusedError:
                print(f"❌ \033[1;31mConexão Recusada:\033[0m O IP {ip_alvo} não está rodando o comando 'listen'.")
            except Exception as e:
                print(f"❌ Erro de conexão: {e}")

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

# Comando ai
        elif comando == "ai":
            print("\n--- Iniciando Conexão Neural (PyOS AI) ---")
            
            arquivo_config = os.path.join(FOLDER_DATAS, "config_db.json")
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

# Comando news
        elif comando == "news":
            print("\n--- Central de Notícias PyOS ---")
            print("Conectando aos satélites de informação... 📡\n")
            
            try:
                # Usamos o RSS do Google News focado nas principais notícias (em Português)
                url = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"
                
                # Disfarçamos o PyOS de navegador normal para o servidor não bloquear a nossa conexão
                requisicao = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                # Baixa o arquivo XML com as notícias
                with urllib.request.urlopen(requisicao) as resposta:
                    dados_xml = resposta.read()
                    
                # A mágica do Python: Transforma o texto XML numa árvore de dados que podemos navegar
                raiz = ET.fromstring(dados_xml)
                
                # Procura por todos os 'itens' (que são as notícias) dentro do 'canal' do RSS
                noticias_encontradas = raiz.findall('./channel/item')
                
                if not noticias_encontradas:
                    print("Nenhuma notícia encontrada no momento.")
                else:
                    # Pega apenas as 5 primeiras notícias da lista
                    for i, item in enumerate(noticias_encontradas[:5], 1):
                        titulo = item.find('title').text
                        link = item.find('link').text
                        
                        # Imprime o título e o link formatados
                        print(f"{i}. 📰 {titulo}")
                        print(f"   🔗 {link}\n")
                        
                print("-" * 65)
                print("DICA: Segure a tecla 'Ctrl' (ou 'Cmd' no Mac) e clique no link para abrir no seu navegador real!")
                
            except Exception as e:
                print(f"Erro ao buscar notícias: {e}")
                print("DICA: Verifique a sua conexão com a internet.")

# Comando price
        elif comando == "price":
            print(f"\n\033[1;32m========== 📈 PAINEL FINANCEIRO PyOS ==========\033[0m")
            print("Conectando aos servidores da Bolsa de Valores...\n")
            
            # Define qual moeda buscar (se não digitar nada, mostra todas)
            moeda_escolhida = argumento.upper().strip() if argumento else "TODAS"
            
            try:
                # URL da AwesomeAPI que traz as cotações em tempo real para o BRL (Real Brasileiro)
                url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
                requisicao = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(requisicao) as resposta:
                    # Lê a resposta da internet e converte o JSON para um dicionário Python
                    dados = json.loads(resposta.read().decode('utf-8'))
                    
                # Função interna para formatar e imprimir cada moeda bonitinha na tela
                def exibir_moeda(sigla, nome, dados_moeda):
                    valor = float(dados_moeda['bid'])
                    variacao = float(dados_moeda['pctChange'])
                    
                    # Define a cor da variação (Verde para alta, Vermelho para baixa)
                    cor_var = "\033[1;32m▲" if variacao > 0 else "\033[1;31m▼"
                    
                    # Formata o número para o padrão brasileiro (R$ 5.12)
                    if sigla == "BTC":
                        # O Bitcoin é um valor muito alto, então formatamos com separador de milhar
                        valor_str = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    else:
                        valor_str = f"{valor:.2f}".replace(".", ",")
                        
                    print(f"💰 \033[1;37m{nome} ({sigla}):\033[0m R$ {valor_str}  {cor_var} {variacao}%\033[0m")

                # Exibe de acordo com o que o usuário pediu
                if moeda_escolhida in ["USD", "TODAS"]:
                    exibir_moeda("USD", "Dólar Comercial", dados['USDBRL'])
                if moeda_escolhida in ["EUR", "TODAS"]:
                    exibir_moeda("EUR", "Euro          ", dados['EURBRL'])
                if moeda_escolhida in ["BTC", "TODAS"]:
                    exibir_moeda("BTC", "Bitcoin       ", dados['BTCBRL'])
                
                if moeda_escolhida not in ["USD", "EUR", "BTC", "TODAS"]:
                    print(f"❌ Moeda '{moeda_escolhida}' não encontrada no acesso rápido.")
                    print("Tente digitar apenas: cotacao usd, cotacao eur ou cotacao btc.")
                    
            except Exception as e:
                print(f"\033[1;31mErro ao acessar os dados financeiros: {e}\033[0m")
                print("DICA: Verifique a sua conexão com a internet ou se a API está no ar.")
                
            print(f"\033[1;32m===============================================\033[0m\n")

# Comando browse
        elif comando == "browse":
            if argumento:
                # \033[1;36m deixa o texto em Ciano Negrito, e \033[0m reseta a cor
                print(f"\n\033[1;36m========== 🌐 NAVEGADOR PyOS LYNX ==========\033[0m")
                
                url = argumento if argumento.startswith('http') else 'http://' + argumento
                print(f"\033[33mAcessando:\033[0m {url}\n") # \033[33m é Amarelo
                
                try:
                    requisicao = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    with urllib.request.urlopen(requisicao) as resposta:
                        html_bruto = resposta.read().decode('utf-8', errors='ignore')
                        
                    soup = BeautifulSoup(html_bruto, 'html.parser')
                    
                    for elemento_lixo in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
                        elemento_lixo.extract()
                        
                    texto_limpo = soup.get_text(separator='\n')
                    linhas_formatadas = [linha.strip() for linha in texto_limpo.splitlines() if linha.strip()]
                    
                    # --- A MÁGICA DA FORMATAÇÃO DE TEXTO ---
                    linhas_exibidas = 0
                    limite_linhas = 40 # Reduzimos um pouco o limite para a leitura ficar mais focada
                    
                    for linha in linhas_formatadas:
                        if linhas_exibidas >= limite_linhas:
                            break
                            
                        # Se a linha for muito curta (como um menu que sobrou), ignoramos para manter a tela limpa
                        if len(linha) < 15:
                            continue
                            
                        # O textwrap vai "dobrar" o texto para não passar de 80 caracteres de largura
                        paragrafo_bonito = textwrap.fill(linha, width=80)
                        
                        print(paragrafo_bonito)
                        print() # Imprime uma linha em branco para separar os parágrafos
                        
                        # Conta quantas linhas reais esse parágrafo ocupou na tela
                        linhas_exibidas += paragrafo_bonito.count('\n') + 1 
                    # ---------------------------------------
                    
                    if len(linhas_formatadas) > limite_linhas:
                        print(f"\033[1;30m[... Fim da prévia do Modo Leitura ...]\033[0m")
                        
                    print(f"\033[1;36m=============================================\033[0m\n")
                    
                except Exception as e:
                    print(f"\033[1;31mErro ao carregar a página: {e}\033[0m") # Vermelho para erro
                    print("DICA: Verifique se o link está correto (ex: pt.wikipedia.org).")
            else:
                print("Por favor, digite o link do site. Exemplo: navegar pt.wikipedia.org/wiki/Python")

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

# Comando track
        elif comando == "track":
            if argumento:
                # \033[1;36m é a cor Ciano (Azul claro brilhante)
                print(f"\n\033[1;36m========== 🌍 RASTREADOR GLOBAL PyOS ==========\033[0m")
                print(f"A triangular o alvo: {argumento}...\n")
                
                try:
                    # Se o utilizador digitar com "https://", limpamos para o radar funcionar bem
                    alvo = argumento.replace("https://", "").replace("http://", "").split("/")[0]
                    
                    # API gratuita de geolocalização (não precisa de chave)
                    url = f"http://ip-api.com/json/{alvo}"
                    requisicao = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    with urllib.request.urlopen(requisicao) as resposta:
                        dados = json.loads(resposta.read().decode('utf-8'))
                        
                    # Verifica se a API conseguiu encontrar o alvo com sucesso
                    if dados.get("status") == "success":
                        # Imprime os dados formatados com cores (Amarelo para as etiquetas)
                        print(f"📍 \033[1;33mIP Alvo:\033[0m      {dados.get('query')}")
                        print(f"🏙️ \033[1;33mCidade:\033[0m       {dados.get('city')} - {dados.get('regionName')}")
                        print(f"🏳️ \033[1;33mPaís:\033[0m         {dados.get('country')} ({dados.get('countryCode')})")
                        print(f"🏢 \033[1;33mProvedor:\033[0m     {dados.get('isp')}")
                        print(f"🗺️ \033[1;33mCoordenadas:\033[0m  Lat {dados.get('lat')}, Lon {dados.get('lon')}")
                        print(f"🕒 \033[1;33mFuso Horário:\033[0m {dados.get('timezone')}")
                        
                        # Easter Egg: Link direto para o mapa
                        link_mapa = f"https://www.google.com/maps/search/?api=1&query={dados.get('lat')},{dados.get('lon')}"
                        print(f"\n🔗 \033[1;34mSatélite (Clique com Ctrl):\033[0m {link_mapa}")
                    else:
                        print(f"❌ \033[1;31mFalha na triangulação:\033[0m Não foi possível localizar '{alvo}'.")
                        
                except Exception as e:
                    print(f"\033[1;31mErro de conexão com os satélites: {e}\033[0m")
                    print("DICA: Verifique a sua conexão com a internet.")
                    
                print(f"\033[1;36m===============================================\033[0m\n")
            else:
                print("Por favor, digite um IP ou site. Exemplo: rastrear google.com ou rastrear 8.8.8.8")

# Comando wiki
        elif comando == "wiki":
            if argumento:
                # Cor Azul Escuro/Anil (\033[1;34m) para combinar com a identidade da Wikipédia
                print(f"\n\033[1;34m========== 📚 ORÁCULO WIKIPÉDIA ==========\033[0m")
                print(f"Consultando os arquivos da humanidade sobre: '{argumento}'...\n")
                
                try:
                    # Prepara o nome que o usuário digitou para virar um link válido (ex: "Buraco negro" vira "Buraco%20negro")
                    termo_busca = urllib.parse.quote(argumento.strip().capitalize())
                    
                    # API oficial da Wikipédia que devolve apenas o Resumo em Português
                    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_busca}"
                    
                    # A Wikipédia exige um User-Agent para saber quem está acessando
                    requisicao = urllib.request.Request(url, headers={'User-Agent': 'PyOS/1.0 (Terminal Hacking)'})
                    
                    with urllib.request.urlopen(requisicao) as resposta:
                        dados = json.loads(resposta.read().decode('utf-8'))
                        
                    # Se a API retornou um resumo (extract)
                    if 'extract' in dados:
                        resumo = dados['extract']
                        
                        # Usa o textwrap para formatar o texto em 80 colunas, ficando igual a um livro
                        paragrafos = textwrap.wrap(resumo, width=80)
                        for linha in paragrafos:
                            print(linha)
                            
                        # Easter Egg: Deixa o link direto caso você queira ler o resto no navegador
                        if 'content_urls' in dados and 'desktop' in dados['content_urls']:
                            link_completo = dados['content_urls']['desktop']['page']
                            print(f"\n🔗 \033[1;36mLeia o artigo completo em:\033[0m {link_completo}")
                    else:
                        print(f"❌ Não encontrei um resumo exato para '{argumento}'.")
                        
                except urllib.error.HTTPError as e:
                    # O erro 404 significa que a página não existe lá na Wikipédia
                    if e.code == 404:
                        print(f"❌ \033[1;31mArtigo não encontrado:\033[0m A Wikipédia não tem uma página exata com o nome '{argumento}'.")
                        print("DICA: Tente ser mais específico ou verificar a ortografia (ex: wiki Albert Einstein).")
                    else:
                        print(f"Erro na comunicação com a Wikipédia: {e}")
                except Exception as e:
                    print(f"\033[1;31mErro de conexão: {e}\033[0m")
                    
                print(f"\033[1;34m==========================================\033[0m\n")
            else:
                print("Por favor, digite o que deseja pesquisar. Exemplo: wiki Inteligência artificial")

# Comando translate
        elif comando == "translate":
            if argumento:
                partes = argumento.split(" ", 1)
                
                if len(partes) >= 2 and "-" in partes[0]:
                    idiomas = partes[0].strip() 
                    texto = partes[1].strip()
                    
                    try:
                        origem, destino = idiomas.split("-", 1)
                        
                        print(f"\n\033[1;35m========== 🌐 TRADUTOR GOOGLE ==========\033[0m")
                        print(f"Traduzindo de [\033[1;33m{origem.upper()}\033[0m] para [\033[1;33m{destino.upper()}\033[0m]...\n")
                        
                        # A MÁGICA: Usando o motor do Google Translate por baixo dos panos!
                        traducao = GoogleTranslator(source=origem, target=destino).translate(texto)
                            
                        print(f"📝 \033[1;32mOriginal:\033[0m {texto}")
                        
                        print(f"✨ \033[1;36mTradução:\033[0m")
                        linhas_traducao = textwrap.wrap(traducao, width=75)
                        for linha in linhas_traducao:
                            print(f"   {linha}")
                            
                    except ValueError:
                        print("❌ Formato de idioma inválido. Use hífen. Exemplo: en-pt, pt-en")
                    except Exception as e:
                        print(f"\033[1;31mErro na tradução: {e}\033[0m")
                        print("DICA: Verifique se as siglas dos idiomas estão corretas (ex: 'en', 'pt', 'es').")
                        
                    print(f"\033[1;35m========================================\033[0m\n")
                else:
                    print("Formato inválido. Use: translate [origem]-[destino] [texto]")
                    print("Exemplo: translate en-pt The quick brown fox jumps over the lazy dog")
            else:
                print("Por favor, digite o idioma e o texto. Ex: translate pt-en Olá mundo")

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

# Comando tree
        elif comando == "tree":
            
            # Se não digitar nada, mapeia a pasta atual ("."). Se digitar, mapeia a pasta escolhida.
            alvo = argumento.strip() if argumento else "."
            
            if not os.path.exists(alvo):
                print(f"❌ A pasta '{alvo}' não existe.")
                continue
                
            print(f"\n\033[1;36m========== 🌳 MAPA DE DIRETÓRIOS ==========\033[0m")
            print(f"Mapeando a estrutura de: \033[1;33m{os.path.abspath(alvo)}\033[0m\n")
            
            # A função mágica que desenha as linhas
            def gerar_arvore(caminho, prefixo="", nivel_atual=0, nivel_max=3):
                # Trava de segurança para não travar o PC lendo o HD inteiro
                if nivel_atual > nivel_max:
                    print(prefixo + "└── \033[1;30m[... limite de profundidade atingido ...]\033[0m")
                    return
                    
                try:
                    # Pega tudo o que tem na pasta e organiza (pastas e arquivos)
                    itens = os.listdir(caminho)
                    itens.sort()
                except PermissionError:
                    # Se o Windows/Linux bloquear o acesso a pastas de sistema
                    print(prefixo + "└── \033[1;31m⛔ [Acesso Negado]\033[0m")
                    return
                    
                total = len(itens)
                for i, item in enumerate(itens):
                    ultimo = (i == total - 1)
                    caminho_completo = os.path.join(caminho, item)
                    
                    # Desenha as quinas e retas
                    ponteiro = "└── " if ultimo else "├── "
                    
                    if os.path.isdir(caminho_completo):
                        # Se for pasta, pinta de Azul e coloca o ícone
                        print(prefixo + ponteiro + "\033[1;34m📁 " + item + "\033[0m")
                        # Prepara o espaçamento para desenhar o que tem dentro DESSA pasta
                        extensao = "    " if ultimo else "│   "
                        gerar_arvore(caminho_completo, prefixo + extensao, nivel_atual + 1, nivel_max)
                    else:
                        # Se for arquivo normal, pinta de Cinza Claro e coloca ícone
                        print(prefixo + ponteiro + "\033[0;37m📄 " + item + "\033[0m")

            # Inicia o mapeamento a partir da pasta raiz que você escolheu
            print("\033[1;34m📁 " + os.path.basename(os.path.abspath(alvo)) + "\033[0m")
            gerar_arvore(alvo)
            
            print(f"\n\033[1;36m===========================================\033[0m\n")

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

# Comando hide
        elif comando == "hide":
            # O comando espera algo como: esconder imagem.png Minha mensagem secreta
            partes = argumento.split(" ", 1)
            
            if len(partes) < 2:
                print("❌ Uso correto: esconder [nome_da_imagem.png] [sua mensagem secreta]")
                print("DICA: Use imagens .PNG! Imagens .JPG destroem os dados ocultos por causa da compressão.")
            else:
                img_path = partes[0]
                # Adicionamos um "marcador final" para o PyOS saber onde a mensagem acaba
                mensagem = partes[1] + "@@FIM@@" 
                
                try:
                    from PIL import Image
                    print(f"\n\033[1;35m========== 🕵️ ESTEGANOGRAFIA ==========\033[0m")
                    print(f"A injetar dados em '{img_path}'...")
                    
                    img = Image.open(img_path)
                    img = img.convert('RGB') # Garante que temos os canais Red, Green, Blue
                    pixels = img.load()
                    largura, altura = img.size
                    
                    # Converte a mensagem de texto para zeros e uns (Binário)
                    binario = ''.join([format(ord(i), "08b") for i in mensagem])
                    tamanho_bin = len(binario)
                    
                    # Verifica se a imagem tem pixels suficientes para o tamanho do texto
                    if tamanho_bin > largura * altura:
                        print("❌ Erro: A imagem é muito pequena para esconder essa quantidade de texto!")
                    else:
                        idx = 0
                        # Varre a imagem pixel por pixel
                        for y in range(altura):
                            for x in range(largura):
                                if idx < tamanho_bin:
                                    r, g, b = pixels[x, y]
                                    
                                    # MÁGICA LSB: Limpa o último bit da cor Vermelha e injeta o nosso bit da mensagem
                                    r = (r & 254) | int(binario[idx])
                                    
                                    pixels[x, y] = (r, g, b)
                                    idx += 1
                                else:
                                    break
                            if idx >= tamanho_bin:
                                break
                        
                        novo_nome = "secreto_" + img_path
                        img.save(novo_nome) # Salva a nova imagem sem perdas
                        print(f"✅ \033[1;32mSucesso!\033[0m Mensagem injetada de forma indetetável.")
                        print(f"A sua nova imagem camuflada chama-se: \033[1;33m{novo_nome}\033[0m")
                        
                except FileNotFoundError:
                    print(f"❌ Imagem '{img_path}' não encontrada na pasta atual.")
                except Exception as e:
                    print(f"Erro crítico no motor de injeção: {e}")
                print(f"\033[1;35m=======================================\033[0m\n")

# Comando reveal
        elif comando == "reveal":
            if not argumento:
                print("❌ Uso correto: reveal [nome_da_imagem_secreta.png]")
            else:
                img_path = argumento
                try:
                    from PIL import Image
                    print(f"\n\033[1;35m========== 👁️ DECODIFICADOR ==========\033[0m")
                    print(f"A analisar pixels de '{img_path}' à procura de anomalias LSB...\n")
                    
                    img = Image.open(img_path)
                    img = img.convert('RGB')
                    pixels = img.load()
                    largura, altura = img.size
                    
                    # Extrai o último bit do canal vermelho de todos os pixels
                    binario = ""
                    for y in range(altura):
                        for x in range(largura):
                            r, g, b = pixels[x, y]
                            binario += str(r & 1)
                            
                    # Agrupa os bits de 8 em 8 para transformar de volta em letras
                    mensagem_extraida = ""
                    for i in range(0, len(binario), 8):
                        byte = binario[i:i+8]
                        if len(byte) == 8:
                            mensagem_extraida += chr(int(byte, 2))
                            # Assim que encontrar o nosso marcador final, para a busca
                            if mensagem_extraida.endswith("@@FIM@@"):
                                mensagem_extraida = mensagem_extraida[:-7] # Remove o marcador
                                break
                                
                    print(f"🔓 \033[1;36mMensagem Revelada:\033[0m \033[1;37m{mensagem_extraida}\033[0m")
                    
                except FileNotFoundError:
                    print(f"❌ Imagem '{img_path}' não encontrada.")
                except Exception as e:
                    print(f"Erro ao extrair dados: {e}. Tem a certeza que esta imagem tem uma mensagem oculta?")
                print(f"\033[1;35m=======================================\033[0m\n")

# Comando base64
        elif comando == "base64":
            import base64
            
            # Se o usuário não digitar nada ou digitar errado
            if not argumento or " " not in argumento:
                print("\n\033[1;34m========== 🔠 CODIFICADOR BASE64 ==========\033[0m")
                print("Uso correto:")
                print("  \033[1;33mbase64 encode [texto]\033[0m : Transforma um texto em Base64")
                print("  \033[1;33mbase64 decode [texto]\033[0m : Reverte um Base64 para texto normal")
                print("\033[1;34m===========================================\033[0m\n")
                continue
                
            # Divide o comando da mensagem ("encode" ou "decode" e o "texto")
            partes = argumento.split(" ", 1)
            acao = partes[0].lower()
            texto = partes[1]
            
            if acao in ["encode", "codificar"]:
                try:
                    # O Python exige que o texto vire "bytes" antes de ser convertido
                    bytes_texto = texto.encode('utf-8')
                    base64_bytes = base64.b64encode(bytes_texto)
                    resultado = base64_bytes.decode('utf-8')
                    
                    print(f"\n🔐 \033[1;32mTexto Codificado (Base64):\033[0m")
                    print(f"\033[1;37m{resultado}\033[0m\n")
                except Exception as e:
                    print(f"❌ Erro na codificação: {e}")
                    
            elif acao in ["decode", "decodificar"]:
                try:
                    # Processo inverso: pega os bytes do Base64 e transforma em texto legível
                    base64_bytes = texto.encode('utf-8')
                    bytes_texto = base64.b64decode(base64_bytes)
                    resultado = bytes_texto.decode('utf-8')
                    
                    print(f"\n🔓 \033[1;36mTexto Decodificado:\033[0m")
                    print(f"\033[1;37m{resultado}\033[0m\n")
                except base64.binascii.Error:
                    print("❌ \033[1;31mErro:\033[0m O texto inserido não é um formato Base64 válido (falta de preenchimento ou caracteres incorretos).")
                except Exception as e:
                    print(f"❌ Erro na decodificação: {e}")
                    
            else:
                print("❌ Ação desconhecida. Use 'encode' ou 'decode'.")

# Comando password
        elif comando == "password":
            # Arquivos do nosso sistema de segurança
            arquivo_chave = os.path.join(FOLDER_DATAS, ".key_master.key")
            arquivo_cofre = os.path.join(FOLDER_DATAS, "safe_pyos.json")
            
            # 1. Sistema de Chave Mestra (Gera uma chave AES se você ainda não tiver uma)
            if not os.path.exists(arquivo_chave):
                chave_nova = Fernet.generate_key()
                with open(arquivo_chave, "wb") as f_chave:
                    f_chave.write(chave_nova)
            
            # Carrega a chave mestra para a memória do PyOS
            with open(arquivo_chave, "rb") as f_chave:
                chave = f_chave.read()
            
            motor_criptografia = Fernet(chave)
            
            # Se o usuário digitou apenas "senha", mostra o manual
            if not argumento:
                print("\n\033[1;31m========== 🔒 COFRE CRIPTOGRAFADO ==========\033[0m")
                print("Comandos de Segurança:")
                print("  \033[1;33mpassword generate\033[0m                : Cria uma senha inquebrável de 16 caracteres")
                print("  \033[1;33mpassword save [serviço] [senha]\033[0m  : Criptografa e guarda uma senha")
                print("  \033[1;33mpassword read\033[0m                    : Destranca o cofre e mostra as suas senhas")
                print("  \033[1;33mpassword delete [serviço]\033[0m        : Remove uma senha do cofre para sempre")
                print("\033[1;31m============================================\033[0m\n")
                continue
                
            # Divide o argumento. O "2" garante que a senha não seja cortada se tiver espaços!
            partes = argumento.split(" ", 2)
            acao = partes[0].lower()
            
            if acao == "generate":
                # Mistura letras maiúsculas, minúsculas, números e símbolos difíceis
                caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*_-=+"
                senha_forte = "".join(random.choice(caracteres) for _ in range(16))
                
                print(f"\n🛡️ \033[1;32mNova Senha Gerada:\033[0m \033[1;37m{senha_forte}\033[0m")
                print("DICA: Use 'password save [serviço] [senha]' para salvá-la no cofre!\n")
                
            elif acao == "save":
                if len(partes) < 3:
                    print("❌ Erro de sintaxe. Use: password save [nome_do_site] [sua_senha]")
                else:
                    servico = partes[1].capitalize()
                    senha_plana = partes[2]
                    
                    # A MÁGICA: Transforma a senha numa hash ilegível
                    senha_criptografada = motor_criptografia.encrypt(senha_plana.encode()).decode()
                    
                    # Carrega o cofre atual (se existir)
                    cofre = {}
                    if os.path.exists(arquivo_cofre):
                        try:
                            with open(arquivo_cofre, "r", encoding="utf-8") as f:
                                cofre = json.load(f)
                        except Exception:
                            pass
                            
                    # Guarda a versão criptografada e salva no disco
                    cofre[servico] = senha_criptografada
                    
                    with open(arquivo_cofre, "w", encoding="utf-8") as f:
                        json.dump(cofre, f, indent=4)
                        
                    print(f"🔒 \033[1;32mSucesso!\033[0m A senha do serviço '\033[1;33m{servico}\033[0m' foi criptografada e trancada no cofre.")

            elif acao in ["read", "list"]:
                if not os.path.exists(arquivo_cofre):
                    print("📭 O seu cofre está vazio. Use 'password save' primeiro.")
                else:
                    try:
                        with open(arquivo_cofre, "r", encoding="utf-8") as f:
                            cofre = json.load(f)
                            
                        print("\n\033[1;31m========== 🔓 COFRE ABERTO ==========\033[0m")
                        if not cofre:
                            print("O cofre não tem senhas salvas.")
                        else:
                            for servico, senha_cifra in cofre.items():
                                # A MÁGICA REVERSA: Destranca a senha usando a Chave Mestra
                                senha_revelada = motor_criptografia.decrypt(senha_cifra.encode()).decode()
                                print(f" 🔑 \033[1;33m{servico}:\033[0m {senha_revelada}")
                        print("\033[1;31m=====================================\033[0m\n")
                    except Exception as e:
                        print(f"❌ Erro crítico ao destrancar o cofre. A chave mestra foi alterada? Erro: {e}")
            
            elif acao in ["delete", "deletar", "remover"]:
                if len(partes) < 2:
                    print("❌ Erro de sintaxe. Use: password delete [nome_do_serviço]")
                else:
                    servico = partes[1].capitalize()
                    
                    if os.path.exists(arquivo_cofre):
                        try:
                            with open(arquivo_cofre, "r", encoding="utf-8") as f:
                                cofre = json.load(f)
                                
                            # Verifica se o serviço existe mesmo no cofre
                            if servico in cofre:
                                del cofre[servico] # Apaga do dicionário
                                
                                # Salva o cofre atualizado de volta no disco
                                with open(arquivo_cofre, "w", encoding="utf-8") as f:
                                    json.dump(cofre, f, indent=4)
                                    
                                print(f"🗑️ \033[1;31mDestruído:\033[0m A senha de '\033[1;33m{servico}\033[0m' foi apagada permanentemente do cofre.")
                            else:
                                print(f"❌ O serviço '{servico}' não foi encontrado nas suas anotações.")
                                
                        except Exception as e:
                            print(f"Erro ao acessar o cofre: {e}")
                    else:
                        print("📭 O seu cofre já está vazio ou ainda não foi criado.")
            else:
                print("❌ Comando de cofre não reconhecido. Digite apenas 'password' para ajuda.")

# Comando txt_read
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
                print("Por favor, digite o nome do arquivo. Exemplo: 'txt_read notas.txt'")
                
# Comando txt_write
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
                print("Por favor, digite o nome do arquivo. Exemplo: 'txt_write notas.txt'")

# Comando txt_edit
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
                    print(f"Erro: '{argumento}' não foi encontrado. Se quiser criar um novo, use o comando 'txt_write'.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: 'txt_edit notas.txt'")

# Comando csv_write
        elif comando == "csv_write":
            if argumento:
                # Garante que o arquivo tenha a extensão correta
                if not argumento.endswith('.csv'):
                    argumento += '.csv'
                    
                if os.path.exists(argumento):
                    print(f"Erro: O arquivo '{argumento}' já existe. Use 'csv_add' para inserir dados.")
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
                print("Por favor, digite o nome da planilha. Exemplo: csv_write clientes.csv")

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
                    print(f"Erro: Planilha '{argumento}' não encontrada. Crie primeiro com 'csv_write'.")
            else:
                print("Por favor, digite o nome da planilha. Exemplo: cdv_add clientes.csv")

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
                print("Por favor, digite o nome da planilha. Exemplo: csv_read clientes.csv")

# Comando open_image
        elif comando == "open_image":
            if argumento:
                if os.path.exists(argumento):
                    try:
                        # 1. Abre a imagem e converte para o formato RGB padrão
                        from PIL import Image
                        img = Image.open(argumento)
                        img = img.convert("RGB")
                        
                        # 2. Define a largura máxima (em "pixels/caracteres") para caber no terminal
                        largura_max = 60 
                        
                        # 3. Calcula a nova altura mantendo a proporção da imagem.
                        # Multiplicamos por 0.5 porque os caracteres do terminal são 2x mais altos que largos!
                        proporcao = (img.height / img.width)
                        altura_nova = int(largura_max * proporcao * 0.5)
                        
                        # 4. Encolhe a imagem
                        img = img.resize((largura_max, altura_nova))
                        
                        print(f"\n--- Exibindo: {argumento} ---")
                        
                        # 5. Varre a imagem linha por linha, pixel por pixel
                        for y in range(altura_nova):
                            linha_terminal = ""
                            for x in range(largura_max):
                                r, g, b = img.getpixel((x, y))
                                
                                # A MÁGICA: Código ANSI True Color para pintar o fundo do texto com o RGB do pixel
                                # Colocamos dois espaços em branco '  ' para formar o bloco e depois o '\033[0m' para resetar a cor
                                linha_terminal += f"\033[48;2;{r};{g};{b}m  \033[0m"
                                
                            print(linha_terminal) # Imprime a linha inteira da imagem
                            
                        print("-" * (largura_max * 2))
                        
                    except Exception as e:
                        print(f"Erro ao processar a imagem. Tem certeza de que é um arquivo de imagem válido? Erro: {e}")
                else:
                    print(f"Erro: O arquivo '{argumento}' não foi encontrado.")
            else:
                print("Por favor, digite o nome da imagem. Exemplo: open_image logo.png")

# Comando audio
        elif comando == "audio":
            if argumento:
                # Inicializa o motor de áudio apenas quando for usado pela primeira vez
                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                acao = argumento.strip().lower()

                if acao == "pause":
                    pygame.mixer.music.pause()
                    print("⏸️ Música em pausa.")
                elif acao == "continue" or acao == "play":
                    pygame.mixer.music.unpause()
                    print("▶️ Música retomada.")
                elif acao == "stop":
                    pygame.mixer.music.stop()
                    print("⏹️ Música parada.")
                else:
                    # Se não for nenhum comando de controlo, assume que é o nome do ficheiro
                    if os.path.exists(argumento):
                        try:
                            pygame.mixer.music.load(argumento)
                            # O -1 faz com que a música fique em loop infinito
                            pygame.mixer.music.play(-1)
                            print(f"🎵 A tocar agora: {argumento} (em segundo plano)")
                            print("DICA: Use 'audio pause' ou 'audio stop' para controlar o áudio.")
                        except Exception as e:
                            print(f"Erro ao tentar reproduzir o ficheiro. Certifique-se de que é um .mp3 ou .wav válido. Erro: {e}")
                    else:
                        print(f"Erro: O ficheiro '{argumento}' não foi encontrado.")
            else:
                print("Por favor, digite o nome da música ou o comando. Ex: audio lofi.mp3")

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

# Comando scan
        elif comando == "scan":
            import socket
            import threading
            
            print(f"\n\033[1;36m========== 📡 RADAR DE REDE LOCAL ==========\033[0m")
            print("Iniciando varredura tática (Ping Sweep)...")
            
            # 1. Descobre qual é o SEU IP atual na rede
            meu_ip = "127.0.0.1"
            try:
                # Tenta conectar no Google rapidinho só para o seu roteador te dar a sua "identidade"
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                meu_ip = s.getsockname()[0]
                s.close()
            except Exception:
                print("❌ Não foi possível identificar a rede. Você está conectado ao Wi-Fi/Cabo?")
                continue
                
            # Extrai a base da rede (ex: de "192.168.0.15" vira "192.168.0.")
            base_ip = '.'.join(meu_ip.split('.')[:-1]) + '.'
            print(f"Sua Sub-rede: \033[1;33m{base_ip}0/24\033[0m")
            print("Disparando 254 pacotes paralelos. Aguarde...\n")
            
            aparelhos_ativos = []
            threads = []
            
            # 2. A função que cada thread vai executar (pingar um único IP)
            def pingar_alvo(ip):
                # O comando muda se for Windows (win32) ou Linux/Mac
                if sys.platform == "win32":
                    # -n 1 (manda 1 pacote) | -w 500 (espera meio segundo) | > nul (esconde o texto feio do sistema)
                    cmd = f"ping -n 1 -w 500 {ip} > nul 2>&1"
                else:
                    # -c 1 (1 pacote) | -W 1 (espera 1 segundo) | > /dev/null (esconde o texto)
                    cmd = f"ping -c 1 -W 1 {ip} > /dev/null 2>&1"
                
                resposta = os.system(cmd)
                
                # Se a resposta for 0, significa que o alvo recebeu o pacote e respondeu!
                if resposta == 0:
                    aparelhos_ativos.append(ip)

            # 3. Dispara as 254 threads de uma vez
            for i in range(1, 255):
                ip_alvo = f"{base_ip}{i}"
                t = threading.Thread(target=pingar_alvo, args=(ip_alvo,))
                threads.append(t)
                t.start()
                
            # 4. Espera todos os radares voltarem com as respostas
            for t in threads:
                t.join()
                
            # 5. Imprime o relatório final e organiza os IPs em ordem numérica
            aparelhos_ativos.sort(key=lambda ip: int(ip.split('.')[-1]))
            
            print(f"🎯 \033[1;32mVarredura Concluída!\033[0m Encontrados \033[1;37m{len(aparelhos_ativos)}\033[0m dispositivos ativos:")
            for ativo in aparelhos_ativos:
                if ativo == meu_ip:
                    print(f"   💻 \033[1;36m{ativo}\033[0m (Este Computador)")
                elif ativo == f"{base_ip}1":
                    print(f"   🌐 \033[1;33m{ativo}\033[0m (Provável Roteador)")
                else:
                    print(f"   📱 \033[1;37m{ativo}\033[0m (Dispositivo Desconhecido)")
                    
            print(f"\033[1;36m============================================\033[0m\n")

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

# Comando self-destruct
        elif comando == "self-destruct":
            import time
            import tempfile
            
            print("\n\033[1;41m\033[1;37m !!! ALERTA DE SEGURANÇA MÁXIMA !!! \033[0m")
            print("\033[1;31mVocê iniciou o Protocolo de Autodestruição Total.\033[0m")
            print("Isso apagará o seu Banco de Dados, Senhas e \033[1;33mTODO O CÓDIGO-FONTE DO PyOS\033[0m.")
            print("NÃO HAVERÁ VOLTA. O SEU TRABALHO SERÁ PULVERIZADO.")
            
            confirmacao = input("\n\033[1;33mDigite o código 'OMEGA' para confirmar (ou Enter para cancelar): \033[0m")
            
            if confirmacao.strip().upper() == "OMEGA":
                print("\n\033[1;31m[!] CÓDIGO ACEITO. PROTOCOLO OMEGA INICIADO.\033[0m")
                
                for i in range(5, 0, -1):
                    sys.stdout.write(f"\r\033[1;31m[ INICIANDO LIMPEZA TOTAL EM {i} ... ]\033[0m")
                    sys.stdout.flush()
                    time.sleep(1)
                    
                print("\n\n\033[1;33mPREPARANDO CARGA EXPLOSIVA DO SISTEMA...\033[0m")
                time.sleep(1)
                
                # 1. Pega o caminho absoluto da pasta atual do seu projeto PyOS
                pasta_pyos = os.getcwd()
                
                # 2. O Truque: Cria um script .bat na pasta TEMP do Windows (bem longe daqui)
                caminho_bat = os.path.join(tempfile.gettempdir(), "apagar_pyos.bat")
                
                # Este script espera 2 segundos, apaga a sua pasta inteira (rmdir /s /q) e depois apaga-se a si mesmo
                conteudo_bat = f"""@echo off
                timeout /t 2 /nobreak > nul
                rmdir /s /q "{pasta_pyos}"
                del "%~f0"
                """
                # Salva o script fantasma
                with open(caminho_bat, "w", encoding="utf-8") as f:
                    f.write(conteudo_bat)
                    
                print("\n\033[1;31mADEUS.\033[0m")
                time.sleep(1)
                
                # 3. Executa o script fantasma de forma invisível e desvinculada do Python
                # CREATE_NO_WINDOW (0x08000000) impede que a tela preta do cmd apareça
                subprocess.Popen(["cmd.exe", "/c", caminho_bat], creationflags=0x08000000)
                
                # 4. Suicídio do processo: fecha o PyOS na mesma fração de segundo
                # Isso libera a pasta para que o script fantasma consiga apagá-la
                sys.exit(0)
                
            else:
                print("\n\033[1;32mProtocolo abortado. O código-fonte sobreviveu.\033[0m")

        else:
            print(f"Comando '{comando}' não reconhecido. Digite 'help' para ver a lista.")

if __name__ == "__main__":
    iniciar_pyos()
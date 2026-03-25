import os
import datetime
import sys
import shutil
import stat
import subprocess
import json
import time
import google.generativeai as genai

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
        "vermelho": "\033[31m", "verde": "\033[32m", "amarelo": "\033[33m",
        "azul": "\033[34m", "roxo": "\033[35m", "ciano": "\033[36m",
        "branco": "\033[37m", "restaurar": "\033[0m"
    }
    
    # Pega a cor salva do usuário (ou usa 'restaurar' se for a primeira vez)
    cor_salva = banco_cores.get(usuario, "restaurar")
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
            print("  help-config    : Exibe os comandos de configurações de usuários e outros")
            print("  quit           : Desliga o sistema")

        elif comando == "help-basics":
            print("\n--- Comandos Disponíveis ---")
            print("  help    : Mostra esta lista de comandos de ajuda")
            print("  logout  : Encerra a sessão atual e volta para a tela de login")
            print("  date    : Exibe a data e hora atuais")
            print("  ping    : Testa a conexão de rede com um site ou IP (ex: ping google.com)")
            print("  clear   : Limpa a tela do terminal")
            print("  list    : Lista os arquivos na pasta atual")
            print("  print   : Repete o que você digitar (ex: print olá mundo)")
            print("  calc    : Uma calculadora simples (ex: calc 5 + 5)")
            print("  ai      : Inicia uma conversa com a Inteligência Artificial (ex: ai)")

        elif comando == "help-archives":
            print("\n--- Comandos Disponíveis ---")
            print("  cd      : Navega entre as pastas (ex: cd nome_da_pasta ou cd .. para voltar)")
            print("  search  : Busca arquivos e pastas pelo nome (ex: search projeto)")
            print("  mkdir   : Cria uma nova pasta (ex: mkdir nova_pasta)")
            print("  rmdir   : Deleta uma pasta (ex: rmdir pasta_antiga)")
            print("  open    : Executa um arquivo com o programa padrão do seu computador (ex: open foto.jpg)")
            print("  delete  : Deleta um arquivo específico (ex: delete texto.txt)")
            print("  empty   : Apaga TODOS os arquivos de uma pasta de uma vez (ex: empty minha_pasta)")
            print("  disk    : Analisa o espaço de armazenamento do disco atual")
            print("  read    : Exibe o texto de um arquivo no terminal (ex: read notas.txt)")
            print("  write   : Cria/edita um arquivo de texto (ex: write notas.txt)")
            print("  edit    : Edita um arquivo de texto já existente (ex: edit notas.txt)")
            
        elif comando == "help-config":
            print("\n--- Comandos Disponíveis ---")
            print("  adduser : Adiciona um novo usuário ao sistema (ex: adduser maria)")
            print("  dltuser : Deleta um usuário do sistema (ex: deluser joao)")
            print("  color   : Muda a cor do terminal (ex: color verde, color restaurar)")
            
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
            if argumento:
                try:
                    # Avalia a expressão matemática simples. 
                    # Nota: eval() é perigoso em ambientes reais, mas ok para este simulador básico.
                    resultado = eval(argumento)
                    print(f"Resultado: {resultado}")
                except Exception:
                    print("Erro na expressão matemática. Tente algo como: calc 10 * 2")
            else:
                print("Por favor, digite uma conta. Exemplo: calc 5 + 5")

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
                # Usamos o modelo pro, que é o padrão universal e mais estável da API
                modelo = genai.GenerativeModel('gemini-pro')
                
                # Inicia o histórico de chat para a IA lembrar do contexto da conversa
                chat = modelo.start_chat(history=[])
                
                print("\nConexão estabelecida! Você está conversando com o Assistente PyOS.")
                print("DICA: Digite ':q' ou 'sair' para encerrar o chat e voltar ao sistema.")
                print("-" * 65)
                
                # Loop infinito do chat
                while True:
                    pergunta = input(f"\n[{usuario}] > ")
                    
                    if pergunta.strip().lower() in [':q', 'sair']:
                        print("Encerrando a conexão neural... Voltando ao PyOS.")
                        break
                    if not pergunta.strip():
                        continue
                        
                    print("[PyOS AI] Pensando...", end="\r")
                    
                    # Envia a pergunta para a IA e recebe a resposta
                    resposta = chat.send_message(pergunta)
                    
                    # Limpa a linha do "Pensando..." e imprime a resposta real
                    print(" " * 20, end="\r") 
                    print(f"[PyOS AI] {resposta.text}")
                    
            except Exception as e:
                print(f"\nErro de conexão com a IA: {e}")
                print("DICA: Se a sua chave estiver errada, delete o arquivo 'config_db.json' para resetar.")

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
                
# Comando read
        elif comando == "read":
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
        elif comando == "write":
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
        elif comando == "edit":
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
                print("Por favor, digite o nome do usuário que deseja deletar. Exemplo: deluser visitante")

# Comando color
        elif comando == "color":
            cores = {
                "vermelho": "\033[31m",
                "verde": "\033[32m",
                "amarelo": "\033[33m",
                "azul": "\033[34m",
                "roxo": "\033[35m",
                "ciano": "\033[36m",
                "branco": "\033[37m",
                "restaurar": "\033[0m"
            }
            
            if argumento:
                cor_escolhida = argumento.lower()
                
                if cor_escolhida in cores:
                    # Aplica a cor na tela
                    print(cores[cor_escolhida], end="")
                    
                    if cor_escolhida == "restaurar":
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
                    print(" -> vermelho, verde, amarelo, azul, roxo, ciano, branco, restaurar")
            else:
                print("Por favor, digite uma cor. Exemplo: 'color verde'")

        else:
            print(f"Comando '{comando}' não reconhecido. Digite 'help' para ver a lista.")

if __name__ == "__main__":
    iniciar_pyos()
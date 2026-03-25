import os
import datetime
import sys
import shutil
import stat
import subprocess
import json

def limpar_tela():
    # Limpa a tela dependendo do sistema operacional real do usuário
    os.system('cls' if os.name == 'nt' else 'clear')

def iniciar_pyos():
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

    limpar_tela()
    print("=================================================")
    print(f" Bem-vindo ao PyOS, {usuario}! ")
    print(" Digite 'ajuda' para ver os comandos disponíveis.")
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
            print("\n--- Comandos Disponíveis ---")
            print("  help    : Mostra esta lista de comandos")
            print("  date    : Exibe a data e hora atuais")
            print("  clear   : Limpa a tela do terminal")
            print("  list    : Lista os arquivos na pasta atual")
            print("  print   : Repete o que você digitar (ex: eco olá mundo)")
            print("  calc    : Uma calculadora simples (ex: calc 5 + 5)")
            print("  cd      : Navega entre as pastas (ex: cd nome_da_pasta ou cd .. para voltar)")
            print("  mkdir   : Cria uma nova pasta (ex: mkdir nova_pasta)")
            print("  rmdir   : Deleta uma pasta (ex: rmdir pasta_antiga)")
            print("  open    : Executa um arquivo com o programa padrão do seu computador (ex: abrir foto.jpg)")
            print("  empty   : Apaga TODOS os arquivos de uma pasta de uma vez (ex: empty minha_pasta)")
            print("  disc    : Analisa o espaço de armazenamento do disco atual")
            print("  read    : Exibe o texto de um arquivo no terminal (ex: ler notas.txt)")
            print("  write   : Cria/edita um arquivo de texto (ex: escrever notas.txt)")
            print("  edit    : Edita um arquivo de texto já existente (ex: editar notas.txt)")
            print("  quit    : Desliga o sistema")
            
        elif comando == "date":
            agora = datetime.datetime.now()
            print(f"Data e hora do sistema: {agora.strftime('%d/%m/%Y %H:%M:%S')}")
            
        elif comando == "clear":
            limpar_tela()
            
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
                
        elif comando == "print":
            print(argumento)
            
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
                print("Por favor, digite o nome da pasta. Exemplo: cd Documentos (ou 'cd ..' para voltar)")
                
        elif comando == "disc":
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
                
        elif comando == "mkdir":
            if argumento:
                try:
                    local_especifico = r"C:\ "
                    caminho_completo = os.path.join(local_especifico, argumento)
                    os.mkdir(argumento)
                    print(f"Pasta '{argumento}' criada com sucesso!")
                except FileExistsError:
                    print(f"Erro: A pasta '{argumento}' já existe.")
                except Exception as e:
                    print(f"Erro ao criar a pasta: {e}")
            else:
                print("Por favor, digite o nome da pasta. Exemplo: mkdir arquivos_importantes")
                
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
                print("Por favor, digite o nome da pasta. Exemplo: rmdir pasta_antiga")
                
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
                print("Por favor, digite o nome do arquivo. Exemplo: abrir documento.pdf")

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
                print("Por favor, digite o nome da pasta. Exemplo: esvaziar arquivos_velhos")
                
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
                print("Por favor, digite o nome do arquivo. Exemplo: ler notas.txt")
                
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
                print("Por favor, digite o nome do arquivo. Exemplo: escrever notas.txt")

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
                    print(f"Erro: '{argumento}' não foi encontrado. Se quiser criar um novo, use o comando 'escrever'.")
            else:
                print("Por favor, digite o nome do arquivo. Exemplo: editar notas.txt")
                
        else:
            print(f"Comando '{comando}' não reconhecido. Digite 'ajuda' para ver a lista.")

if __name__ == "__main__":
    iniciar_pyos()
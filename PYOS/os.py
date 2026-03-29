# ==========================================
# Native Python modules (already installed)
# ==========================================
import os, sys, shutil, stat, subprocess, time, datetime, threading
import json, csv, math, random, re, textwrap, unicodedata
import socket, socketserver, http.server
import urllib.request, urllib.parse, xml.etree.ElementTree as ET
import base64, hashlib

# ==========================================
# THIRD-PARTY MODULES (Installed via PIP)
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

def clear_screen():
    # Clears the screen depending on the user's actual operating system.
    os.system('cls' if os.name == 'nt' else 'clear')

def start_pyos():
    os.system('')
    clear_screen()
    
    # --- PREPARE THE DATABASE ---
    FOLDER_DATAS = "database"
    if not os.path.exists(FOLDER_DATAS):
        os.makedirs(FOLDER_DATAS)
    # --------------------------------------

    # --- Password-based login system and database. ---
    archive_db = os.path.join(FOLDER_DATAS, "users_db.json")
    
    # 1. Loads the database if it exists; otherwise, creates an empty list (dictionary).
    if os.path.exists(archive_db):
        with open(archive_db, 'r', encoding='utf-8') as f:
            database_users = json.load(f)
    else:
        database_users = {}

    print("Starting PyOS...")
    user = ""
    while not user:
        user = input("Login (Enter your username): ").strip()
        
    # 2. Checks if the user already exists in our database.
    if user in database_users:
        correct_password = database_users[user]
        entered_password = ""
        
        # It loops until the user guesses the correct password.
        while entered_password != correct_password:
            entered_password = input("Password: ")
            if entered_password != correct_password:
                print("Wrong password. Try again.")
    else:
        # 3. If it doesn't exist, create a new account and save it in the JSON file.
        print(f"\nUser '{user}' not found. Creating a new account...")
        new_password = input("Create a password for your user: ")
        database_users[user] = new_password
        
        # Save the update to the file.
        with open(archive_db, 'w', encoding='utf-8') as f:
            json.dump(database_users, f, indent=4)
        print("Account created successfully! Logging into the system...")
    # ---------------------------------------------------------------

    clear_screen()
    print("=================================================")
    print(f" Welcome to PyOS, {user}! ")
    print(" Project created by \033[1;31mCAFOX-E\033[0m with care.")
    print(" Type 'help' to see the available commands.")
    print("=================================================")

    while True:
        # Our system's command prompt
        entrance = input(f"\n{user}@PyOS> ").strip()
        
        if not entrance:
            continue
            
        # Separates the command from the arguments (e.g., 'echo hello' -> command='echo', argument='hello')
        parts = entrance.split(" ", 1)
        comand = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        # Logic of the commands
        if comand == "quit":
            print("Shutting down PyOS... See you later!")
            sys.exit()
            
        elif comand == "help":
            print("\n--- Help Commands ---")
            print("  help-basics    : Displays the program's basic commands")
            print("  help-web       : Displays the basic commands for web use")
            print("  help-archives  : Displays the file exploration commands")
            print("  help-office    : Displays commands for creating and editing text files and spreadsheets")
            print("  help-config    : Displays user settings commands and others")
            print("  quit           : Turn off the system")
            print("  \033[1;31mself-destruct\033[0m  : Initiates the Omega Protocol (Erases all data and shuts down PyOS)")

        elif comand == "help-basics":
            print("\n--- Available Commands ---")
            print("  help           : Shows a list of help commands")
            print("  logout         : Ends the current session and returns you to the login screen")
            print("  date           : Displays the current date and time")
            print("  time           : Displays the weather forecast in ASCII art (e.g., time, or time lisboa)")
            print("  ping           : Tests the network connection to a website or IP address (e.g., ping google.com)")
            print("  clear          : Clear the terminal screen")
            print("  rmnder         : Set a talking alarm in minutes (e.g., rmnder 1 Take out the pizza)")
            print("  print          : Repeat what you type (e.g., print Hello World!)")
            print("  speak          : Makes the system read a text aloud (e.g., speak Hello World!)")
            print("  calc           : A simple calculator (e.g., calc 5 + 5)")
            print("  play           : Open the PyOS mini-game menu to relax")
            print("  task           : Manage your daily tasks (e.g., task add, task read, task ok)")
            print("  banner         : Generates a giant ASCII art sign (e.g., PyOS banner)")
            print("  listen         : Open a port on your network and wait for a secret connection")
            print("  conect         : Connect to a PyOS radio that is listening (e.g., connect to 192.168.0.15)")

        elif comand == "help-web":
            print("\n--- Available Commands ---")
            print("  news           : Displays the top 5 headlines of the moment")
            print("  price          : Shows the value of the Dollar, Euro, and Bitcoin in Reais (e.g., price or price btc)")
            print("  browse         : Read text from a website directly in the terminal (e.g., browse pt.wikipedia.org/wiki/Linux)")
            print("  track          : Triangulates the geographic location of an IP address or website (e.g., track google.com)")
            print("  wiki           : Consult the Wikipedia Oracle on any subject (e.g., wiki Black hole)")
            print("  translate      : Translates text between languages (e.g., translate En-pt Hello world")
            print("  server         : Start the sharing (e.g., server web OR server ftp)")
            print("  ai             : Start a conversation with Artificial Intelligence (e.g., ai)")

        elif comand == "help-archives":
            print("\n--- Available Commands ---")
            print("  list           : Lists the files in the current folder")
            print("  cd             : Navigate between folders (e.g., cd folder_name or cd .. to go back)")
            print("  search         : Search for files and folders by name (e.g., search project)")
            print("  mkdir          : Creates a new folder (e.g., mkdir new_folder)")
            print("  rmdir          : Deletes a folder (e.g., rmdir old_folder)")
            print("  tree           : Draws a visual map of files and folders (e.g., tree or tree database)")
            print("  open           : Open a file using your computer's default program (e.g., open photo.jpg)")
            print("  delete         : Deletes a specific file (e.g., delete text.txt)")
            print("  empty          : Delete ALL files from a folder at once (e.g., empty my_folder)")
            print("  lock           : Encrypts a file with a password (e.g., lock secret.txt)")
            print("  unlock         : Decrypts a locked file (e.g., unlock secret.txt.lock)")
            print("  hide           : Hides secret text within the pixels of an image (e.g., hide photo.png The password is 123)")
            print("  reveal         : Extracts the hidden secret message in an image (e.g., reveal photo.png)")
            print("  base64         : Encodes or decodes texts in Base64 format (e.g. base64 encodes text)")
            print("  password       : Encrypted password vault (e.g., password generate, password save, password read)")
            
        elif comand == "help-office":
            print("\n--- Available Commands ---")
            print("  txt_read       : Displays the text from a file in the terminal (e.g., txt_read notes.txt)")
            print("  txt_write      : Creates a text file (e.g., txt_write notes.txt)")
            print("  txt_edit       : Edits an existing text file (e.g., txt_edit notes.txt)")
            print("  csv_write      : Creates a new spreadsheet (e.g., csv_write data.csv)")
            print("  csv_add        : Adds a row of data to the spreadsheet (e.g., csv_add data.csv)")
            print("  csv_read       : Reads and displays a spreadsheet in table format (e.g., csv_read data.csv)")
            print("  open_image     : Opens and draws an image directly in the terminal (e.g., open_image photo.jpg)")
            print("  audio          : Background music player (e.g., audio music.mp3, audio pause, audio stop)")

        elif comand == "help-config":
            print("\n--- Comandos Disponíveis ---")
            print("  disk           : Analyzes the current disk storage space")
            print("  status         : Shows real-time CPU, RAM, and battery usage")
            print("  devices        : Lists the connected network adapters and USB devices")
            print("  scan           : Map your local Wi-Fi network and list connected devices")
            print("  adduser        : Adds a new user to the system (e.g., adduser mary)")
            print("  dltuser        : Deletes a user from the system (e.g., dltuser john)")
            
# Comand logout
        elif comand == "logout":
            print(f"\nClosing the session of '{user}'...")
            
            # Restores the color to the default (white/gray) before returning to the home screen.
            print("\033[0m", end="")
            
            # Wait a second to give a more realistic feeling of the system shutting down.
            import time
            time.sleep(1)
            
            # It calls the main function again, restarting the login cycle!
            return start_pyos()

# Comand date
        elif comand == "date":
            now = datetime.datetime.now()
            print(f"System date and time: {now.strftime('%d/%m/%Y %H:%M:%S')}")

# Comand time
        elif comand == "time":          
            print("\n--- PyOS Meteorological Satellite ---")
            print("Connecting to the space weather station... 🛰️\n")
            
            try:
                # If the user types a city (e.g., time new york), encode the spaces and accents.
                city = urllib.parse.quote(argument.strip()) if argument else ""
                
                # The '?0' at the end of the URL tells the server to send only the current weather (so as not to clutter the screen).
                url = f"https://wttr.in/{city}?0"
                
                # The Trick: We disguised Python as 'curl' (a root terminal command) 
                # to make the website return the ANSI colors instead of a normal HTML website.
                request = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
                
                with urllib.request.urlopen(request) as answer:
                    time_ascii = answer.read().decode('utf-8')
                    print(time_ascii)
                    
            except Exception as e:
                print(f"Error retrieving satellite reading: {e}")
                print("TIP: Check your internet connection.")

# Comand ping
        elif comand == "ping":
            if argument:
                print(f"\nFiring network pulses to '{argument}'...")
                print("Please wait for a response from the server...\n")
                
                try:
                    # Windows uses '-n' to set the number of packets. Mac/Linux use '-c'.
                    # Let's configure it to send 4 packets (so it doesn't keep running forever on Linux/Mac)
                    parameter = '-n' if sys.platform == 'win32' else '-c'
                    
                    # It assembles the exact command that the actual system needs.
                    ping_comand = ['ping', parameter, '4', argument]
                    
                    # Execute the command and display the result directly on the PyOS screen.
                    subprocess.call(ping_comand)
                    
                    print("\nConnection test completed.")
                except Exception as e:
                    print(f"Error accessing the network: {e}")
            else:
                print("Please enter a website or IP address. Example: ping google.com")
            
# Comand clear
        elif comand == "clear":
            clear_screen()

# Comand rmnder
        elif comand == "rmnder":
            # Checks if the user entered the time and message (e.g., "5 Take out the pizza")
            parts = argument.split(" ", 1)
            
            if len(parts) >= 2 and parts[0].replace('.', '', 1).isdigit():
                minutes = float(parts[0])
                message = parts[1]
                
                # This is the function that will run hidden in the system background.
                def start_timer(time_minutes, reminder_text, username):
                    import time
                    # Converts minutes to seconds and pauses the invisible thread.
                    time.sleep(time_minutes * 60)
                    
                    # When the time runs out, it "invades" the terminal to let you know.
                    print(f"\n\n⏰ [SYSTEM REMINDER]: {reminder_text.upper()}!")
                    # Reprints the terminal cursor to avoid cluttering your screen.
                    print(f"[{username}] > ", end="", flush=True)
                    
                    # Try speaking aloud using the PyOS voice engine.
                    try:
                        import pyttsx3
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 170)
                        engine.say(f"Attention, reminder: {reminder_text}")
                        engine.runAndWait()
                    except Exception:
                        pass

                # Prepare the "parallel dimension" (Thread) with our function.
                thread_alarm = threading.Thread(target=start_timer, args=(minutes, message, user))
                
                # The daemon=True setting causes the alarm to be automatically destroyed if you close PyOS.
                thread_alarm.daemon = True 
                
                # Press "play" on the invisible timer!
                thread_alarm.start()
                
                print(f"⏰ Reminder successfully set for {minutes} minute(s) from now")
                print("You can continue using the system normally!")
            else:
                print("Invalid format. Use: rmnder [minutes] [message]")
                print("Example: rmnder 2.5 Check the bread in the oven")

# Comand print
        elif comand == "print":
            print(argument)

# Comand speak
        elif comand == "speak":
            if argument:
                print(f"🗣️ PyOS says: {argument}")
                try:
                    # 1. Start the voice engine
                    engine = pyttsx3.init()
                    
                    # 2. Set the voice speed (optional, 150 to 200 is a good natural speed)
                    engine.setProperty('rate', 170)
                    
                    # 3. Make the system talk
                    engine.say(argument)
                    
                    # 4. Wait for the conversation to finish before releasing the terminal back to you
                    engine.runAndWait()
                    
                except Exception as e:
                    print(f"Error in the voice module: {e}")
                    print("TIP: Check if your computer's volume is turned on.")
            else:
                print("Please type what I should say. Example: speak Operating system successfully activated.")

# Comand calc
        elif comand == "calc":
            # We created a "safe dictionary" with the allowed mathematical functions.
            # This makes eval() much safer and more powerful!
            mathematical_functions = {
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, 
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e, "abs": abs
            }
            
            def resolve_account(expression):
                try:
                    # 1. Transform the word "of" into a multiplication (Ex: 50% of 100 becomes 50% * 100)
                    adjusted_expression = expression.replace(' of ', ' * ')
                    
                    # 2. Transforms the number with a percentage sign into a division symbol (e.g., 50% becomes 50/100)
                    # The 're.sub' function searches for numbers followed by % and performs the mathematically correct substitution.
                    adjusted_expression = re.sub(r'([0-9.]+)%', r'(\1/100)', adjusted_expression)
                    
                    result = eval(adjusted_expression, {"__builtins__": None}, mathematical_functions)
                    return result
                except ZeroDivisionError:
                    return "Error: Division by zero is not allowed."
                except Exception:
                    return "Syntax error. Please check the typed expression."

            # If the user typed the calculation directly into the line (e.g., calc 10 * 2)
            if argument:
                print(f"Result: {resolve_account(argument)}")
                
            # If the user typed only 'calc', we opened Interactive Mode.
            else:
                print("\n--- PyOS Scientific Calculator ---")
                print("Basic operators: + (addition), - (subtraction), * (multiplication), / (division), ** (exponentiation)")
                print("Advanced functions: sqrt(x), sin(x), cos(x), log(x), pi, e")
                print("TIP: Type ':q' or 'exit' to return to the system.")
                print("-" * 35)
                
                while True:
                    count = input("calc> ").strip().lower()
                    
                    if count in [':q', 'sair']:
                        print("Closing calculator...")
                        break
                    if not count:
                        continue
                        
                    result = resolve_account(count)
                    print(f" = {result}")

# Comand play
        elif comand == "play":
            while True:
                print("\n=== 🕹️ PyOS Game Room ===")
                print("1. Guess the Number")
                print("2. Rock, Paper, Scissors")
                print("3. Hangman")
                print("0. Leave games")
                print("================================")
                
                choice = input("Choose a game (0, 1, 2 or 3): ").strip()
                
                if choice == '0':
                    print("Leaving the arcade. Back to work!")
                    
                    # --- TEMPORARY FILE CLEANUP ---
                    dictionary_file = "dicionary_en.txt"
                    if os.path.exists(dictionary_file):
                        try:
                            os.remove(dictionary_file)
                            print("[System] Temporary dictionary deleted. Folder cleared!")
                        except Exception as e:
                            pass
                    # ---------------------------------------------
                    break
                    
                elif choice == '1':
                    print("\n--- Guess the Number ---")
                    secret_number = random.randint(1, 100)
                    attempts = 0
                    print("PyOS came up with a number between 1 and 100. Try to guess!")
                    
                    while True:
                        guess = input("Your guess (or ':q' to exit): ").strip()
                        if guess.lower() == ':q': break
                        if not guess.isdigit(): continue
                            
                        guess = int(guess)
                        attempts += 1
                        
                        if guess < secret_number: print("🔺 Higher!")
                        elif guess > secret_number: print("🔻 Lower!")
                        else:
                            print(f"🎉 Congratulations! You guessed {secret_number} perfectly with {attempts} attempt(s)!")
                            break
                            
                elif choice == '2':
                    print("\n--- Rock, Paper, Scissors ---")
                    options = ["rock", "paper", "scissors"]
                    
                    while True:
                        play = input("Choose: rock, paper, scissors (or ':q' to exit): ").strip().lower()
                        if play == ':q': break
                        if play not in options: continue
                            
                        pc_play = random.choice(options)
                        print(f"💻 The computer chose: {pc_play.upper()}")
                        
                        if play == pc_play: print("🤝 Draw!")
                        elif (play == 'rock' and pc_play == 'scissor') or \
                             (play == 'paper' and pc_play == 'rock') or \
                             (play == 'scissor' and pc_play == 'paper'):
                            print("🏆 You won this round!")
                        else: print("💀 You lost! The computer was smarter.")
                        
                # --- Hangman Game (Words with 5+ Letters) ---
                elif choice == '3':
                    print("\n--- Hangman ---")
                    
                    dictionary_file = "dicionario_en.txt"
                    # Emergency list updated with only longer words.
                    words = ["python", "computer", "keyboard", "internet", "criptography"] 
                    
                    # 1. Check if the dictionary has already been downloaded.
                    if not os.path.exists(dictionary_file):
                        print("Downloading the complete Portuguese dictionary (please wait a few seconds)...")
                        try:
                            url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
                            urllib.request.urlretrieve(url, dictionary_file)
                            print("Dictionary downloaded successfully!")
                        except Exception as e:
                            print(f"Error downloading: {e}. Using the emergency list.")
                    
                    # 2. Read the words from the file.
                    try:
                        if os.path.exists(dictionary_file):
                            with open(dictionary_file, 'r', encoding='utf-8') as f:
                                # Filter to use ONLY words with 5 or more letters!
                                words = [p.strip() for p in f.readlines() if len(p.strip()) >= 5]
                    except Exception:
                        pass
                        
                    # 3. Sort the word
                    original_word = random.choice(words).lower()
                    
                    # 4. Remove the accents from the words.
                    secret_word = "".join(c for c in unicodedata.normalize('NFD', original_word) if unicodedata.category(c) != 'Mn')
                    
                    discovered_letters = []
                    allowed_errors = 6
                    
                    print(f"TIP: The word has {len(secret_word)} letters!")
                    
                    while True:
                        hidden_word = ""
                        for letter in secret_word:
                            if letter in discovered_letters:
                                hidden_word += letter + " "
                            else:
                                hidden_word += "_ "
                                
                        print(f"\nWord: {hidden_word}")
                        print(f"Remaining attempts: {allowed_errors}")
                        
                        if "_" not in hidden_word:
                            print(f"🎉 Congratulations! You escaped the gallows! The word was {original_word.upper()}.")
                            break
                            
                        if allowed_errors == 0:
                            print(f"💀 Game over! You were hanged. The word was: {original_word.upper()}")
                            break
                            
                        typed_letter = input("Type a letter (or ':q' to exit): ").strip().lower()
                        
                        if typed_letter == ':q': break
                        if len(typed_letter) != 1 or not typed_letter.isalpha():
                            print("Please enter only one valid letter.")
                            continue
                            
                        # Remove the accent from the typed letter as well.
                        typed_letter = "".join(c for c in unicodedata.normalize('NFD', typed_letter) if unicodedata.category(c) != 'Mn')
                            
                        if typed_letter in discovered_letters:
                            print("You've already tried that letter! Try another one.")
                            continue
                            
                        discovered_letters.append(typed_letter)
                        
                        if typed_letter in secret_word:
                            print("✅ Great! You got one letter right.")
                        else:
                            print("❌ Oops! That letter doesn't exist in the word.")
                            allowed_errors -= 1
                else:
                    print("Invalid selection. Please try again.")

# Comand task
        elif comand == "task":
            
            # The file where PyOS will store its data
            task_file = os.path.join(FOLDER_DATAS, "tasks_pyos.json")
            
            # 1. Load existing tasks (if the file already exists).
            tasks = []
            if os.path.exists(task_file):
                try:
                    with open(task_file, 'r', encoding='utf-8') as f:
                        tasks = json.load(f)
                except Exception:
                    pass
            
            # If the user typed only "task", we display the user manual.
            if not argument:
                print("\n\033[1;36m========== 📋 TASK MANAGER ==========\033[0m")
                print("Available commands:")
                print("  \033[1;33mtask add [text]\033[0m : Add a new task")
                print("  \033[1;33mtask read\033[0m        : List all your tasks.")
                print("  \033[1;33mtask ok [number]\033[0m : Mark a task as completed.")
                print("  \033[1;33mtask del [number]\033[0m: Delete a task from the list.")
                print("\033[1;36m===============================================\033[0m\n")
                continue # Return to the beginning of the loop without error.

            # Divide what the user typed (e.g., "add" and "Study Python")
            parts = argument.split(" ", 1)
            action = parts[0].lower()
            detail = parts[1] if len(parts) > 1 else ""

            # --- CRUD LOGIC (Create, Read, Update, Delete) ---
            if action == "add" and detail:
                tasks.append({"text": detail, "completed": False})
                print(f"✅ \033[1;32mTask added to the database:\033[0m {detail}")
            
            elif action in ["read", "list"]:
                print("\n\033[1;36m========== 📋 YOUR TASKS ==========\033[0m")
                if not tasks:
                    print("No tasks left to do. You are free! 🎮")
                else:
                    for i, t in enumerate(tasks):
                        # Paint the [X] green and the [ ] red.
                        status = "\033[1;32m[X]\033[0m" if t["completed"] else "\033[1;31m[ ]\033[0m"
                        # Strikethrough text if complete using special ANSI code (\033[9m)
                        text = f"\033[9m{t['text']}\033[0m" if t["completed"] else t['text']
                        print(f" {i+1}. {status} {text}")
                print("\033[1;36m========================================\033[0m\n")
            
            elif action == "ok" and detail.isdigit():
                idx = int(detail) - 1
                if 0 <= idx < len(tasks):
                    tasks[idx]["completed"] = True
                    print(f"🎉 \033[1;32mTask {idx+1} completed!\033[0m Excelent work.")
                else:
                    print("❌ Invalid task number.")
                    
            elif action == "del" and detail.isdigit():
                idx = int(detail) - 1
                if 0 <= idx < len(tasks):
                    removed = tasks.pop(idx)
                    print(f"🗑️ \033[1;31mTask deleted:\033[0m {removed['text']}")
                else:
                    print("❌ Invalid task number.")
            else:
                print("❌ The task command is not recognized. Just type 'task' for help.")

            # 2. Saves the changes back to the hard drive.
            try:
                with open(task_file, 'w', encoding='utf-8') as f:
                    json.dump(tasks, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Critical error while saving tasks: {e}")

# Comand banner
        elif comand == "banner":
            if not argument:
                print("\n\033[1;36m========== 🎨 BANNER GENERATOR ==========\033[0m")
                print("❌ Correct usage: banner [text]")
                print("Example: banner Hacked System")
                print("\033[1;36m===========================================\033[0m\n")
            else:
                try:
                    import pyfiglet
                    
                    # Use the 'slant' font for a slanted, modern look.
                    # Setting width=100 ensures that the text won't break as easily if the screen is small.
                    banner_ascii = pyfiglet.figlet_format(argument, font="slant", width=100)
                    
                    # Print the banner in Brilliant Cyan
                    print(f"\n\033[1;36m{banner_ascii}\033[0m")
                    
                except ImportError:
                    print("❌ Library missing. Open a normal command prompt (CMD) and type: pip install pyfiglet")
                except pyfiglet.FontNotFound:
                    print("❌ The ASCII font was not found by the system.")
                except Exception as e:
                    print(f"❌ Error generating the sign: {e}")

# Comand listen
        elif comand == "listen":
            import socket
            import threading
            from datetime import datetime
            
            print("\n\033[1;35m========== 📻 GHOST RADIO (SERVER) ==========\033[0m")
            
            archive_log = os.path.join(FOLDER_DATAS, "interceptations_radio.log")
            
            # Invisible function that logs everything to the log file.
            def record_log(sender, message):
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                try:
                    with open(archive_log, "a", encoding="utf-8") as f:
                        f.write(f"[{now}] {sender}: {message}\n")
                except:
                    pass
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                my_ip = s.getsockname()[0]
            except:
                my_ip = "127.0.0.1"
            finally:
                s.close()
                
            secret_door = 9999
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                server.bind(("0.0.0.0", secret_door))
                server.listen(1)
                
                print(f"📡 Radio tower erected! Frequency: \033[1;33m{secret_door}\033[0m")
                print(f"Tell your partner to type: \033[1;36mconect {my_ip}\033[0m")
                print("Awaiting infiltration...\n")
                
                conection, address = server.accept()
                
                print(f"✅ \033[1;32mConnection established with the Agent {address[0]}!\033[0m")
                print("Point-to-point chat initiated. Everything is being recorded in the logs.")
                print("\033[1;35m==================================================\033[0m\n")
                
                # This marks the beginning of the conversation in the log.
                record_log("SISTEM", f"=== CONNECTION INITIATED WITH {address[0]} ===")
                
                active_chat = [True]
                
                def receive_messages(conn):
                    while active_chat[0]:
                        try:
                            msg = conn.recv(1024).decode('utf-8')
                            if not msg or msg.lower() == 'sair':
                                print("\n❌ \033[1;31mThe partner cut the line.\033[0m Press Enter to go back.")
                                record_log("SISTEM", "=== THE PARTNER DISCONNECTED ===")
                                active_chat[0] = False
                                break
                            
                            # Print to the screen and save to an invisible file!
                            print(f"\n\033[1;36m[Partner]:\033[0m \033[1;37m{msg}\033[0m")
                            record_log(address[0], msg)
                        except:
                            break
                            
                threading.Thread(target=receive_messages, args=(conection,), daemon=True).start()
                
                while active_chat[0]:
                    try:
                        text = input()
                        if not active_chat[0]: break
                        
                        if text.lower() == 'sair':
                            conection.send("sair".encode('utf-8'))
                            active_chat[0] = False
                            record_log("SISTEM", "=== YOU ENDED THE CONNECTION ===")
                            print("Turning off transmitters...")
                            break
                            
                        if text.strip():
                            sys.stdout.write("\033[F\033[K")
                            print(f"\033[1;32m[You]:\033[0m \033[1;37m{text}\033[0m")
                            # Record your message and send it to your partner.
                            record_log(my_ip, text)
                            conection.send(text.encode('utf-8'))
                    except:
                        break
                        
                conection.close()
                server.close()
            except Exception as e:
                print(f"❌ Transmitter failure: {e}")

# Comand conect
        elif comand == "conect":
            import socket
            import threading
            from datetime import datetime
            
            if not argument:
                print("\n\033[1;35m========== 📻 GHOST RADIO ==========\033[0m")
                print("❌ Correct usage: connect to [TOWER_IP]")
                print("Example: connect to 192.168.0.15")
                print("\033[1;35m=======================================\033[0m\n")
                continue
                
            target_ip = argument.strip()
            secret_door = 9999
            
            archive_log = os.path.join(FOLDER_DATAS, "interceptations_radio.log")
            
            def record_log(sender, message):
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                try:
                    with open(archive_log, "a", encoding="utf-8") as f:
                        f.write(f"[{now}] {sender}: {message}\n")
                except:
                    pass
            
            print(f"\n\033[1;35m========== 📻 GHOST RADIO (INFILTRATOR) ==========\033[0m")
            print(f"Trying to tune to the IP frequency {target_ip}...")
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((target_ip, secret_door))
                
                print(f"✅ \033[1;32mSuccessful infiltration!\033[0m")
                print("Point-to-point chat initiated. Everything is being recorded in the logs.")
                print("\033[1;35m=====================================================\033[0m\n")
                
                record_log("SISTEM", f"=== YOU INFILTRATED THE IP {target_ip} ===")
                
                active_chat = [True]
                
                def receive_messages(conn):
                    while active_chat[0]:
                        try:
                            msg = conn.recv(1024).decode('utf-8')
                            if not msg or msg.lower() == 'sair':
                                print("\n❌ \033[1;31mThe tower shut down the transmission.\033[0m Press Enter to go back.")
                                record_log("SISTEM", "=== THE TOWER DISCONNECTED ===")
                                active_chat[0] = False
                                break
                            print(f"\n\033[1;36m[Partner]:\033[0m \033[1;37m{msg}\033[0m")
                            record_log(target_ip, msg)
                        except:
                            break
                            
                threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
                
                while active_chat[0]:
                    try:
                        text = input()
                        if not active_chat[0]: break
                        
                        if text.lower() == 'sair':
                            client.send("sair".encode('utf-8'))
                            active_chat[0] = False
                            record_log("SISTEM", "=== YOU CUT THE LINE ===")
                            print("Disconnecting from the tower...")
                            break
                            
                        if text.strip():
                            sys.stdout.write("\033[F\033[K")
                            print(f"\033[1;32m[You]:\033[0m \033[1;37m{text}\033[0m")
                            record_log("YOU", text)
                            client.send(text.encode('utf-8'))
                    except:
                        break
                        
                client.close()
            except ConnectionRefusedError:
                print(f"❌ \033[1;31mConnection Refused:\033[0m The IP address {target_ip} is not running the 'listen' command.")
            except Exception as e:
                print(f"❌ Connection error: {e}")

# Comand server
        elif comand == "server":
            if argument in ["web", "ftp"]:
                # Trick to get the local IP address
                try:
                    import socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    local_ip = s.getsockname()[0]
                    s.close()
                except Exception:
                    local_ip = "127.0.0.1"

                # --- OPTION 1: WEB SERVER (Browser) ---
                if argument == "web":
                    import http.server
                    import socketserver
                    PORT = 8000
                    Handler = http.server.SimpleHTTPRequestHandler
                    socketserver.TCPServer.allow_reuse_address = True
                    
                    try:
                        with socketserver.TCPServer(("", PORT), Handler) as httpd:
                            print(f"\n--- PyOS Web Server Started ---")
                            print(f"🔗 Access via browser: http://{local_ip}:{PORT}")
                            print("Press 'Ctrl + C' in the terminal to disconnect.")
                            httpd.serve_forever()
                    except KeyboardInterrupt:
                        print("\nWeb server successfully shut down.")
                    except Exception as e:
                        print(f"\nWeb server error: {e}")

                # --- OPTION 2: FTP SERVER (File Explorer) ---
                elif argument == "ftp":
                    try:
                        # Import the tools from pyftpdlib
                        from pyftpdlib.authorizers import DummyAuthorizer
                        from pyftpdlib.handlers import FTPHandler
                        from pyftpdlib.servers import FTPServer
                        
                        PORT_FTP = 2121
                        
                        # Configure permissions (read and write)
                        authorizer = DummyAuthorizer()
                        # 'elradfmw' means full permission: read, write, delete, create folders.
                        authorizer.add_anonymous(os.getcwd(), perm='elradfmw')
                        
                        handler = FTPHandler
                        handler.authorizer = authorizer
                        
                        # Turn off annoying FTP log messages to avoid cluttering your screen.
                        import logging
                        logging.getLogger("pyftpdlib").setLevel(logging.WARNING)
                        
                        server = FTPServer((local_ip, PORT_FTP), handler)
                        
                        print(f"\n--- PyOS FTP Server Started ---")
                        print(f"Shared folder: {os.getcwd()}")
                        print(f"Open File Explorer (Windows) and type in the address bar at the top:")
                        print(f"🔗 ftp://{local_ip}:{PORT_FTP}")
                        print("------------------------------------------")
                        print("Press 'Ctrl + C' in the terminal to disconnect.")
                        
                        server.serve_forever()
                        
                    except ImportError:
                        print("Error: The 'pyftpdlib' library is not installed.")
                        print("Open your PC's terminal and type: pip install pyftpdlib")
                    except KeyboardInterrupt:
                        print("\nFTP server successfully shut down. Returning to PyOS.")
                    except Exception as e:
                        print(f"\nFTP server error: {e}")
            else:
                print("Please choose the mode. Example: web server OR ftp server.")

# Comand ai
        elif comand == "ai":
            print("\n--- Initiating Neural Connection (PyOS AI) ---")
            
            archive_config = os.path.join(FOLDER_DATAS, "config_db.json")
            # Load the settings to see if we already have the API key.
            if os.path.exists(archive_config):
                with open(archive_config, 'r', encoding='utf-8') as f:
                    data_config = json.load(f)
            else:
                data_config = {}

            # Checks if the current user has already saved an API key.
            api_key = data_config.get(f"{user}_api_key", "")

            # If there is no key, it asks the user to type it in and saves it to the file.
            if not api_key:
                print("To use AI, you need a free Google AI Studio key.")
                print("Get yours at: https://aistudio.google.com/app/apikey")
                api_key = input("Paste your API Key here (or type 'log out' to cancel): ").strip()
                
                if api_key.lower() == 'leave':
                    continue
                
                # Saves the key associated with the user.
                data_config[f"{user}_api_key"] = api_key
                with open(archive_config, 'w', encoding='utf-8') as f:
                    json.dump(data_config, f, indent=4)
                print("Key successfully saved to your profile!")

            try:
                # Configure the AI ​​with the user's key.
                genai.configure(api_key=api_key)
                
                print("Looking for a compatible AI model on Google's servers...", end="\r")
                
                # --- AUTOMATIC MODEL SEARCH ---
                name_model = None
                for m in genai.list_models():
                    # Find the first template that supports text generation ('generateContent')
                    if 'generateContent' in m.supported_generation_methods:
                        name_model = m.name
                        # We will give preference to the newest models (1.5) if they exist.
                        if '1.5' in name_model:
                            break 
                            
                if not name_model:
                    print("Critical Error: No text template available for your account/key.")
                    continue
                    
                # Start the model that PyOS discovered on its own!
                model = genai.GenerativeModel(name_model)
                # ----------------------------------------
                
                # Clear the search bar
                print(" " * 60, end="\r")
                
                chat = model.start_chat(history=[])
                print(f"\nConnection established using the template: {name_model}")
                print("You are currently chatting with the PyOS Assistant. Type ':q' or 'exit' to return.")
                print("-" * 65)
                
                while True:
                    question = input(f"\n[{user}] > ")
                    
                    if question.strip().lower() in [':q', 'leave']:
                        print("Closing the neural connection... Back to PyOS.")
                        break
                    if not question.strip():
                        continue
                        
                    print("[PyOS AI] Thinking...", end="\r")
                    answer = chat.send_message(question)
                    print(" " * 20, end="\r") 
                    print(f"[PyOS AI] {answer.text}")
                    
            except Exception as e:
                print(f"\nConnection error with AI: {e}")
                print("TIP: If your key is invalid, open the 'config_db.json' file and delete the line containing your API key so the system will request a new one.")

# Comand news
        elif comand == "news":
            print("\n--- PyOS News Center ---")
            print("Connecting to information satellites... 📡\n")
            
            try:
                # We use Google News RSS, which focuses on the top news stories (in Portuguese).
                url = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"
                
                # We disguised PyOS as a normal browser so the server wouldn't block our connection.
                request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                # Download the XML file with the news.
                with urllib.request.urlopen(request) as answer:
                    datas_xml = answer.read()
                    
                # The magic of Python: It transforms XML text into a navigable data tree.
                source = ET.fromstring(datas_xml)
                
                # Search for all 'items' (which are the news items) within the RSS 'channel'.
                news_found = source.findall('./channel/item')
                
                if not news_found:
                    print("No news found at the moment.")
                else:
                    # Just grab the first 5 news items from the list.
                    for i, item in enumerate(news_found[:5], 1):
                        tittle = item.find('title').text
                        link = item.find('link').text
                        
                        # Imprime o título e o link formatados
                        print(f"{i}. 📰 {tittle}")
                        print(f"   🔗 {link}\n")
                        
                print("-" * 65)
                print("TIP: Hold down the 'Ctrl' key (or 'Cmd' on a Mac) and click the link to open it in your actual browser!")
                
            except Exception as e:
                print(f"Error searching for news: {e}")
                print("TIP: Check your internet connection.")

# Comand price
        elif comand == "price":
            print(f"\n\033[1;32m========== 📈 FINANCIAL DASHBOARD PyOS ==========\033[0m")
            print("Connecting to the Stock Exchange servers...\n")
            
            # Define which currency to search for (if you don't type anything, it shows all currencies).
            chosen_currency = argument.upper().strip() if argument else "ALL"
            
            try:
                # AwesomeAPI URL that provides real-time exchange rates for the BRL (Brazilian Real).
                url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
                request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(request) as answer:
                    # Reads the response from the internet and converts the JSON into a Python dictionary.
                    datas = json.loads(answer.read().decode('utf-8'))
                    
                # Internal function to format and print each coin nicely on the screen.
                def display_currency(acronym, name, currency_data):
                    value = float(currency_data['bid'])
                    variation = float(currency_data['pctChange'])
                    
                    # Define the color of the variation (Green for high, Red for low)
                    color_var = "\033[1;32m▲" if variation > 0 else "\033[1;31m▼"
                    
                    # Format the number to the Brazilian standard (R$ 5.12)
                    if acronym == "BTC":
                        # Bitcoin is a very high value, so we formatted it with a thousands separator.
                        value_str = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    else:
                        value_str = f"{value:.2f}".replace(".", ",")
                        
                    print(f"💰 \033[1;37m{name} ({acronym}):\033[0m R$ {value_str}  {color_var} {variation}%\033[0m")

                # Displays according to the user's request.
                if chosen_currency in ["USD", "ALL"]:
                    display_currency("USD", "Dólar Comercial", datas['USDBRL'])
                if chosen_currency in ["EUR", "ALL"]:
                    display_currency("EUR", "Euro          ", datas['EURBRL'])
                if chosen_currency in ["BTC", "ALL"]:
                    display_currency("BTC", "Bitcoin       ", datas['BTCBRL'])
                
                if chosen_currency not in ["USD", "EUR", "BTC", "TODAS"]:
                    print(f"❌ Currency '{chosen_currency}' not found in quick access.")
                    print("Try typing only: usd quote, eur quote or btc quote.")
                    
            except Exception as e:
                print(f"\033[1;31mError accessing financial data: {e}\033[0m")
                print("TIP: Check your internet connection or if the API is up and running.")
                
            print(f"\033[1;32m===============================================\033[0m\n")

# Comand browse
        elif comand == "browse":
            if argument:
                # \033[1;36m deixa o texto em Ciano Negrito, e \033[0m reseta a cor
                print(f"\n\033[1;36m========== 🌐 PyOS LYNX BROWSER ==========\033[0m")
                
                url = argument if argument.startswith('http') else 'http://' + argument
                print(f"\033[33mAccessing:\033[0m {url}\n") # \033[33m is Yellow
                
                try:
                    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    with urllib.request.urlopen(request) as answer:
                        html_brute = answer.read().decode('utf-8', errors='ignore')
                        
                    soup = BeautifulSoup(html_brute, 'html.parser')
                    
                    for garbage_element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
                        garbage_element.extract()
                        
                    clean_text = soup.get_text(separator='\n')
                    formatted_lines = [linha.strip() for linha in clean_text.splitlines() if linha.strip()]
                    
                    # --- The Magic of Text Formatting ---
                    displayed_lines = 0
                    limit_lines = 40 # We reduced the limit slightly to make the reading more focused.
                    
                    for line in formatted_lines:
                        if displayed_lines >= limite_linhas:
                            break
                            
                        # If the line is too short (like a leftover menu), we ignore it to keep the screen clean.
                        if len(line) < 15:
                            continue
                            
                        # The text wrap will "fold" the text so that it doesn't exceed 80 characters in width.
                        beautiful_paragraph = textwrap.fill(line, width=80)
                        
                        print(beautiful_paragraph)
                        print() # Print a blank line to separate paragraphs.
                        
                        # Count how many actual lines this paragraph occupied on the screen.
                        displayed_lines += beautiful_paragraph.count('\n') + 1 
                    # ---------------------------------------
                    
                    if len(formatted_lines) > limite_linhas:
                        print(f"\033[1;30m[... End of Reading Mode preview ...]\033[0m")
                        
                    print(f"\033[1;36m=============================================\033[0m\n")
                    
                except Exception as e:
                    print(f"\033[1;31mError loading page: {e}\033[0m") # Red for error
                    print("TIP: Check if the link is correct (e.g., pt.wikipedia.org).")
            else:
                print("Please enter the website link. Example: browse pt.wikipedia.org/wiki/Python")

# Comand list
        elif comand == "list":
            print(f"\nCurrent directory contents ({os.getcwd()}):")
            try:
                # Get all items (folders and files)
                items = os.listdir('.')
                
                # First, we show the folders.
                for item in items:
                    if os.path.isdir(item):
                        print(f" [FOLDER]   {item}")
                        
                # Next, we show the files.
                for item in items:
                    if os.path.isfile(item):
                        print(f" [ARCHIVE] {item}")
                        
                if not items:
                    print(" (The folder is empty)")
                    
            except Exception as e:
                print(f"Error reading directory: {e}")

# Comand track
        elif comand == "track":
            if argument:
                # \033[1;36m is the color Cyan (bright light blue)
                print(f"\n\033[1;36m========== 🌍 PyOS GLOBAL TRACKER ==========\033[0m")
                print(f"Triangulate the target: {argument}...\n")
                
                try:
                    # If the user types with "https://", we clear the code so the radar works properly.
                    target = argument.replace("https://", "").replace("http://", "").split("/")[0]
                    
                    # Free geolocation API (no key required)
                    url = f"http://ip-api.com/json/{target}"
                    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    with urllib.request.urlopen(request) as answer:
                        datas = json.loads(answer.read().decode('utf-8'))
                        
                    # Checks if the API successfully found the target.
                    if datas.get("status") == "success":
                        # Prints the formatted data in color (Yellow for labels).
                        print(f"📍 \033[1;33mIP Target:\033[0m      {datas.get('query')}")
                        print(f"🏙️ \033[1;33mCity:\033[0m       {datas.get('city')} - {datas.get('regionName')}")
                        print(f"🏳️ \033[1;33mCountry:\033[0m         {datas.get('country')} ({datas.get('countryCode')})")
                        print(f"🏢 \033[1;33mProvider:\033[0m     {datas.get('isp')}")
                        print(f"🗺️ \033[1;33mCoordinates:\033[0m  Lat {datas.get('lat')}, Lon {datas.get('lon')}")
                        print(f"🕒 \033[1;33mTime zone:\033[0m {datas.get('timezone')}")
                        
                        # Easter Egg: Direct link to the map
                        link_map = f"https://www.google.com/maps/search/?api=1&query={datas.get('lat')},{datas.get('lon')}"
                        print(f"\n🔗 \033[1;34mSatellite (Ctrl-click):\033[0m {link_map}")
                    else:
                        print(f"❌ \033[1;31mTriangulation failure:\033[0m Unable to locate '{target}'.")
                        
                except Exception as e:
                    print(f"\033[1;31mSatellite connection error: {e}\033[0m")
                    print("TIP: Check your internet connection.")
                    
                print(f"\033[1;36m===============================================\033[0m\n")
            else:
                print("Please enter an IP address or website. Example: track google.com or track 8.8.8.8")

# Comand wiki
        elif comand == "wiki":
            if argument:
                # Cor Azul Escuro/Anil (\033[1;34m) para combinar com a identidade da Wikipédia
                print(f"\n\033[1;34m========== 📚 WIKIPEDIA ORACLE ==========\033[0m")
                print(f"Consulting humanity's archives on: '{argument}'...\n")
                
                try:
                    # Prepare the name the user typed to become a valid link (e.g., "Black hole" becomes "Black%20hole")
                    search_term = urllib.parse.quote(argument.strip().capitalize())
                    
                    # The official Wikipedia API that returns only the Portuguese abstract.
                    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{search_term}"
                    
                    # Wikipedia requires a User-Agent to know who is accessing it.
                    request = urllib.request.Request(url, headers={'User-Agent': 'PyOS/1.0 (Terminal Hacking)'})
                    
                    with urllib.request.urlopen(request) as answer:
                        datas = json.loads(answer.read().decode('utf-8'))
                        
                    # If the API returned a summary (extract)
                    if 'extract' in datas:
                        resume = datas['extract']
                        
                        # Use the textwrap to format the text into 80 columns, making it look like a book.
                        paragraphs = textwrap.wrap(resume, width=80)
                        for line in paragraphs:
                            print(line)
                            
                        # Easter Egg: Here's the direct link in case you want to read the rest in your browser.
                        if 'content_urls' in datas and 'desktop' in datas['content_urls']:
                            complete_link = datas['content_urls']['desktop']['page']
                            print(f"\n🔗 \033[1;36mRead the full article at:\033[0m {complete_link}")
                    else:
                        print(f"❌ I couldn't find an exact summary for '{argument}'.")
                        
                except urllib.error.HTTPError as e:
                    # Error 404 means that the page does not exist on Wikipedia.
                    if e.code == 404:
                        print(f"❌ \033[1;31mArticle not found:\033[0m Wikipedia doesn't have an exact page with that name. '{argument}'.")
                        print("TIP: Try to be more specific or check your spelling (e.g., wiki Albert Einstein).")
                    else:
                        print(f"Error communicating with Wikipedia: {e}")
                except Exception as e:
                    print(f"\033[1;31mConnection error: {e}\033[0m")
                    
                print(f"\033[1;34m==========================================\033[0m\n")
            else:
                print("Please type what you want to search for. Example: wiki Artificial intelligence")

# Comand translate
        elif comand == "translate":
            if argument:
                parts = argument.split(" ", 1)
                
                if len(parts) >= 2 and "-" in parts[0]:
                    languages = parts[0].strip() 
                    text = parts[1].strip()
                    
                    try:
                        origin, destiny = languages.split("-", 1)
                        
                        print(f"\n\033[1;35m========== 🌐 GOOGLE TRANSLATOR ==========\033[0m")
                        print(f"Translating from [\033[1;33m{origin.upper()}\033[0m] to [\033[1;33m{destiny.upper()}\033[0m]...\n")
                        
                        # THE MAGIC: Using the Google Translate engine behind the scenes!
                        translation = GoogleTranslator(source=origin, target=destiny).translate(text)
                            
                        print(f"📝 \033[1;32mOriginal:\033[0m {text}")
                        
                        print(f"✨ \033[1;36mTranslation:\033[0m")
                        lines_translation = textwrap.wrap(translation, width=75)
                        for line in lines_translation:
                            print(f"   {line}")
                            
                    except ValueError:
                        print("❌ Invalid language format. Use a hyphen. Example: en-pt, pt-en")
                    except Exception as e:
                        print(f"\033[1;31mTranslation error: {e}\033[0m")
                        print("TIP: Check that the language abbreviations are correct (e.g., 'en', 'pt', 'es').")
                        
                    print(f"\033[1;35m========================================\033[0m\n")
                else:
                    print("Invalid format. Use: translate [source]-[destination] [text]")
                    print("Example: translate en-pt The quick brown fox jumps over the lazy dog")
            else:
                print("Please enter the language and text. Ex: translate pt-en Hello world")

# Comand cd
        elif comand == "cd":
            if argument:
                try:
                    # Changes the current directory to the one the user typed.
                    os.chdir(argument)
                    print(f"Directory changed to: {os.getcwd()}")
                except FileNotFoundError:
                    print(f"Error: The folder '{argument}' was not found.")
                except NotADirectoryError:
                    print(f"Error: '{argument}' is a file, not a folder.")
                except Exception as e:
                    print(f"Error accessing folder: {e}")
            else:
                print("Please type the folder name. Example: 'cd Documents (or 'cd ..' to go back)'")

# Comand search
        elif comand == "search":
            if argument:
                print(f"\nSearching folders by '{argument}' starting from: {os.getcwd()}")
                print("This may take a few seconds depending on the number of files...\n")
                
                found = 0
                
                # os.walk iterates through the current folder ('.') and absolutely all subfolders within it.
                for source, folders, archives in os.walk('.'):
                    
                    # 1. Check if any folder has the name we typed.
                    for folder_name in folders:
                        # Converting to lowercase so that search is not case-sensitive.
                        if argument.lower() in folder_name.lower():
                            full_path = os.path.join(source, folder_name)
                            print(f" [FOLDER]   {full_path}")
                            found += 1
                            
                    # 2. Check if any file has the name we typed.
                    for archive_name in archives:
                        if argument.lower() in archive_name.lower():
                            full_path = os.path.join(source, archive_name)
                            print(f" [ARCHIVE] {full_path}")
                            found += 1
                
                if found == 0:
                    print(f"No items containing '{argument}' were found here.")
                else:
                    print(f"\nSearch completed: {found} item(s) found.")
            else:
                print("Please type the name or part of the name to search. Example: search for report")

# Comand mkdir
        elif comand == "mkdir":
            if argument:
                try:
                    os.mkdir(argument)
                    print(f"Folder '{argument}' created successfully!")
                except FileExistsError:
                    print(f"Error: The folder '{argument}' already exists.")
                except Exception as e:
                    print(f"Error creating folder: {e}")
            else:
                print("Please type the folder name. Example: 'mkdir important_files'")
                
# Comand rmdir
        elif comand == "rmdir":
            if argument:
                # This function helps to bypass the "Access Denied" error in protected files.
                def force_exclusion(function, path, error_information):
                    os.chmod(path, stat.S_IWRITE)
                    function(path)

                try:
                    # The 'onerror' parameter calls our function if Windows attempts to block the deletion.
                    shutil.rmtree(argument, onerror=force_exclusion)
                    print(f"Folder '{argument}' and all its contents have been successfully deleted!")
                except FileNotFoundError:
                    print(f"Error: The folder '{argument}' was not found.")
                except NotADirectoryError:
                    print(f"Error: '{argument}' is a file, not a folder. Use a command to delete files.")
                except PermissionError:
                    print(f"Critical Error: Access denied. Make sure you are not INSIDE the folder (use 'cd ..' to exit) and that no program is using the files.")
                except Exception as e:
                    print(f"Error deleting folder: {e}")
            else:
                print("Please type the folder name. Example: 'rmdir old_folder'")

# Comand tree
        elif comand == "tree":
            
            # If you don't type anything, it maps the current folder (""). If you type something, it maps the chosen folder.
            target = argument.strip() if argument else "."
            
            if not os.path.exists(target):
                print(f"❌ The folder '{target}' does not exist.")
                continue
                
            print(f"\n\033[1;36m========== 🌳 DIRECTORY MAP ==========\033[0m")
            print(f"Mapping the structure of: \033[1;33m{os.path.abspath(target)}\033[0m\n")
            
            # The magic function that draws the lines.
            def generate_tree(path, prefix="", current_level=0, max_level=3):
                # Security lock to prevent the PC from crashing when reading the entire hard drive.
                if current_level > max_level:
                    print(prefix + "└── \033[1;30m[... depth limit reached ...]\033[0m")
                    return
                    
                try:
                    # Take everything in the folder and organize it (folders and files).
                    items = os.listdir(path)
                    items.sort()
                except PermissionError:
                    # If Windows/Linux blocks access to system folders
                    print(prefix + "└── \033[1;31m⛔ [Access denied]\033[0m")
                    return
                    
                total = len(items)
                for i, item in enumerate(items):
                    last = (i == total - 1)
                    full_path = os.path.join(path, item)
                    
                    # Draw the corners and straight lines.
                    pointer = "└── " if last else "├── "
                    
                    if os.path.isdir(full_path):
                        # If it's a folder, paint it blue and add the icon.
                        print(prefix + pointer + "\033[1;34m📁 " + item + "\033[0m")
                        # Prepare the spacing to draw what's inside THIS folder.
                        extention = "    " if last else "│   "
                        generate_tree(full_path, prefix + extention, current_level + 1, max_level)
                    else:
                        # If it's a regular file, paint it Light Gray and add an icon.
                        print(prefix + pointer + "\033[0;37m📄 " + item + "\033[0m")

            # Start mapping from the root folder you chose.
            print("\033[1;34m📁 " + os.path.basename(os.path.abspath(target)) + "\033[0m")
            generate_tree(target)
            
            print(f"\n\033[1;36m===========================================\033[0m\n")

# Comand open
        elif comand == "open":
            if argument:
                if os.path.exists(argument):
                    try:
                        # Check the user's actual operating system to use the correct command.
                        if sys.platform == "win32":
                            os.startfile(argument)  # Specific command for Windows
                        elif sys.platform == "darwin":
                            subprocess.call(["open", argument])  # Specific command for Mac
                        else:
                            subprocess.call(["xdg-open", argument])  # Specific command for Linux
                            
                        print(f"Opening '{argument}'...")
                    except Exception as e:
                        print(f"Error opening file: {e}")
                else:
                    print(f"Error: The file '{argument}' was not found in the current folder.")
            else:
                print("Please enter the file name. Example: 'open document.pdf'")

# Comand delete
        elif comand == "delete":
            if argument:
                # 1. Checks if what the user typed is actually a file.
                if os.path.isfile(argument):
                    try:
                        # `os.remove` is the Python function for deleting files.
                        os.remove(argument)
                        print(f"File '{argument}' successfully deleted!")
                    except PermissionError:
                        print(f"Error: Access denied. The file '{argument}' may be open in another program or be protected.")
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                        
                # 2. If it's a folder, it warns the user to use the correct command.
                elif os.path.isdir(argument):
                    print(f"Error: '{argument}' is a folder. To delete folders, use the 'rmdir' command.")
                    
                # 3. If it's neither of those, the file doesn't exist there.
                else:
                    print(f"Error: The file '{argument}' was not found in the current folder.")
            else:
                print("Please type the name of the file you want to delete. Example: delete notes.txt")

# Comand empty
        elif comand == "empty":
            if argument:
                try:
                    # Check if the folder actually exists and is a directory.
                    if os.path.isdir(argument):
                        archives = os.listdir(argument)
                        counter = 0
                        
                        for item in archives:
                            # Specify the full file path.
                            item_path = os.path.join(argument, item)
                            
                            # Check if it's a file (so you don't accidentally delete a subfolder).
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                                counter += 1
                                
                        print(f"Success: {counter} file(s) deleted from folder '{argument}'.")
                    else:
                        print(f"Error: '{argument}' was not found or is not a folder.")
                except Exception as e:
                    print(f"Error while trying to empty the folder: {e}")
            else:
                print("Please enter the folder name. Example: 'empty old_files'")
                
# Comand lock  
        elif comand == "lock":
            if argument:
                if os.path.exists(argument):
                    password = input(f"Create a password to lock '{argument}': ")
                    
                    try:
                        # 1. Transform your standard password into a strong 32-byte cryptographic key.
                        key = base64.urlsafe_b64encode(hashlib.sha256(password.encode('utf-8')).digest())
                        fernet = Fernet(key)
                        
                        # 2. Reads the original data from the file.
                        with open(argument, 'rb') as f:
                            original_data = f.read()
                            
                        # 3. Shuffle everything using the key.
                        encrypted_data = fernet.encrypt(original_data)
                        
                        # 4. Save the file with a new name ".lock" and delete the original.
                        new_name = argument + ".lock"
                        with open(new_name, 'wb') as f:
                            f.write(encrypted_data)
                            
                        os.remove(argument) # Delete the unprotected file.
                        print(f"🔒 Success! Protected file saved as '{new_name}'.")
                        print("WARNING: If you forget your password, the file will be lost forever!")
                        
                    except Exception as e:
                        print(f"Error encrypting: {e}")
                else:
                    print(f"Error: File '{argument}' not found.")
            else:
                print("Please enter the file name. Example: lock diary.txt")

# Comand unlock
        elif comand == "unlock":
            if argument:
                if os.path.exists(argument):
                    if not argument.endswith('.lock'):
                        print("Warning: The file does not have the '.lock' extension. Are you sure it's encrypted?")
                        
                    password = input(f"Enter the password to unlock '{argument}': ")
                    
                    try:
                        # 1. Recreate the key using the password you entered.
                        key = base64.urlsafe_b64encode(hashlib.sha256(password.encode('utf-8')).digest())
                        fernet = Fernet(key)
                        
                        # 2. Read the locked data
                        with open(argument, 'rb') as f:
                            encrypted_data = f.read()
                            
                        # 3. Try to unscramble it (if the password is wrong, the math fails and it falls into the except block).
                        original_data = fernet.decrypt(encrypted_data)
                        
                        # 4. Remove the ".lock" extension from the name to revert to normal.
                        original_name = argument.replace('.lock', '')
                        # If the file doesn't have ".lock" in its name, add a suffix to avoid overwriting it incorrectly.
                        if original_name == argument: 
                            original_name = "unlocked_" + argument
                            
                        # 5. Save the readable file and delete the locked version.
                        with open(original_name, 'wb') as f:
                            f.write(original_data)
                            
                        os.remove(argument)
                        print(f"🔓 Success! File unlocked and saved as '{original_name}'.")
                        
                    except Exception:
                        # The library's default error for an incorrect password is InvalidToken, but we generally handle it this way.
                        print("❌ Error: Incorrect password or corrupted file! Access denied.")
                else:
                    print(f"Error: File '{argument}' not found.")
            else:
                print("Please enter the file name. Example: unlock diary.txt.lock")

# Comand hide
        elif comand == "hide":
            # The command expects something like: hide image.png My secret message
            parts = argument.split(" ", 1)
            
            if len(parts) < 2:
                print("❌ Correct usage: hide [image_name.png] [your secret message]")
                print("TIP: Use .PNG images! .JPG images destroy hidden data due to compression.")
            else:
                img_path = parts[0]
                # We added a "terminal marker" so PyOS knows where the message ends.
                message = parts[1] + "@@FIM@@" 
                
                try:
                    from PIL import Image
                    print(f"\n\033[1;35m========== 🕵️ STEGANOGRAPHY ==========\033[0m")
                    print(f"Injecting data into '{img_path}'...")
                    
                    img = Image.open(img_path)
                    img = img.convert('RGB') # It guarantees that we have the Red, Green, and Blue channels.
                    pixels = img.load()
                    width, height = img.size
                    
                    # Converts the text message to zeros and ones (binary).
                    binary = ''.join([format(ord(i), "08b") for i in message])
                    bin_size = len(binary)
                    
                    # Check if the image has enough pixels for the text size.
                    if bin_size > width * height:
                        print("❌ Error: The image is too small to hide this amount of text!")
                    else:
                        idx = 0
                        # Scans the image pixel by pixel.
                        for y in range(height):
                            for x in range(width):
                                if idx < bin_size:
                                    r, g, b = pixels[x, y]
                                    
                                    # LSB MAGIC: Clears the last bit of red color and injects our message bit.
                                    r = (r & 254) | int(binary[idx])
                                    
                                    pixels[x, y] = (r, g, b)
                                    idx += 1
                                else:
                                    break
                            if idx >= bin_size:
                                break
                        
                        new_name = "secret_" + img_path
                        img.save(new_name) # Save the new image without loss.
                        print(f"✅ \033[1;32mSuccess!\033[0m Message injected in an undetectable way.")
                        print(f"Their new camouflage image is called: \033[1;33m{new_name}\033[0m")
                        
                except FileNotFoundError:
                    print(f"❌ Image '{img_path}' not found in the current folder.")
                except Exception as e:
                    print(f"Critical error in the injection engine: {e}")
                print(f"\033[1;35m=======================================\033[0m\n")

# Comand reveal
        elif comand == "reveal":
            if not argument:
                print("❌ Correct usage: reveal [secret_image_name.png]")
            else:
                img_path = argument
                try:
                    from PIL import Image
                    print(f"\n\033[1;35m========== 👁️ DECODER ==========\033[0m")
                    print(f"Analyzing pixels from '{img_path}' looking for LSB anomalies...\n")
                    
                    img = Image.open(img_path)
                    img = img.convert('RGB')
                    pixels = img.load()
                    width, height = img.size
                    
                    # Extracts the last bit from the red channel of all pixels.
                    binary = ""
                    for y in range(height):
                        for x in range(width):
                            r, g, b = pixels[x, y]
                            binary += str(r & 1)
                            
                    # It groups the bits in sets of 8 to transform them back into letters.
                    extracted_message = ""
                    for i in range(0, len(binary), 8):
                        byte = binary[i:i+8]
                        if len(byte) == 8:
                            extracted_message += chr(int(byte, 2))
                            # Once you find our final marker, stop the search.
                            if extracted_message.endswith("@@FIM@@"):
                                extracted_message = extracted_message[:-7] # Remove the marker
                                break
                                
                    print(f"🔓 \033[1;36mMessage Revealed:\033[0m \033[1;37m{extracted_message}\033[0m")
                    
                except FileNotFoundError:
                    print(f"❌ Image '{img_path}' not found.")
                except Exception as e:
                    print(f"Error extracting data: {e}. Are you sure this image has a hidden message?")
                print(f"\033[1;35m=======================================\033[0m\n")

# Comand base64
        elif comand == "base64":
            import base64
            
            # If the user doesn't type anything or types incorrectly
            if not argument or " " not in argument:
                print("\n\033[1;34m========== 🔠 BASE64 ENCODER ==========\033[0m")
                print("Correct usage:")
                print("  \033[1;33mbase64 encode [texto]\033[0m : Converts text to Base64")
                print("  \033[1;33mbase64 decode [texto]\033[0m : Reverts Base64 to plain text.")
                print("\033[1;34m===========================================\033[0m\n")
                continue
                
            # Divide the message command ("encode" or "decode" and the "text")
            parts = argument.split(" ", 1)
            action = parts[0].lower()
            text = parts[1]
            
            if action in ["encode", "code"]:
                try:
                    # Python requires that text be converted into "bytes" before it can be converted.
                    bytes_texto = text.encode('utf-8')
                    base64_bytes = base64.b64encode(bytes_texto)
                    result = base64_bytes.decode('utf-8')
                    
                    print(f"\n🔐 \033[1;32mEncoded Text (Base64):\033[0m")
                    print(f"\033[1;37m{result}\033[0m\n")
                except Exception as e:
                    print(f"❌ Coding error: {e}")
                    
            elif action in ["decode", "decode"]:
                try:
                    # Reverse process: takes the bytes from Base64 and transforms them into readable text.
                    base64_bytes = text.encode('utf-8')
                    bytes_texto = base64.b64decode(base64_bytes)
                    result = bytes_texto.decode('utf-8')
                    
                    print(f"\n🔓 \033[1;36mDecoded Text:\033[0m")
                    print(f"\033[1;37m{result}\033[0m\n")
                except base64.binascii.Error:
                    print("❌ \033[1;31mErro:\033[0m The text entered is not a valid Base64 format (missing information or incorrect characters).")
                except Exception as e:
                    print(f"❌ Error in decoding: {e}")
                    
            else:
                print("❌ Unknown action. Use 'encode' or 'decode'.")

# Comand password
        elif comand == "password":
            # Files from our security system
            key_achive = os.path.join(FOLDER_DATAS, ".key_master.key")
            safe_archive = os.path.join(FOLDER_DATAS, "safe_pyos.json")
            
            # 1. Master Key System (Generates an AES key if you don't already have one)
            if not os.path.exists(key_achive):
                new_key = Fernet.generate_key()
                with open(key_achive, "wb") as f_key:
                    f_key.write(new_key)
            
            # Loads the master key into PyOS memory.
            with open(key_achive, "rb") as f_key:
                key = f_key.read()
            
            encryption_engine = Fernet(key)
            
            # If the user entered only "password", the manual shows
            if not argument:
                print("\n\033[1;31m========== 🔒 ENCRYPTED SAFE ==========\033[0m")
                print("Security Commands:")
                print("  \033[1;33mpassword generate\033[0m                : Create an unbreakable 16-character password.")
                print("  \033[1;33mpassword save [service] [password]\033[0m  : Encrypt and store a password.")
                print("  \033[1;33mpassword read\033[0m                    : Unlock the safe and show your passwords.")
                print("  \033[1;33mpassword delete [service]\033[0m        : Remove a safe password forever.")
                print("\033[1;31m============================================\033[0m\n")
                continue
                
            # Divide the argument. The "2" ensures that the password won't be truncated if it contains spaces!
            parts = argument.split(" ", 2)
            action = parts[0].lower()
            
            if action == "generate":
                # It mixes uppercase letters, lowercase letters, numbers, and difficult symbols.
                characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*_-=+"
                strong_password = "".join(random.choice(characters) for _ in range(16))
                
                print(f"\n🛡️ \033[1;32mNew Password Generated:\033[0m \033[1;37m{strong_password}\033[0m")
                print("TIP: Use 'password save [service] [password]' to save it in the vault!\n")
                
            elif action == "save":
                if len(parts) < 3:
                    print("❌ Syntax error. Use: password save [website_name] [your_password]")
                else:
                    service = parts[1].capitalize()
                    flat_password = parts[2]
                    
                    # THE MAGIC: Transforms the password into an unreadable hash.
                    encrypted_password = encryption_engine.encrypt(flat_password.encode()).decode()
                    
                    # Loads the current vault (if it exists).
                    safe = {}
                    if os.path.exists(safe_archive):
                        try:
                            with open(safe_archive, "r", encoding="utf-8") as f:
                                safe = json.load(f)
                        except Exception:
                            pass
                            
                    # Save the encrypted version and save it to disk.
                    safe[service] = encrypted_password
                    
                    with open(safe_archive, "w", encoding="utf-8") as f:
                        json.dump(safe, f, indent=4)
                        
                    print(f"🔒 \033[1;32mSuccess!\033[0m The password for the service '\033[1;33m{service}\033[0m' was encrypted and locked in the safe.")

            elif action in ["read", "list"]:
                if not os.path.exists(safe_archive):
                    print("📭 Your safe is empty. Use 'password save' first.")
                else:
                    try:
                        with open(safe_archive, "r", encoding="utf-8") as f:
                            safe = json.load(f)
                            
                        print("\n\033[1;31m========== 🔓 OPEN SAFE ==========\033[0m")
                        if not safe:
                            print("The safe has no saved passwords.")
                        else:
                            for service, cipher_password in safe.items():
                                # REVERSE MAGIC: Unlock the password using the Master Key
                                password_revealed = encryption_engine.decrypt(cipher_password.encode()).decode()
                                print(f" 🔑 \033[1;33m{service}:\033[0m {password_revealed}")
                        print("\033[1;31m=====================================\033[0m\n")
                    except Exception as e:
                        print(f"❌ Critical error unlocking the safe. Has the master key been changed? Error: {e}")
            
            elif action in ["delete", "dlt", "remove"]:
                if len(parts) < 2:
                    print("❌ Syntax error. Use: password delete [service_name]")
                else:
                    service = parts[1].capitalize()
                    
                    if os.path.exists(safe_archive):
                        try:
                            with open(safe_archive, "r", encoding="utf-8") as f:
                                safe = json.load(f)
                                
                            # Check if the service actually exists in the safe.
                            if service in safe:
                                del safe[service] # Delete from dictionary
                                
                                # Save the updated vault back to disk.
                                with open(safe_archive, "w", encoding="utf-8") as f:
                                    json.dump(safe, f, indent=4)
                                    
                                print(f"🗑️ \033[1;31mDestroyed:\033[0m The password for '\033[1;33m{service}\033[0m' it was permanently erased from the safe.")
                            else:
                                print(f"❌ The service '{service}' was not found in your notes.")
                                
                        except Exception as e:
                            print(f"Error accessing the safe: {e}")
                    else:
                        print("📭 Your safe is either already empty or has not yet been created.")
            else:
                print("❌ Safe command not recognized. Just type 'password' for help.")

# Comand txt_read
        elif comand == "txt_read":
            if argument:
                # Checks if what the user typed is actually a file
                if os.path.isfile(argument):
                    try:
                        # Opens the file in read-only mode ('r') with accent support (utf-8)
                        with open(argument, 'r', encoding='utf-8') as archive:
                            content = archive.read()
                            print(f"\n--- Reading: {argument} ---\n")
                            print(content)
                            print(f"\n--- End of {argument} ---")
                    except UnicodeDecodeError:
                        print("Error: This does not appear to be a regular text file (it cannot be read).")
                    except Exception as e:
                        print(f"Error reading file: {e}")
                else:
                    print(f"Error: '{argument}' was not found or is not a valid file.")
            else:
                print("Please enter the file name. Example: 'txt_read notes.txt'")
                
# Comand txt_write
        elif comand == "txt_write":
            if argument:
                print(f"\n--- Writing in: {argument} ---")
                print("TIP: Type ':q' to save/exit, or ':u' to delete the previous line.")
                print("-" * 65)
                
                lines = []
                while True:
                    # Displays the current line number for your convenience
                    line = input(f"{len(lines) + 1} | ")
                    
                    if line.strip() == ':q':
                        break
                    elif line.strip() == ':u':
                        if len(lines) > 0:
                            removed = lines.pop() # Remove the last line from the list
                            print(f"   [Line '{removed}' erased]")
                        else:
                            print("   [The file is already empty]")
                        continue
                        
                    lines.append(line)
                
                try:
                    with open(argument, 'w', encoding='utf-8') as archive:
                        archive.write('\n'.join(lines))
                    print(f"File '{argument}' saved successfully!")
                except Exception as e:
                    print(f"Error saving file: {e}")
            else:
                print("Please enter the file name. Example: 'txt_write notas.txt'")

# Comand txt_edit
        elif comand == "txt_edit":
            if argument:
                # Check if the file exists before attempting to edit it
                if os.path.isfile(argument):
                    try:
                        # 1. Open the file and read the lines that are already there
                        with open(argument, 'r', encoding='utf-8') as archive:
                            lines = archive.read().splitlines()
                            
                        print(f"\n--- Editing: {argument} ---")
                        print("Current text:")
                        
                        # Displays the text with line numbers
                        for i, l in enumerate(lines):
                            print(f"{i + 1} | {l}")
                            
                        print("-" * 65)
                        print("Continue typing to add. Use ':q' to save or ':u' to delete")
                        
                        # 2. Enter the same typing loop as "write"
                        while True:
                            line = input(f"{len(lines) + 1} | ")
                            
                            if line.strip() == ':q':
                                break
                            elif line.strip() == ':u':
                                if len(lines) > 0:
                                    removed = lines.pop()
                                    print(f"   [Line '{removed}' erased]")
                                else:
                                    print("   [The file is already empty]")
                                continue
                                
                            lines.append(line)
                            
                        # 3. Save the file, overwriting it with the updated list
                        with open(argument, 'w', encoding='utf-8') as archive:
                            archive.write('\n'.join(lines))
                        print(f"File '{argument}' updated successfully!")
                        
                    except Exception as e:
                        print(f"Error editing file: {e}")
                else:
                    print(f"Error: '{argument}' was not found. If you want to create a new one, use the 'txt_write' command")
            else:
                print("Please enter the file name. Example: 'txt_edit notes.txt'")

# Comand csv_write
        elif comand == "csv_write":
            if argument:
                # Ensures the file has the correct extension
                if not argument.endswith('.csv'):
                    argument += '.csv'
                    
                if os.path.exists(argument):
                    print(f"Error: The file '{argument}' already exists. Use 'csv_add' to insert data")
                else:
                    print(f"\n--- Creating a Spreadsheet: {argument} ---")
                    columns = input("Enter the column names separated by commas (e.g., Name, Age, Email): ")
                    
                    # Clear the extra spaces around the column names
                    headers = [c.strip() for c in columns.split(',')]
                    
                    try:
                        # Open in 'w' mode to write the first line (headers)
                        with open(argument, 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(headers)
                        print(f"Spreadsheet '{argument}' created with the following columns: {', '.join(headers)}")
                    except Exception as e:
                        print(f"Error creating spreadsheet: {e}")
            else:
                print("Please enter the spreadsheet name. Example: csv_write clients.csv")

# Comand csv_add
        elif comand == "csv_add":
            if argument:
                if not argument.endswith('.csv'):
                    argument += '.csv'
                    
                if os.path.exists(argument):
                    try:
                        # First, it reads the file just to find out what the columns are
                        with open(argument, 'r', encoding='utf-8') as f:
                            reader = csv.reader(f)
                            headers = next(reader, None) # Just take the first line
                        
                        if headers:
                            print(f"\n--- Adicionando dados em: {argument} ---")
                            new_line = []
                            
                            # Requests the specific value for each column dynamically
                            for column in headers:
                                value = input(f"Type the value for '{column}': ")
                                new_line.append(value)
                            
                            # Now open in 'a' (append) mode to paste the new line at the end
                            with open(argument, 'a', newline='', encoding='utf-8') as f:
                                writer = csv.writer(f)
                                writer.writerow(new_line)
                            print("Data added successfully!")
                        else:
                            print("Error: The spreadsheet is empty and has no defined columns")
                    except Exception as e:
                        print(f"Error editing spreadsheet: {e}")
                else:
                    print(f"Error: Spreadsheet '{argument}' not found. Create it first using 'csv_write'")
            else:
                print("Please enter the spreadsheet name. Example: cdv_add clients.csv")

# Comand csv_read
        elif comand == "csv_read":
            if argument:
                if not argument.endswith('.csv'):
                    argument += '.csv'
                    
                if os.path.exists(argument):
                    try:
                        with open(argument, 'r', encoding='utf-8') as f:
                            reader = csv.reader(f)
                            datas = list(reader) # Turn everything into a Python list
                            
                            if not datas:
                                print("The spreadsheet is empty.")
                            else:
                                print(f"\n--- Reading Spreadsheet: {argument} ---\n")
                                
                                # Find the longest word in each column to perfectly align the table
                                sizes = [max(len(str(item)) for item in column) for column in zip(*datas)]
                                
                                for i, line in enumerate(datas):
                                    # Justify the left-aligned text based on the maximum column size
                                    formatted_line = " | ".join(str(item).ljust(size) for item, size in zip(line, sizes))
                                    print(formatted_line)
                                    
                                    # Prints a dividing line just below the header
                                    if i == 0:
                                        print("-" * len(formatted_line))
                                        
                                print("\n--- End of Spreadsheet ---")
                    except Exception as e:
                        print(f"Error reading spreadsheet: {e}")
                else:
                    print(f"Error: Spreadsheet '{argument}' not found.")
            else:
                print("Please enter the spreadsheet name. Example: csv_read clients.csv")

# Comand open_image
        elif comand == "open_image":
            if argument:
                if os.path.exists(argument):
                    try:
                        # 1. Open the image and convert it to the standard RGB format
                        from PIL import Image
                        img = Image.open(argument)
                        img = img.convert("RGB")
                        
                        # 2. Defines the maximum width (in "pixels/characters") to fit in the terminal
                        max_width = 60 
                        
                        # 3. Calculate the new height while maintaining the image's aspect ratio.
                        # We multiply by 0.5 because the terminal characters are twice as tall as they are wide!
                        proportion = (img.height / img.width)
                        new_height = int(max_width * proportion * 0.5)
                        
                        # 4. Shrink the image
                        img = img.resize((max_width, new_height))
                        
                        print(f"\n--- Displaying: {argument} ---")
                        
                        # 5. Scan the image line by line, pixel by pixel
                        for y in range(new_height):
                            terminal_line = ""
                            for x in range(max_width):
                                r, g, b = img.getpixel((x, y))
                                
                                # THE MAGIC: ANSI True Color code to paint the text background with the pixel's RGB.
                                # We put two blank spaces ' ' to form the block and then '\033[0m' to reset the color.
                                terminal_line += f"\033[48;2;{r};{g};{b}m  \033[0m"
                                
                            print(terminal_line) # Prints the entire line of the image.
                            
                        print("-" * (max_width * 2))
                        
                    except Exception as e:
                        print(f"Error processing image. Are you sure it's a valid image file? Error: {e}")
                else:
                    print(f"Error: The file '{argument}' was not found.")
            else:
                print("Please enter the image name. Example: open_image logo.png")

# Comand audio
        elif comand == "audio":
            if argument:
                # The audio engine is initialized only when it is used for the first time.
                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                action = argument.strip().lower()

                if action == "pause":
                    pygame.mixer.music.pause()
                    print("⏸️ Music paused.")
                elif action == "continue" or action == "play":
                    pygame.mixer.music.unpause()
                    print("▶️ Music resumed.")
                elif action == "stop":
                    pygame.mixer.music.stop()
                    print("⏹️ Music stopped.")
                else:
                    # If it's not a control command, it assumes it's the filename.
                    if os.path.exists(argument):
                        try:
                            pygame.mixer.music.load(argument)
                            # The -1 makes the music loop infinitely.
                            pygame.mixer.music.play(-1)
                            print(f"🎵 Now playing: {argument} (in the background)")
                            print("TIP: Use 'audio pause' or 'audio stop' to control the audio.")
                        except Exception as e:
                            print(f"Error playing the file. Please ensure it is a valid .mp3 or .wav file. Error: {e}")
                    else:
                        print(f"Error: The file '{argument}' was not found.")
            else:
                print("Please type the song title or command. Ex: audio lofi.mp3")

# Comand disk
        elif comand == "disk":
            try:
                # Analyze the disk based on the directory we are in
                actual_path = os.getcwd()
                total, used, free = shutil.disk_usage(actual_path)
                
                # Converts values ​​from bytes to Gigabytes (GB)
                gb = 1024 ** 3
                
                print(f"\nAnalysis of current disk storage:")
                print(f" -> Total Space : {total // gb} GB")
                print(f" -> Used Space  : {used // gb} GB")
                print(f" -> Free Space  : {free // gb} GB")
            except Exception as e:
                print(f"Error parsing disk: {e}")

# Comand status
        elif comand == "status":
            print("\n--- PyOS Hardware Monitor ---")
            print("Analyzing system sensors... (please wait 1 second)\n")
            
            try:
                # Internal function to draw the visual progress bar.
                def generate_bar(percentage, size=30):
                    filled = int(size * percentage // 100)
                    empty = size - filled
                    return f"[{'█' * filled}{'-' * empty}]"

                # 1. Reads the CPU (interval=1 makes Python wait 1 second to measure the actual speed)
                cpu_use = psutil.cpu_percent(interval=1)
                
                # 2. Reads the RAM Memory
                memory = psutil.virtual_memory()
                ram_use = memory.percent
                ram_total = memory.total / (1024**3) # Convert from bytes to Gigabytes (GB)
                ram_usage = memory.used / (1024**3)
                
                # 3. Read the battery (if it's a laptop).
                battery = psutil.sensors_battery()

                # Print the results with the bars.
                print(f"CPU: {generate_bar(cpu_use)} {cpu_use}%")
                print(f"RAM: {generate_bar(ram_use)} {ram_use}% ({ram_usage:.1f}GB / {ram_total:.1f}GB)")
                
                # Check if the computer has a battery sensor.
                if battery:
                    status_socket = "🔌 Conected" if battery.power_plugged else "🔋 In battery"
                    print(f"BAT: {generate_bar(battery.percent)} {battery.percent}% ({status_socket})")
                else:
                    print("BAT: [ Battery sensor not detected (Desktop Computer?) ]")
                    
                print("-" * 32)
                
            except Exception as e:
                print(f"Error reading hardware sensors: {e}")

# Comand devices
        elif comand == "devices":
            print("\n--- PyOS Device Manager ---")
            
            # 1. List of Network Cards and Adapters
            print("🌐 Network Adapters:")
            try:
                networks = psutil.net_if_addrs()
                for plate in networks.keys():
                    # Ignores extraneous Windows virtual adapters to keep the list clean.
                    if "Loopback" not in plate and "Pseudo" not in plate:
                        print(f"   [+] {plate}")
            except Exception as e:
                print(f"   Erro ao ler rede: {e}")

            print("\n🔌 Connected USB Devices:")
            print("   (Reading doors, please wait a few seconds...)\n")
            
            # 2. List USB devices using native system commands.
            try:
                usb_devices = []
                
                if sys.platform == 'win32':
                    # It asks Windows PowerShell to list only active USB drives with names.
                    cmd = ['powershell', '-Command', "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' -and $_.FriendlyName } | Select-Object -ExpandProperty FriendlyName"]
                    # `errors='ignore'` prevents accented characters from breaking the code.
                    output = subprocess.check_output(cmd, encoding='cp850', errors='ignore')
                    
                    # Clear the list and remove the generic "Hubs" that Windows duplicates.
                    lines = [line.strip() for line in output.split('\n') if line.strip() and "Hub" not in line]
                    usb_devices = list(set(lines)) # set() remove duplicates
                    
                elif sys.platform == 'linux':
                    # Use the lsusb command in Linux.
                    output = subprocess.check_output(['lsusb'], text=True)
                    usb_devices = [line.split(':', 2)[-1].strip() for line in output.split('\n') if line.strip()]
                    
                elif sys.platform == 'darwin':
                    # Use the Mac's system_profiler.
                    output = subprocess.check_output(['system_profiler', 'SPUSBDataType'], text=True)
                    usb_devices = [line.strip().replace(':', '') for line in output.split('\n') if line.startswith('        ') and ':' in line and '0x' not in line]
                
                # Print the results found.
                if usb_devices:
                    for d in usb_devices:
                        print(f"   [USB] {d}")
                else:
                    print("   No named USB device found.")
                    
            except Exception as e:
                print(f"   [Error reading USB ports: The system blocked the scan]")
                
            print("-" * 42)

# Comand scan
        elif comand == "scan":
            import socket
            import threading
            
            print(f"\n\033[1;36m========== 📡 LOCAL NETWORK RADAR ==========\033[0m")
            print("Initiating tactical sweep (Ping Sweep)...")
            
            # 1. Find out what YOUR current IP address is on the network.
            my_ip = "127.0.0.1"
            try:
                # Try connecting to Google quickly just so your router can give you your "identity".
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                my_ip = s.getsockname()[0]
                s.close()
            except Exception:
                print("❌ We were unable to identify the network. Are you connected via Wi-Fi/Cable?")
                continue
                
            # Extracts the network base (e.g., from "192.168.0.15" becomes "192.168.0.")
            ip_base = '.'.join(my_ip.split('.')[:-1]) + '.'
            print(f"Your Subnet: \033[1;33m{ip_base}0/24\033[0m")
            print("Sending 254 parallel packets. Please wait...\n")
            
            active_devices = []
            threads = []
            
            # 2. The function that each thread will perform (ping a single IP address)
            def drip_target(ip):
                # The command changes depending on whether it's Windows (win32) or Linux/Mac.
                if sys.platform == "win32":
                    # -n 1 (sends 1 packet) | -w 500 (waits half a second) | > nul (hides the ugly text from the system)
                    cmd = f"ping -n 1 -w 500 {ip} > nul 2>&1"
                else:
                    # -c 1 (1 packet) | -W 1 (wait 1 second) | > /dev/null (hide the text)
                    cmd = f"ping -c 1 -W 1 {ip} > /dev/null 2>&1"
                
                answer = os.system(cmd)
                
                # If the response is 0, it means the target received the packet and responded!
                if answer == 0:
                    active_devices.append(ip)

            # 3. It fires all 254 threads at once.
            for i in range(1, 255):
                target_ip = f"{ip_base}{i}"
                t = threading.Thread(target=drip_target, args=(target_ip,))
                threads.append(t)
                t.start()
                
            # 4. Wait for all the radar systems to come back with the answers.
            for t in threads:
                t.join()
                
            # 5. Print the final report and organize the IPs in numerical order.
            active_devices.sort(key=lambda ip: int(ip.split('.')[-1]))
            
            print(f"🎯 \033[1;32mScan Completed!\033[0m Found \033[1;37m{len(active_devices)}\033[0m active devices:")
            for active in active_devices:
                if active == my_ip:
                    print(f"   💻 \033[1;36m{active}\033[0m (This Computer)")
                elif active == f"{ip_base}1":
                    print(f"   🌐 \033[1;33m{active}\033[0m (Probable Router)")
                else:
                    print(f"   📱 \033[1;37m{active}\033[0m (Unknown Device)")
                    
            print(f"\033[1;36m============================================\033[0m\n")

# Comand adduser
        elif comand == "adduser":
            if argument:
                archive_db = os.path.join(FOLDER_DATAS, "users_db.json")
                try:
                    # Loads the current database.
                    with open(archive_db, 'r', encoding='utf-8') as f:
                        database_users = json.load(f)
                    
                    # Checks if the user already exists.
                    if argument in database_users:
                        print(f"Error: The user '{argument}' already exists in the system.")
                    else:
                        # Asks the new user for the password.
                        new_password = input(f"Create a password for the user '{argument}': ")
                        database_users[argument] = new_password
                        
                        # Saves the update to the JSON file.
                        with open(archive_db, 'w', encoding='utf-8') as f:
                            json.dump(database_users, f, indent=4)
                        print(f"User '{argument}' created successfully!")
                except Exception as e:
                    print(f"Error managing users: {e}")
            else:
                print("Please enter the name of the new user. Example: adduser visitor")

# Comand dltuser
        elif comand == "dltuser":
            if argument:
                # Safety lock: prevents digital suicide!
                if argument == user:
                    print("Critical Error: You cannot delete your own user account while logged in!")
                else:
                    archive_db = os.path.join(FOLDER_DATAS, "users_db.json")
                    archive_config = os.path.join(FOLDER_DATAS, "config_db.json")
                    try:
                        with open(archive_db, 'r', encoding='utf-8') as f:
                            database_users = json.load(f)
                        
                        if argument in database_users:
                            # Delete the user from the dictionary and save.
                            del database_users[argument]
                            with open(archive_db, 'w', encoding='utf-8') as f:
                                json.dump(database_users, f, indent=4)
                                        
                            print(f"User '{argument}' successfully deleted from the system!")
                        else:
                            print(f"Error: User '{argument}' does not exist in the database.")
                    except Exception as e:
                        print(f"Error managing users: {e}")
            else:
                print("Please enter the username you wish to delete. Example: dltuser visitor")

# Comand self-destruct
        elif comand == "self-destruct":
            import time
            import tempfile
            
            print("\n\033[1;41m\033[1;37m !!! MAXIMUM SECURITY ALERT !!! \033[0m")
            print("\033[1;31mYou have initiated the Total Self-Destruction Protocol.\033[0m")
            print("This will erase your Database, Passwords and \033[1;33mALL THE SOURCE CODE OF PyOS.\033[0m.")
            print("THERE WILL BE NO GOING BACK. YOUR WORK WILL BE DESTROYED.")
            
            confirmation = input("\n\033[1;33mEnter the code 'OMEGA' to confirm (or Enter to cancel): \033[0m")
            
            if confirmation.strip().upper() == "OMEGA":
                print("\n\033[1;31m[!] CODE ACCEPTED. OMEGA PROTOCOL INITIATED.\033[0m")
                
                for i in range(5, 0, -1):
                    sys.stdout.write(f"\r\033[1;31m[ STARTING TOTAL CLEANING IN {i} ... ]\033[0m")
                    sys.stdout.flush()
                    time.sleep(1)
                    
                print("\n\n\033[1;33mPREPARING EXPLOSIVE CHARGE FOR THE SYSTEM...\033[0m")
                time.sleep(1)
                
                # 1. Get the absolute path to the current folder of your PyOS project.
                folder_pyos = os.getcwd()
                
                # 2. The Trick: Create a .bat script in the Windows TEMP folder (far away from here).
                bat_path = os.path.join(tempfile.gettempdir(), "erase_pyos.bat")
                
                # This script waits 2 seconds, deletes its entire folder (rmdir /s /q), and then deletes itself.
                bat_content = f"""@echo off
                timeout /t 2 /nobreak > nul
                rmdir /s /q "{folder_pyos}"
                del "%~f0"
                """
                # Save the ghost script
                with open(bat_path, "w", encoding="utf-8") as f:
                    f.write(bat_content)
                    
                print("\n\033[1;31mGOODBYE.\033[0m")
                time.sleep(1)
                
                # 3. Executes the ghost script invisibly and independently from Python.
                # CREATE_NO_WINDOW (0x08000000) prevents the black screen from appearing in the command prompt.
                subprocess.Popen(["cmd.exe", "/c", bat_path], creationflags=0x08000000)
                
                # 4. Process suicide: PyOS closes in the same fraction of a second.
                # This frees up the folder so that the ghost script can delete it.
                sys.exit(0)
                
            else:
                print("\n\033[1;32mProtocol aborted. Source code survived.\033[0m")

        else:
            print(f"The command '{command}' is not recognized. Type 'help' to see the list.")

if __name__ == "__main__":
    start_pyos()
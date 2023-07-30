#Hatırlamasını istediğiniz zaman cümleniniz sonuna hatırla ibaresini ekleyin .
#Hatırlama özelliğini kullanmak için memory.db dosyası oluşturun.
#Kullanmak için Api-Key ihtiyacınız var.
#Çalıştırmak için python 11.py kullanın.

import openai
from colorama import Fore, Style
from memory import get_memory_data, save_memory_data, create_tables

openai.api_key = 'Api-Key'

# Veritabanı tablolarını oluştur
create_tables()

memory_data = get_memory_data()

def get_memory_data_for_prompt():
    data = "\n".join([f"{key} hatırlıyor {value}" for key, value in memory_data.items()])
    return data

def generate_chat_response(message):
    global memory_data

    user = "User"
    bot = "Bot"

    if user not in memory_data:
        memory_data[user] = []

    memory_data[user].append(message)

    history = '\n'.join(memory_data[user][-50:]) 

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "Sen bir mesajlaşma robotusun"},
            {"role": "user", "content": f"{history}\n{memory_data}"}

        ]
    )

    chat_response = response.choices[0].message.content.strip()

    if bot not in memory_data:
        memory_data[bot] = []

    memory_data[bot].append(chat_response)

    return chat_response

while True:
    user_input = input(Fore.RED + "You: " + Style.RESET_ALL)
    if "hatırla" in user_input:
        parts = user_input.split("hatırla")
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()

            if key not in memory_data:
                save_memory_data(key, value)
                print(Fore.GREEN + "Bot: Tamam, anladım. Bilgiyi hatırladım." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Bot: Bu isim zaten hatırlanmış." + Style.RESET_ALL)

            bot_response = generate_chat_response(user_input)
            print(Fore.GREEN + "Bot:", bot_response + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Bot: Üzgünüm, bilgiyi anlamadım. Lütfen doğru formatta girin." + Style.RESET_ALL)
    elif "?" in user_input and "kaç yaşında" in user_input:
        parts = user_input.split("?")[1].strip().split("kaç yaşında")
        if len(parts) == 1:
            key = parts[0].strip()

            if key in memory_data:
                print(Fore.GREEN + f"Bot: {key} hakkında hatırladığım bilgi: {memory_data[key]}" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"Bot: {key} hakkında bilgi hatırlamıyorum." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Bot: Üzgünüm, sadece bir kelime hatırlayabilirim." + Style.RESET_ALL)
    elif "geçmiş cevabı getir" in user_input:
        bot_response = generate_chat_response(user_input)
        print(Fore.GREEN + "Bot:", bot_response + Style.RESET_ALL)
    else:
        bot_response = generate_chat_response(user_input)
        print(Fore.GREEN + "Bot:", bot_response + Style.RESET_ALL)
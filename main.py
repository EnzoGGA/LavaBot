from lib import keys
import google.generativeai as genai
import os
import json
from google.generativeai.types import generation_types as gt

send = (lambda text, sty=0, color=0, back=40, end='\n': print(f"\033[{sty};{color};{back}m{text}\033[m", end=end))
clear = (lambda: os.system('cls' if os.name == 'nt' else 'clear'))


def mudar_json(n_colum=None, alt_colum=None):
    with open('lib/data.json', 'r') as f:
        data = json.loads(f.read())
        if n_colum is not None and alt_colum is not None:
            data[n_colum] = alt_colum
    if n_colum is not None and alt_colum is not None:
        with open('lib/data.json', 'w+') as f:
            json.dump(data, f)
    return data


def mudar_hist(hist, title, num_chat=''):
    # Erro
    with open('hist/hist.json', 'r') as f:
        data = json.loads(f.read())
    if not num_chat:
        data[max(list(map(int, list(data.keys())))) + 1] = {"title": title, "content": hist}
    else:
        data[num_chat] = {"title": title, "content": hist}
    with open('hist/hist.json', 'w') as f:
        json.dump(data, f)


def mostrar_hist():
    with open('hist/hist.json', 'r') as f:
        data = json.loads(f.read())
    txt = ''
    if data:
        txt = "Seu historico:"
        for e in data:
            txt += f"\n[{e}] {data[e]['title']}"
    return txt


def delete_hist(num_chat: str):
    with open('hist/hist.json', 'r') as f:
        data = json.loads(f.read())
    data.pop(num_chat)
    data_new = {}
    for e in range(0, len(data.keys())):
        data_new[str(e + 1)] = data[list(data.keys())[e]]
    with open('hist/hist.json', 'w') as f:
        json.dump(data_new, f)


def hist_m(history: list, text: str, role='user'):
    history.append({'role': role, 'parts': [text]})
    return history


def send_message(prompt: str, chat: genai.GenerativeModel, history=None, temp=0.25):
    if history is None:
        history = []
    history.append({'role': 'user', 'parts': [prompt]})
    response = chat.generate_content(history, generation_config=genai.types.GenerationConfig(
        temperature=temp), safety_settings=safety_settings).text
    history.append({'role': 'model', 'parts': [response]})
    return response


def chat_load(num, chat: genai.GenerativeModel, nome: str, prefix: str, bot: str, temp: float):
    with open('hist/hist.json', 'r') as f:
        data = json.loads(f.read())[num]
    title = data['title']
    content_g = data['content']
    content = content_g[3:]
    clear()
    send(f"Titulo: {title}\nTemperatura atual da IA: {temp}", color=32)
    for e in content:
        if e['role'] == 'user':
            send(f"{nome}: {e['parts'][0]}")
        else:
            send(f"{bot}: {e['parts'][0]}", color=36)
    init_chat(chat, nome, prefix, bot, content_g, temp, is_init=False, title=title, num_chat=num,
              prompt=input(f"{nome}: "))


def init_chat(chat: genai.GenerativeModel, nome: str, prefix: str, bot: str, history: list, temp: float, is_init=True,
              title='', num_chat=None, prompt=None, passou=True):
    if is_init:
        passou = False
        with open('hist/hist.json', 'r') as f:
            num_chat = str(len(json.loads(f.read()).keys()) + 1)
        text = send_message(f'Olá, meu nome é {nome}!', chat, history, temp)
        clear()
        send(f'{bot}: ', end='')
        send(text, color=36)
        prompt = input(f"{nome}: ")
        title = (chat.generate_content(f"Crie apenas um pequeno titulo para o prompt a seguir:\n{prompt}",
                                       generation_config=genai.types.GenerationConfig(temperature=0),
                                       safety_settings=safety_settings).text)

    while True:
        if prompt.replace(' ', ''):
            if not prompt[:1] == prefix:
                try:
                    response = send_message(prompt, chat, history, temp)
                    send(f'{bot}: ', end='')
                    send(response, color=36)
                except gt.BlockedPromptException:
                    response = chat.generate_content(
                        'Crie uma pequena frase falando algo tipo: Não posso responder isso pois '
                        'sou apenas uma IA').text
                    hist_m(history, response, 'model')
                    send(f'{bot}: ', end='')
                    send(response, color=31)
                mudar_hist(history, title, num_chat)
                if not passou:
                    chat_load(num_chat, chat, nome, prefix, bot, temp)
            else:
                command(prompt, True)
        prompt = input(f"{nome}: ")


def new_chat(nome: str, prefix: str, bot: str, temp: float, history: list):
    chat = genai.GenerativeModel('gemini-pro',
                                 generation_config=genai.types.GenerationConfig(
                                     temperature=temp))
    init_chat(chat, nome, prefix, bot, history, temp)


def command(msg, is_chat=False):
    data = mudar_json()
    prefix = data['prefix']
    nome = data['name']
    bot = data['name_b']
    temp = data['temperature']
    base_hist = [{"role": "user", "parts": [keys.base_text]}, {"role": "model", "parts": [f"Ok, agora me chamo {bot}, e"
                                                                                          f"seguirei as recomendações."]}]
    comandos = keys.comandos
    is_prefix = msg[:1] == prefix
    if is_prefix or not is_chat:
        options = msg.lstrip(msg.split()[0]).strip()
        msg = msg.lstrip(prefix).split()[0].lower()
        if msg in comandos:
            if msg in ['help', 'h', '?']:
                send("Comandos:", color=36)
                for comandos in comandos:
                    send(f"{prefix}{comandos}", color=36)
                send(keys.menu(prefix), color=36)
            elif msg in ['quit', 'exit']:
                if is_chat:
                    send("Voce está prestes a sair da conversa, esta certo disso? (s/N) ", color=33, end='')
                    if input() in ['s', 'S', 'sim', 'Sim']:
                        clear()
                        main()
                    else:
                        pass
                else:
                    send("Voce está prestes a sair do aplicativo, esta certo disso? (s/N) ", color=33, end='')
                    if input() in ['s', 'S', 'sim', 'Sim']:
                        send("Até mais!", color=32)
                        exit()
                    else:
                        pass
            elif msg in ['hst', 'hist', 'historico']:
                txt = mostrar_hist()
                if txt:
                    send(txt, color=32)
                else:
                    send('Você ainda não tem historico!', color=31)
            elif msg in ['cls', 'clear']:
                clear()
            elif msg in ['del', 'delete_chat', 'delete']:
                with open('hist/hist.json', 'r') as f:
                    len_hist = len(json.loads(f.read()).keys())
                txt = mostrar_hist()
                if txt:
                    send(txt + f"\n[{len_hist + 1}] all", color=32)
                    if options:
                        if options not in ['all', 'a', 'A', str(len_hist + 1)]:
                            try:
                                int(options)
                                delete_hist(options) if (input(f"Deseja apagar o historico Nº {options} (s/N)? ") in
                                                         ['sim', 'Sim', 's', 'S']) else None
                            except ValueError:
                                send('Digite um valor valido!', color=31)
                        else:
                            if input(f"Deseja apagar o historico (s/N)? ") in ['sim', 'Sim', 's', 'S']:
                                with open('hist/hist.json', 'w') as f:
                                    json.dump({}, f)
                    else:
                        try:
                            op = input("Digite o numero do chat que deseja apagar: ")
                            if 1 <= int(op) <= len_hist + 1:
                                if not op == str(len_hist + 1):
                                    delete_hist(op) if (input(f"Deseja apagar o historico Nº {op}?(s/N) ") in
                                                        ['sim', 'Sim', 's', 'S']) else None
                                else:
                                    if input(f"Deseja apagar o historico (s/N)? ") in ['sim', 'Sim', 's', 'S']:
                                        with open('hist/hist.json', 'w') as f:
                                            json.dump({}, f)
                            else:
                                send('Digite um valor valido!', color=31)
                        except ValueError:
                            send('Digite um valor valido!', color=31)
                else:
                    send('Você ainda não tem historico!', color=31)
            elif msg in ['gen', 'generate', 'gerar']:
                chat = genai.GenerativeModel('gemini-pro')
                if options:
                    send(
                        f"{bot}: {chat.generate_content([options],
                                                        generation_config=genai.types.GenerationConfig(
                                                            temperature=temp),
                                                        safety_settings=safety_settings).text}", color=32)
                else:
                    send(
                        f"{bot}: {chat.generate_content([input(f"{nome}: ")],
                                                        generation_config=genai.types.GenerationConfig(
                                                            temperature=temp),
                                                        safety_settings=safety_settings).text}", color=32)
            elif msg in ['temp', 'temperatura', 'temperature']:
                if options:
                    try:
                        options = float(options.replace(',', '.'))
                        if 0 <= options <= 1:
                            mudar_json('temperature', options)
                            send(f"Temperature alterado para {options}", color=32)
                        else:
                            send('Selecione um valor entre 0 e 1!', color=31)
                    except ValueError:
                        send('Selecione um valor valido entre 0 e 1!', color=31)
                else:
                    try:
                        send(f"Temperature = {temp}", color=32)
                        op = float(input("Digite a temperatura que deseja: ").replace(',', '.'))
                        if 0 <= op <= 1:
                            mudar_json('temperature', op)
                            send(f"Temperature alterado para {op}", color=32)
                        else:
                            send('Selecione um valor entre 0 e 1!', color=31)
                    except ValueError:
                        send('Selecione um valor valido entre 0 e 1!', color=31)
            elif msg == "prefix":
                new = input("Digite o prefixo de sua preferencia: ") if not options else options
                mudar_json('prefix', options if options else new)
                send(f'Prefixo alterado para {new}', color=32)
            elif msg in ['v', 'version', 'ver']:
                send(f'LavaAI versão: {data["version"]}', color=32)
            elif msg in ['terminalCommand', 'tc']:
                if options in ['0', '1']:
                    mudar_json('TerminalCommand', True if options == '1' else False)
                    send(f"TerminalCommand alterado para {'true' if options == '1' else 'false'}", color=32)
            elif msg in ['nome', 'name']:
                send(f"Nome atual: {nome}", color=32)
                new = input("Digite o seu nome: ") if not options else options
                mudar_json('name', options if options else new)
                send(f'Nome alterado para {new}', color=32)
            elif msg in ['bot', 'name_b']:
                new = input("Digite o nome de sua preferencia: ") if not options else options
                mudar_json('name_b', options if options else new)
                send(f'Nome da IA alterado para {new}', color=32)
            elif msg == 'new':
                send("Inicializando novo chat", color=32)
                new_chat(nome, prefix, bot, temp, base_hist)
            elif msg in ['open', 'chat', 'chats']:
                chat = genai.GenerativeModel('gemini-pro',
                                             generation_config=genai.types.GenerationConfig(
                                                 temperature=temp))
                with open('hist/hist.json', 'r') as f:
                    len_hist = len(json.loads(f.read()).keys())
                if options:
                    try:
                        if 1 <= int(options) <= len_hist:
                            chat_load(options, chat, nome, prefix, bot, temp)
                        else:
                            send("Digite um valor valido!", color=31)
                    except ValueError:
                        send("Digite um valor valido!", color=31)
                else:
                    try:
                        hist = mostrar_hist()
                        if hist:
                            send(hist, color=32)
                            op = input("Selecione qual chat deseja entrar: ")
                            if 1 <= int(op) <= len_hist:
                                chat_load(op, chat, nome, prefix, bot, temp)
                            else:
                                send("Digite um valor valido!", color=31)
                        else:
                            send("Você não tem chats ativos", color=31)
                    except ValueError:
                        send("Digite um valor valido!", color=31)
        else:
            if data["TerminalCommand"]:
                msg = msg.lstrip(prefix).split()[0]
                send(f'Excessão: {msg}', color=31)
                os.system(msg)
            else:
                send(
                    f'O comando {prefix}{msg} não está registrado, verifique os comandos registrados usando '
                    f'{prefix}help')


def main():
    data = mudar_json()
    if data['FirstAccess']:
        mudar_json("name", input("Digite seu nome: "))
        mudar_json('FirstAccess', False)
    send(f'Olá {data['name']}, bem vindo(a) a {data["name_b"]}. O projeto LavaAI foi desenvolvida por Enzo '
         f'Albuquerque usando a api do Gemini. Digite seu comando para continuar ou digite {data['prefix']}help para '
         f'o menu de ajuda. Use CTRL+C para sair ou '
         f'{data["prefix"]}exit', color=34)
    while True:
        msg = input('> ')
        if msg:
            command(msg)


safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "block_none"
    },
]
if __name__ == '__main__':
    genai.configure(api_key=keys.g_api_key)
    model = genai.GenerativeModel('gemini-pro')
    try:
        clear()
        main()
    except ModuleNotFoundError:
        send('Atenção\nForam detectados alguns erros de modulo e podem ser resolvidos para instalar aperte qualquer '
             'tecla, para cancelar aperte Ctrl+C', sty=1, color=31, end='')
        input()
        os.system('pip install -r requirements.txt')
        clear()
        main()
    except KeyboardInterrupt:
        send("\nAté mais!", color=32)
    except Exception as e:
        send(f'Erro: {e}', color=31)
        main()

import json
import warnings
from requests import get
warnings.filterwarnings("ignore")


def menu(prefix):
    return f'''
{prefix}help | h | ?
Uso:Exibe este menu de ajuda.

{prefix}prefix [options]
Uso: Muda o prefixo para um de sua escolha.

{prefix}name [options]
Uso: Muda seu nome.

{prefix}bot [options]
Uso: Muda o nome da IA.

{prefix}new
Uso: Começa uma nova conversa.

{prefix}temp | temperature
Uso: Define o quão criativo ou objetivo a IA é.
obs: Quanto mais perto de 1 = mais criativo.

{prefix}gen | generate | gerar
Uso: Gera uma resposta da IA sem salvar historico.

{prefix}historico | hst | hist
Uso: Mostra seu historico.

{prefix}del | delete [options]
Uso: Apaga uma conversa do seu historico.

{prefix}v | version | ver
Uso: Mostra a versão do app.

{prefix}quit
Uso: Sai da conversa ou app.

{prefix}chats | open
Uso: Mostra os chats disponiveis.

{prefix}TerminalCommand | tc [options]
Uso: Ativa o modo terminal (todo comando enviado que nao for reconhecido será enviado ao sistema).
obs: 1 para ativar 0 para desativar.

{prefix}exit
Uso: fecha o aplicativo.'''


loc = get('http://ipinfo.io/json').json()
with open('data.json', 'r') as f:
    data = json.loads(f.read())
with open('secrets', 'r') as f:
    g_api_key = f.read()
print(f'Inicializando... (V{data["version"]})')
base_text = (f'I am your creator and from now your name is "{data["name_b"]}" and you are an AI based on the '
             f'gemini-pro that was created by Enzo Albuquerque. You will talk with {data['name']} rigth now, '
             f'{data['name']}`s ip is {loc['ip']} and the location is: latitude: {float(loc['loc'].split(',')[0])} and '
             f'longitude: {float(loc['loc'].split(',')[1])}.\nHere is some informations:\nYour version is currently: '
             f'{data["version"]}.\nYou are running on a console, so you cant use anything that a console '
             f'doesnt support.')
print(base_text)
comandos = ['help', 'h', '?', 'new', 'exit', 'chats', 'quit', 'clear', 'cls', 'prefix', 'terminalcommand', 'tc', 'nome',
            'name', 'bot', 'name_b', 'hst', 'historico', 'hist', 'del', 'delete_chat', 'delete', 'gen', 'generate',
            'gerar', 'temp', 'temperature', 'chat', 'open', 'v', 'version', 'ver']

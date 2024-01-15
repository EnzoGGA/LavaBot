import json
import warnings
warnings.filterwarnings("ignore")


with open('lib/data.json', 'r') as f:
    data = json.loads(f.read())
with open('lib/secrets', 'r') as f:
    g_api_key = f.read()

base_text = (f'I am your creator and from now on i name you "{data["name_b"]}" and you are an AI based on the '
             f'gemini-pro that was created by Enzo Albuquerque. You will talk with {data['name']} now. You do '
             f'not need to answer anything for this prompt!')


comandos = ['help', 'h', '?', 'new', 'exit', 'chats', 'quit', 'clear', 'cls', 'prefix', 'terminalcommand', 'tc', 'nome',
            'name', 'bot', 'name_b', 'hst', 'historico', 'hist', 'del', 'delete_chat', 'delete', 'gen', 'generate',
            'gerar', 'temp', 'temperature', 'chat']


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

{prefix}quit
Uso: Sai da conversa ou app.
        
{prefix}chats
Uso: Mostra os chats disponiveis.
        
{prefix}TerminalCommand | tc [options]
Uso: Ativa o modo terminal (todo comando enviado que nao for reconhecido será enviado ao sistema).
obs: 1 para ativar 0 para desativar.

{prefix}exit
Uso: fecha o aplicativo.'''

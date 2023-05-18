__author__ = "Arthur Conti Gomes da Silva"

from apizabbix import ZabbixAPI
import json
from termcolor import colored
import apizabbix as apizabbix
import os
import pandas as pd

try:
    api = apizabbix.connect()
except:
    print(colored("Não foi possivel conectar ao Zabbix Server.", 'red', attrs=['bold']))
    print(colored("Verifique se as informações passadas estão corretas!", attrs=['bold']))
    exit()

def login():
    api = apizabbix.connect()
    print(colored('Necessário usuário no Zabbix para ter acesso a essa central!', 'red', attrs=['bold']))
    user = input(colored('Usuário (alias): ', attrs=['bold']))
    
    allusers = api.user.get(
    output=['alias'],
    filter={
        'alias': user
        }
    )
    
    count_allusers = api.user.get(
    countOutput=['1'],
    filter={
        'alias': user
        }
    )
    
    string_count = str(count_allusers).strip('[]')
    
    if string_count == '1':
        menu()
    elif string_count == '0':
        print(colored("User "+ user + " não foi encontrado no Zabbix, tente colocar um user valido!", 'red', attrs=['bold']))
        print('')
        login()
        
    string_name = allusers[0]
    string_name = string_name['alias']
        
    api.user.logout()


def banner():
    print(colored('''
                ______       ______ ______ _____            
                ___  /______ ___  /____  /____(_)___  __    
                __  / _  __ `/_  __ \_  __ \_  /__  |/_/    
                _  /__/ /_/ /_  /_/ /  /_/ /  / __>  <      
                /____/\__,_/ /_.___//_.___//_/  /_/|_|
                  ''', 'red', attrs=['bold']))
    print('')   
 
def menu():
    os.system('clear')
    banner()
    print(colored("Bem vindo a sua central de scripts Zabbix", 'blue', attrs=['bold']))
    print(colored('Desenvolvido por Arthur Gomes'))
    print('')
    print(colored('---Escolha uma opção---', 'yellow', attrs=['bold']))
    print('')
    print('[1] - Relatório de alertas')
    print('[2] - Relatório de users')
    print('[3] - Relatório de users desativados')
    print('[4] - Relatótio de hosts enables')
    print('[5] - Criar users')
    print('[6] - Relatório de hosts com agent desatualizado')
    print('')
    print('[0] - Sair')
    print('')
    escolha()
    
def escolha():
    escolha = input(colored('[+] - Selecione uma opção[0-3]\n', 'blue', attrs=['bold']))
    if escolha == '1':
        menu_alertas()
    elif escolha == '2':
        menu_users()
    elif escolha == '3':
        users_disable()
    elif escolha == '4':
        hosts_enable()
    elif escolha == '5':
        cria_user()
    elif escolha == '6':
        agent_desatualizado()
    elif escolha == '0':
        escolha_retorno()
    else:
        print(colored('Você selecionou ' + escolha, 'red', attrs=['bold']))
        print(colored('Por favor escolha uma opção valida', 'red', attrs=['bold']))
        print('')
        menu()

def menu_users():
    os.system('clear')
    print(colored('---Escolha uma opção---', 'yellow', attrs=['bold']))
    print('')
    print('[1] - Relatório com todos os users')
    print('[2] - Pesquisar users')
    print('')
    print('[0] - Voltar')
    print('')
    pesquisa_users()
     
def pesquisa_users():
    api = apizabbix.connect()
    escolha = input(colored('[+] - Selecione uma opção[0-3]\n', 'blue', attrs=['bold']))
    if escolha == '1':
        os.system('clear')
        allusers = api.user.get(
            getAccess=[]
        )
        
        count_allusers = api.user.get(
            countOutput=['1']
        )
        
        string_count = str(count_allusers).strip('[]')
        
        with open('arquivos/allusers.json', 'w') as json_file:
            json.dump(allusers, json_file, indent=4)
            
        print(colored('Foram encotrados ' + string_count + ' user no Zabbix', attrs=['bold']))
        print(colored('Foi gerado um json com o nome "allusers.json" com as informações do user', attrs=['bold']))

        api.user.logout()
    
        escolha_retorno()
        
    elif escolha == '2':
        os.system('clear')
        
        user = input(colored("Digite o alias do user que deseja pesquisar: ", 'blue', attrs=['bold']))
        
        allusers = api.user.get(
        getAccess=[],
        search={
            'alias': user
            }
        )
        
        count_allusers = api.user.get(
        countOutput=['1'],
        search={
            'alias': user
            }
        )
        
        string_count = str(count_allusers).strip('[]')
        
        with open('arquivos/user.json', 'w') as json_file:
            json.dump(allusers, json_file, indent=4)

        print(colored('Foram encotrados ' + string_count + ' user com esse alias', attrs=['bold']))
        print(colored('Foi gerado um json com o nome "user.json" com as informações do user', attrs=['bold']))

        api.user.logout()
        
        escolha_retorno()

    elif escolha == '0':
        menu()
    else:
        input(colored('Opção invalida, aperta Enter para escolher uma nova opção', 'red', attrs=['bold']))     
    
def menu_alertas():
    api = apizabbix.connect()
    os.system('clear')
    print(colored("Os alertas do Zabbix podem ter os seguintes graus de severidade", 'blue', attrs=['bold']))
    print('')
    print(colored('---Escolha uma opção---', 'yellow', attrs=['bold']))
    print('')
    print('[1] - Disaster')
    print('[2] - High')
    print('[3] - Average')
    print('[4] - Warning')
    print('[5] - Information')
    print('')
    print('[0] - Sair')
    print('')
    escolha_alertas()
    
def escolha_alertas():
    api = apizabbix.connect()
    escolha = input(colored("Digite a severidade dos alertas que deseja ver [0-5]\n ", 'blue', attrs=['bold']))
    if escolha == '1':
        severidade = '5'
    elif escolha == '2':
        severidade = '4'
    elif escolha == '3':
        severidade = '3'
    elif escolha == '4':
        severidade = '2'
    elif escolha == '5':
        severidade = '1'
    elif escolha == '0':
        menu()
    else:
        print(colored('Você selecionou ' + escolha, 'red', attrs=['bold']))
        print(colored('Por favor escolha uma opção valida', 'red', attrs=['bold']))
        print('')
        menu_alertas()

    alerts = api.problem.get(
        output=['name'],
        filter={
            'severity': severidade
        }
    )

    count_alerts = api.problem.get(
        countOutput=['1'],
        filter={
            'severity': severidade
        }
    )

    with open('arquivos/alerts.json', 'w') as json_file:
        json.dump(alerts, json_file, indent=4)

    if count_alerts == '0':
        print('')
        print("Existem " + count_alerts + " alertas")
    else:
        print('')
        print("Existem " + count_alerts + " alertas")
        print("Foi gerado um json com o nome: 'alerts.json' com esses alertas")

    api.user.logout()
    
    escolha_retorno()
    
def escolha_retorno():
    print('')
    escolha = input("Deseja fazer outra consulta [y/n]\n")
    if escolha == 'y':
        menu()
    elif escolha == 'n':
        os.system('clear')
        print(colored("Obrigado por usar nosso Scrip", 'blue', attrs=['bold']))
        print(colored('Em caso de dúvidas ou sugestões entrar em contato pelo cliq com agomes', 'blue', attrs=['bold']))
        input(colored("Pressione Enter para sair", 'blue', attrs=['bold']))
        os.system('clear')
        exit()
    else:
        os.system('clear')
        print(colored('Opção invalida, tente novamente', 'red', attrs=['bold']))
        print('')
        escolha_retorno()
        
def cria_user():
    api = apizabbix.connect()
    os.system('clear')
    print(colored('Você esta prestes a criar um novo user no Zabbix', 'blue', attrs=['bold']))
    print(colored('Forneça o alias e a senha do user que deseja criar', 'blue', attrs=['bold']))
    print('')
    user = input(colored('User: ', 'blue', attrs=['bold']))
    senha = input(colored('Senha: ', 'blue', attrs=['bold']))
    
    try:
        create_user = api.user.create(
            {

                "alias": user,
                "passwd": senha,
                "usrgrps": [
                    {
                        "usrgrpid": "8"
                    }
                ]
            }
        )
    except:
        print("Usuário já existe")
        cria_user()
    
    with open('arquivos/create_user.json', 'w') as json_file:
        json.dump(create_user, json_file, indent=4)
    
    print('')
    print(colored('User ' + user + " criado com sucesso", 'blue', attrs=['bold']))
    print(colored('Foi gerado um json com o nome: "create_user", com o id do novo user!', 'blue', attrs=['bold']))
    
    escolha_retorno()
    
def users_disable():
    os.system('clear')
    api = apizabbix.connect()
    input(colored("Pressione Enter para gerar o relatório: ", 'blue', attrs=['bold']))
    group_disable = api.usergroup.get(
        output=['name'],
        selectUsers=['alias'],
        filter={
            'name': 'Disabled'
        }
    )
    
    count_group_disable = api.usergroup.get(
        countOutput=['users'],
        selectUsers=['alias'],
        filter={
            'name': 'Disabled'
        }
    )
    
    with open('arquivos/users_disable.json', 'w') as json_file:
        json.dump(group_disable, json_file, indent=4)
        
    print(colored('Foi gerado um json com o nome: "users_disable", com os nomes desses users', 'blue', attrs=['bold']))
    
    escolha_retorno()
    
def hosts_enable():
    os.system('clear')
    api = apizabbix.connect()
    input(colored("Pressione Enter para gerar o relatório: ", 'blue', attrs=['bold']))
    
    hosts_dis = api.host.get(
        output=["name"],
        filter={
            'status': '0'
        }
    )
    
    hosts_dis = pd.DataFrame(hosts_dis)
    
    hosts_dis.to_csv('arquivos/hosts_enable.csv', columns=['name'], index=False, header=0)
    
    os.system('clear')
    input(colored("O relatório foi gerado com sucesso com o nome de 'hosts_enable.csv', para continuar navegando aperte Enter!", 'blue', attrs=['bold']))

    escolha_retorno()
    
def agent_desatualizado():
    os.system('clear')
    api = apizabbix.connect()
    input(colored("Pressione Enter para gerar o relatório: ", 'blue', attrs=['bold']))
    
    itens = api.item.get(
        output = ['lastvalue'],
        selectHosts = 'extend',
        search = {
            'name': 'Version of Zabbix agent running'
        }
    )
    
    hosts = [] 
    lastvalues = []

    for item in itens:
        hosts.append(item['hosts'][0]['host'])
        lastvalues.append(item['lastvalue'])

    versions = dict(zip(hosts, lastvalues))

    for key, value in list(versions.items()):
        if value != '':
            del versions[key]
            
    count = 0    
        
    for item in versions:
        count = count + 1 

    with open('arquivos/agent_desatualizado.json', 'w') as json_file:
        json.dump(versions, json_file, indent=4)

    os.system('clear')
    print("Existem ", count, " hosts com o Zabbix-agent desatualizado!!")
    input(colored("O relatório foi gerado com sucesso com o nome de 'agent_deatualizado.json', para continuar navegando aperte Enter!", 'blue', attrs=['bold']))
    
    escolha_retorno()
    
def main():
    login()

main()

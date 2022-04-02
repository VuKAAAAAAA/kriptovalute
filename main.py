from bitcoin import *
from blockchain import exchangerates
import PySimpleGUI as sg
from bitcoinrpc.authproxy import AuthServiceProxy
import datetime

#Server access data
user = ""
password = ""
host = ""
port = ""

bitcoin_rpc_client = "http://" + user + ":" + password + "@" + host + ":" + port + "/"

def layout():
    sg.theme('SandyBeach')
    layout = [
                [sg.Image(r"photos\wallet2.png")],
                [sg.Image(r"photos\key2.png", size=(55,55)), sg.Button('Get a private key', button_color = 'red', key='private_key', size = (50,2))],
                [sg.Image(r"photos\key1.png", size=(55,55)), sg.Button('Get a public key', button_color = 'red', key='public_key', size = (50,2))],
                [sg.Image(r"photos\wallet.png", size=(55,55)),sg.Button('Create your bitcoin wallet address', button_color = 'red', key='address', size = (50,2))],
                [sg.Image(r"photos\blockchain_info.png")],
                [sg.Image(r"photos\blockchain2.png", size=(55,55)),sg.Button('Get info about transactions in the chain', button_color = "green",  key='transactions_info', size = (50,2))],
                [sg.Image(r"photos\blockchain2.png", size=(55, 55)), sg.Button('Get block count', button_color="green", key='block_count',size=(50, 2))],
                [sg.Image(r"photos\blockchain2.png", size=(55, 55)), sg.Button('Get mining info', button_color="green", key='mining_info', size=(50, 2))],
                [sg.Image(r"photos\blockchain2.png", size=(55, 55)), sg.Button('Get server uptime', button_color="green", key='uptime', size=(50, 2))],
                [sg.Image(r"photos\other.png")],
                [sg.Image(r"photos\bitcoin.png", size=(55, 55)), sg.Text('Get the Bitcoin price in fiat currencies:')],
                [sg.Button('Exchange rates', key='exchange_rates', size = (50,2))],
                [sg.Image(r"photos\stats.png", size=(55,55)), sg.Text('Get info about block, enter the block height:')],
                [sg.InputText(key='high', size = (50,1))],
                [sg.Button('Get Full statistic', size = (50,2))],
                [sg.Button('Get Basic statistic', size=(50, 2))],
                [sg.Image(r"photos\address.png", size=(55,55)),sg.Text('Enter the Bitcoin address:')],
                [sg.InputText(key='address_input', size = (50,1))],
                [sg.Button('View Full address transaction history', key='history', size = (50,2))],
                [sg.Button('View Basic address transaction history', key='basic_history', size=(50, 2))],
                [sg.Cancel()]
              ]
    return layout


def get_block_count():
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = client.getblockcount()
    data = ''
    data += 'Current block: '+ str(info)
    sg.popup_scrolled(data, title='Current block')

def get_uptime():
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = str(datetime.timedelta(seconds = client.uptime()))
    data = ''
    data += 'Server is up for : ' + str(info)
    sg.popup_scrolled(data, title='Server uptime')

def get_blockchain_difficulty():
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = client.getdifficulty()
    sg.popup(info, title='Bitcoin difficulty')

def get_transactions_statistic():
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = client.getchaintxstats()
    data = ''
    for key, item in info.items():
        data += str(key) + ' : ' + str(item) + '\n'
    sg.popup_scrolled(data, title='Statistics about transactions in the chain')

def get_mining_info():
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = client.getmininginfo()
    data = ''
    for key, item in info.items():
        data += str(key) + ' : ' + str(item) + '\n'
    sg.popup_scrolled(data, title='Mining info')


def get_block_statistic(high):
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = client.getblockstats(high)
    data = ''
    for key, item in info.items():
        data += str(key) + ' : ' + str(item) + '\n'
    sg.popup_scrolled(data, title='Full statistics about block in the chain')

def get_basic_block_statistic(high):
    client = AuthServiceProxy(bitcoin_rpc_client)
    info = client.getblockstats(high)
    data = ''
    for key, item in info.items():
        if (key == 'avgfee' or  key == 'height' or  key == 'blockhash' or  key == 'maxfee' or  key == 'minfee' or  key == 'totalfee'):
            data += str(key) + ' : ' + str(item) + '\n'
    sg.popup_scrolled(data, title='Basic statistics about block in the chain')

def get_exchange_rates():
    ticker = exchangerates.get_ticker()
    dict = {}
    for k in ticker:
        dict[k] = ticker[k].p15min

    data = ''
    for key, item in dict.items():
        data += str(key) + ' : ' + str(item) + '\n'
    sg.popup_scrolled(data, title='Exchange rates')


def get_transaction_history(address):
    h = history(address)
    output_peer_string = ''

    dic = {}
    for index, value in enumerate(h):
        dic[index] = value
    for key, item in dic.items():
        output_peer_string += "Transaction" + str(key+1) + ':' + '\n' + "Address: " + str(item.get("address"))  + '\n' + "Value: " + str(item.get("value"))  + '\n' \
                              + "Output: " + str(item.get("output"))  + '\n' + "Block Height: " + str(item.get("block_height"))  + '\n'+ "Spend: " + str(item.get("spend"))  + '\n'
    sg.popup_scrolled(output_peer_string, title='Full transaction history')

def get_basic_transaction_history(address):
    h = history(address)
    output_peer_string = ''
    dic = {}
    for index, value in enumerate(h):
        dic[index] = value
    for key, item in dic.items():
        output_peer_string += "Transaction " + str(key+1) + ':' + '\n' + "Address:" + str(item.get("address")) + '\n' + "Value:" + str(item.get("value")) + '\n' + "Block Height:" \
                              + str(item.get("block_height")) + '\n'
    sg.popup_scrolled(output_peer_string, title='Basic transaction history')


def get_public_key():
    public_key = privtopub(random_key())

    sg.popup(public_key, title='Public key')


def get_bitcoin_address():
    public_key = privtopub(random_key())
    bitcoin_address = pubtoaddr(public_key)

    sg.popup(bitcoin_address, title='Address')


def main():
    window = sg.Window('BlockExplorer Application', layout(), icon = "C:\search2.ico", size=(1920, 1080), element_justification='center')

    while True:
        event, values = window.read()

        if event in (None, 'Cancel'):
            break
        if event == 'transactions_info':
            get_transactions_statistic()
        if event == 'mining_info':
            get_mining_info()
        if event == 'uptime':
            get_uptime()
        if event == 'block_count':
            get_block_count()
        if event == 'blockchain_difficulty':
            get_blockchain_difficulty()
        if event == 'Get Full statistic':
            get_block_statistic(int(values['high']))
        if event == 'Get Basic statistic':
            get_basic_block_statistic(int(values['high']))
        if event == 'private_key':
            sg.popup(random_key(), title='Private key')
        if event == 'exchange_rates':
            get_exchange_rates()
        if event == 'history':
            get_transaction_history(values['address_input'])
        if event == 'basic_history':
            get_basic_transaction_history(values['address_input'])
        if event == 'public_key':
            get_public_key()
        if event == 'address':
            get_bitcoin_address()

    window.close()


if __name__ == '__main__':
    main()

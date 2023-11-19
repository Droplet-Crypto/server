from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
import requests
from common_types import ActionType, HistoryAction
from constants import COINGECKO_PRICE_API_URL, ERC20_ABI, HTTP_RPC, KNOWN_TOKENS, POLYGONSCAN_BASE_URL, POLYGONSCAN_TOKEN_URL
from eth_utils.address import to_checksum_address
from web3 import Web3, HTTPProvider

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_token_prices() ->  dict[str, float]:
    token_ids = []
    for token_info in KNOWN_TOKENS.values():
        token_ids.append(token_info.coingecko)
    
    response = requests.get(COINGECKO_PRICE_API_URL.format(token_ids=','.join(token_ids)))
    result = response.json()

    token_prices = {}
    print('coingecko response', response.json())

    for token_address, token_info in KNOWN_TOKENS.items():
        token_prices[token_address] = result[token_info.coingecko]['usd']

    return token_prices

@app.get('/accountData/{account_address}')
def get_account_data(account_address: str):
    account_address = to_checksum_address(account_address)
    token_prices = get_token_prices()

    polygonscan_url = POLYGONSCAN_TOKEN_URL.format(account=account_address)
    response = requests.get(polygonscan_url).json()
    result = response['result']

    history: list[HistoryAction] = []
    for transfer_info in result:
        token_address = to_checksum_address(transfer_info['contractAddress'])
        if token_address not in KNOWN_TOKENS:
            continue
        
        token_decimals = int(transfer_info['tokenDecimal'])
        uint_value = int(transfer_info['value'])
        human_amount = uint_value / 10 ** token_decimals
        token_symbol = transfer_info['tokenSymbol']

        action_type: ActionType
        from_address = to_checksum_address(transfer_info['from'])
        if from_address == account_address:
            action_type = 'send'
            message = f'Send {human_amount} {token_symbol}'
        else:
            action_type = 'receive'
            message = f'Receive {human_amount} {token_symbol}'

        tx_hash = transfer_info['hash']
        link = f'{POLYGONSCAN_BASE_URL}/tx/{tx_hash}'
        history.append(HistoryAction(
            action_type=action_type,
            usd_amount=human_amount * token_prices[token_address],
            message=message,
            link=link
        ))

    serialized_history = []
    for action in history:
        serialized_history.append(action.to_json())

    web3 = Web3(HTTPProvider(HTTP_RPC))
    balance = 0
    for token_address, token_info in KNOWN_TOKENS.items():
        token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)  # type: ignore
        uint_balance = token_contract.functions.balanceOf(account_address).call()
        human_balance = uint_balance / 10 ** token_info.decimals
        print(f'{token_info.symbol} balance:', human_balance)
        balance += human_balance * token_prices[token_address]

    formatted_balance = str(int(balance * 100) / 100)  # 2 symbols after floating point
    return {
        'balance': formatted_balance,
        'history': serialized_history,
    }

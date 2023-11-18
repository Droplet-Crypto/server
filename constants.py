import json
from common_types import TokenInfo

development = True

if development:
    POLYGONSCAN_TOKEN_URL = 'https://api-testnet.polygonscan.com/api?module=account&action=tokentx&address={account}&startblock=0&endblock=999999999&page=0&offset=100&sort=desc&apikey=AZYTVXT69HF8Z6T5PQ25C2HP71KFQXBHH9'
    POLYGONSCAN_BASE_URL = 'https://mumbai.polygonscan.com'
    HTTP_RPC = 'https://rpc.ankr.com/polygon_mumbai'
    KNOWN_TOKENS: dict[str, TokenInfo] = {
        '0x1558c6FadDe1bEaf0f6628BDd1DFf3461185eA24': TokenInfo(
            decimals=18,
            symbol='AAVE',
            coingecko='aave',
        ),
        '0x1fdE0eCc619726f4cD597887C9F3b4c8740e19e2': TokenInfo(
            decimals=6,
            symbol='USDT',
            coingecko='tether',
        ),
    }
else:
    POLYGONSCAN_TOKEN_URL = 'https://api.polygonscan.com/api?module=account&action=tokentx&address={account}&startblock=0&endblock=999999999&page=0&offset=100&sort=desc&apikey=AZYTVXT69HF8Z6T5PQ25C2HP71KFQXBHH9'
    POLYGONSCAN_BASE_URL = 'https://polygonscan.com'
    HTTP_RPC = 'https://polygon.llamarpc.com'
    KNOWN_TOKENS: dict[str, TokenInfo] = {}

with open("abi/erc20.json", 'r') as f:
    ERC20_ABI = json.loads(f.read())

COINGECKO_PRICE_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids={token_ids}&vs_currencies=USD&x_cg_demo_api_key=CG-4qSNu9Cz8z3iaJeLsppDGjym'

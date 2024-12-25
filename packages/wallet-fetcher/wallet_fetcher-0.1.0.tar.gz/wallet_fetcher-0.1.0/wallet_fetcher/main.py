import requests
from concurrent.futures import ThreadPoolExecutor

def get_signatures(wallet_address):
    url = "https://api.mainnet-beta.solana.com"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            wallet_address,
            {"limit": 100}
        ]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        signatures_data = response.json()
        return [sig['signature'] for sig in signatures_data.get('result', [])]
    except (requests.exceptions.RequestException, KeyError):
        return []

def fetch_sender(signature):
    url = f'https://api.solana.fm/v0/transfers/{signature}'
    headers = {
        'authority': 'api.solana.fm',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['result']['data'][0]['source']
    except (requests.exceptions.RequestException, KeyError, IndexError):
        return None

def get_senders(wallet_address):
    signatures = get_signatures(wallet_address)
    if not signatures:
        return []

    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_sender, signatures)
        return [result for result in results if result]

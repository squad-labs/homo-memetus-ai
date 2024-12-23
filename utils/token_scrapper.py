import requests
import json

urls = [
  'https://api.dexscreener.com/token-profiles/latest/v1',
  'https://api.dexscreener.com/token-boosts/latest/v1',
  'https://api.dexscreener.com/token-boosts/top/v1'
]

def get_only_solana(tokens):
  return list(filter(lambda x: x['chainId'] == 'solana', tokens))

def main():
  total_data = []
  try:
    for url in urls:
      response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
      })

      if response.status_code == 200:
        data = get_only_solana(response.json())
        total_data.extend(data)

    unique_data = list({d['tokenAddress']: d for d in total_data}.values())
    with open("data.json", "w", encoding="utf-8") as json_file:
      json.dump(unique_data, json_file, ensure_ascii=False, indent=2)
  except Exception as e:
    print(f"Error: {e}")
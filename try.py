import requests

ALPHA_VANTAGE_API_KEY = "ZUTMJQV502645BUD"

url = f'https://www.alphavantage.co/query?function=BRENT&interval=weekly&apikey={ALPHA_VANTAGE_API_KEY}'
r = requests.get(url)
data = r.json()

print(data)
import requests

#request to coinMarketCap
def price():
    url = 'http://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start' : '1',
        'limit' : '100',
        'convert' : 'USD'
    }
    headers = {
        'accept' :'application/json',
        'X-CMC_PRO_API_KEY': '002eb6c7-22c2-41b1-9fdd-d2bf5375da4e'
    }

    r = requests.get(url = url , params = params, headers = headers).json()

    bitcoin = r['data'][0]

    price = round(bitcoin['quote']['USD']['price'],2)
    return price


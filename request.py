import requests

url = 'https://us-central1-swamphacksvi-266915.cloudfunctions.net/gather'

response = requests.get(url)
json = response.json()
print(json)

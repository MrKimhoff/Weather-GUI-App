import json
import requests
import pprint

response = requests.get('http://api.open-notify.org/astros.json')

print(f'Response {response}')
print(f'Content {response.content}')
print(f'Headers Type {type(response.headers)}')

pprint.pprint(response.json())

json_string = response.text

json_dict = json.loads(json_string)

# pprint.pprint(iss_list)

for key in json_dict:
    print('Key: {} Value: {}'.format(key, json_dict[key]))


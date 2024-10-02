import requests
import json


url = "http://127.0.0.1:8888/productionplan"

# Cargar el payload desde el archivo json
with open('C:\\Users\\guill\\OneDrive\\Desktop\\engie_proyecto\\payload3.json', 'r') as file:
    payload = json.load(file)


response = requests.post(url, json=payload)

# Verificar el código de estado de la respuesta
print(f"Status Code: {response.status_code}")

# Mostrar la respuesta en formato json
print(f"Response: {response.json()}")

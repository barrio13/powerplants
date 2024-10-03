from flask import Flask, request, jsonify


app = Flask(__name__)

# Función para calcular el merit order.
def calcular_costo(plant, fuels):
    if plant["type"] == "windturbine":
        return 0 
    elif plant["type"] == "gasfired":
        return (1 / plant["efficiency"])*fuels["gas(euro/MWh)"] + fuels["co2(euro/ton)"]*0.3
    elif plant["type"] == "turbojet":
        return (1 / plant["efficiency"])*fuels["kerosine(euro/MWh)"]
    
# Función para calcular la producción.
def calcular_produccion(payload):
    load = payload["load"]
    fuels = payload["fuels"]
    powerplants = payload["powerplants"]

    # Ponemos la carga de cada planta a 0.
    for plant in powerplants:
        plant["cost"] = calcular_costo(plant, fuels)
        plant["power"] = 0

    # Ordenar las plantas
    powerplants = sorted(powerplants, key=lambda x: x["cost"])
    

    # Asignar load a las plantas eólicas.
    for plant in powerplants:
        if plant['type'] == 'windturbine':
            power_eol = round((plant['pmax']*fuels['wind(%)'])/100,1)
            if power_eol > load:
                plant['power'] = round(load,1)
                load = 0
            else:
                plant['power'] = power_eol
                load -= plant['power']

    
    prev_plant = None

    # Asignar load al resto de plantas.
    for plant in powerplants:
        if plant['type'] == 'windturbine':
            continue
        if load <= 0:
            break
        if load < plant['pmin']:               # En el caso de que la carga restante sea más pequeña que el pmin, asignamos el pmin y restamos la diferencia a la planta anterior 
            d = plant['pmin'] - load
            plant['power'] = plant['pmin']
            if prev_plant:
                prev_plant['power'] -= d
            load = 0
        else:
            if load <= plant['pmax']:
                plant['power'] = round(load, 1)
                load = 0
            else:
                plant['power'] = round(plant['pmax'], 1)
                load -= plant['power']
        prev_plant = plant
 
     
    return [{"name": plant["name"], "p": round(plant["power"], 1)} for plant in powerplants]


@app.route('/productionplan', methods=['POST'])
def production_plan():
    payload = request.get_json()
    plan = calcular_produccion(payload)

    return jsonify(plan), 200

if __name__ == "__main__":
    app.run(port=8888, debug=True)



import json
import folium

# Carregando os dados do arquivo JSON
with open("bus_data.json", "r") as file:
    bus_data = json.load(file)

# Criando um mapa com a correção nas coordenadas (inverter latitude e longitude)
map_center_corrected = [-7.135721432647074, -34.882950003653825]
bus_map_corrected = folium.Map(
    location=map_center_corrected, zoom_start=13, tiles="cartodbpositron"
)

# Adicionando as rotas de ônibus ao mapa com as coordenadas corretamente invertidas
for bus_line in bus_data:
    # Convertendo a string JSON do campo 'geojson' em um objeto Python
    geojson_data = json.loads(bus_line["geojson"]) if "geojson" in bus_line else None

    if geojson_data and "features" in geojson_data:
        for feature in geojson_data["features"]:
            if feature["geometry"]["type"] == "LineString":
                # Invertendo as coordenadas (latitude e longitude)
                corrected_coordinates = [
                    (coord[1], coord[0]) for coord in feature["geometry"]["coordinates"]
                ]
                folium.PolyLine(
                    locations=corrected_coordinates,
                    color="red",  # Cor vermelha para destaque
                    weight=8,  # Espessura maior para destaque
                    opacity=0.9,  # Opacidade alta para destaque
                    popup=f"Linha: {bus_line['linha']}",  # Popup com o nome da linha
                ).add_to(bus_map_corrected)

# Mostrando o mapa corrigido
bus_map_corrected

# Mostrando o mapa
bus_map_corrected.show_in_browser()

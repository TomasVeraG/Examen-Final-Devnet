import requests
import urllib.parse

# --- CONFIGURACIÓN ---
key = "d8ab0aab-9ebe-4f7d-95d5-ebaea4ab22e1"

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"

def get_location(city):
    """Obtiene latitud, longitud y nombre formateado de una ciudad"""
    url = f"{geocode_url}q={urllib.parse.quote(city)}&limit=1&key={key}"
    try:
        response = requests.get(url)
        json_data = response.json()
        
        if response.status_code == 200 and json_data["hits"]:
            lat = json_data["hits"][0]["point"]["lat"]
            lng = json_data["hits"][0]["point"]["lng"]
            name = json_data["hits"][0]["name"]
            country = json_data["hits"][0]["country"]
            return lat, lng, name, country
        else:
            return None, None, None, None
    except:
        return None, None, None, None

def main():
    print("--------------------------------------------------")
    print("      SISTEMA DE VIAJES CHILE - ARGENTINA         ")
    print("--------------------------------------------------")
    
    while True:
        print("\n(Escribe 'v' en cualquier momento para salir)")
        
        # 1. Ciudad de Origen
        orig = input("Ciudad de Origen (Chile): ")
        if orig.lower() == "v":
            print("¡Hasta luego!")
            break

        # 2. Ciudad de Destino
        dest = input("Ciudad de Destino (Argentina): ")
        if dest.lower() == "v":
            print("¡Hasta luego!")
            break

        # 3. Validar ciudades
        lat1, lng1, name1, country1 = get_location(orig)
        lat2, lng2, name2, country2 = get_location(dest)

        if not name1 or not name2:
            print("Error: No se pudo encontrar una de las ciudades. Intente nuevamente.")
            continue

        print(f"\nRuta identificada: {name1} ({country1}) -> {name2} ({country2})")

        # 4. Medio de transporte
        print("Medios disponibles: car, bike, foot")
        vehicle = input("Medio de transporte: ")
        if vehicle.lower() == "v":
            print("¡Hasta luego!")
            break
            
        if vehicle not in ['car', 'bike', 'foot']:
            print("Transporte no válido, se usará 'car' por defecto.")
            vehicle = 'car'

        # 5. Calcular Ruta
        r_url = f"{route_url}point={lat1},{lng1}&point={lat2},{lng2}&vehicle={vehicle}&key={key}&locale=es"
        
        try:
            resp = requests.get(r_url)
            data = resp.json()

            if resp.status_code == 200 and "paths" in data:
                path = data["paths"][0]
                dist_m = path["distance"]
                time_ms = path["time"]

                # Conversiones
                km = dist_m / 1000
                miles = km * 0.621371
                
                seconds = int(time_ms / 1000)
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                sec = seconds % 60

                print(f"\n>>> RESULTADOS DEL VIAJE <<<")
                print(f"Distancia: {km:.2f} km")
                print(f"Distancia: {miles:.2f} millas")
                print(f"Duración:  {hours:02} horas, {minutes:02} minutos, {sec:02} segundos")
                
                print("\n>>> NARRATIVA DEL VIAJE <<<")
                # Mostramos solo las primeras 5 instrucciones para no saturar la pantalla
                # pero indicamos que hay más.
                instructions = path["instructions"]
                for i in range(min(5, len(instructions))):
                    instr = instructions[i]
                    print(f"- {instr['text']} ({instr['distance']/1000:.2f} km)")
                
                if len(instructions) > 5:
                    print(f"... y {len(instructions)-5} instrucciones más.")
            else:
                print("Error al calcular la ruta (posiblemente no hay camino en ese transporte).")
        except:
            print("Error de conexión con la API.")

if __name__ == "__main__":
    main()
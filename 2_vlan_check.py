def verificar_vlan(vlan_id):
    if 1 <= vlan_id <= 1005:
        return "Rango Normal"
    elif 1006 <= vlan_id <= 4094:
        return "Rango Extendido"
    else:
        return "No corresponde a una VLAN respectiva"

try:
    vlan = int(input("Ingrese el número de VLAN: "))
    resultado = verificar_vlan(vlan)
    print(f"La VLAN {vlan} corresponde a: {resultado}")
except ValueError:
    print("Error: Por favor ingrese un número entero válido.")
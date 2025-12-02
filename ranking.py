import csv
import os


RANKING_FILE = "ranking.csv"
MAX_JUGADORES = 10



def es_numero(texto):
    """
    Devuelve True si es un número decimal válido, False si no lo es.

    """
    if texto.count(".") > 1:
        return False

    # Caso: solo contiene dígitos o un punto
    partes = texto.split(".")

    # Parte entera debe ser solo números
    if not partes[0].isdigit():
        return False

    # Si tiene decimales, también deben ser números
    if len(partes) == 2 and not partes[1].isdigit():
        return False

    return True



# Crear archivo si no existe

def crear_archivo_si_no_existe():
    if not os.path.exists(RANKING_FILE):
        f = open(RANKING_FILE, "w", newline="", encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow(["nombre", "tiempo", "dibujo"])
        f.close()



# Leer archivo

def cargar_datos_csv():
    crear_archivo_si_no_existe()

    f = open(RANKING_FILE, "r", encoding="utf-8")
    reader = csv.DictReader(f)
    datos = list(reader)
    f.close()

    return datos



def convertir_datos_a_ranking(datos):
    ranking = []

    for fila in datos:
        texto_tiempo = fila["tiempo"]

        # Validar número sin try
        if es_numero(texto_tiempo) is False:
            continue  # ignora filas no válidas

        tiempo = float(texto_tiempo)

        ranking.append({
            "nombre": fila["nombre"],
            "tiempo": tiempo,
            "dibujo": fila.get("dibujo", "")
        })

    ranking.sort(key=lambda x: x["tiempo"])
    return ranking[:MAX_JUGADORES]



# Ranking final

def leer_ranking():
    datos = cargar_datos_csv()
    ranking = convertir_datos_a_ranking(datos)
    return ranking



# Guardar ranking

def guardar_en_ranking(nombre, tiempo, dibujo):
    ranking = leer_ranking()

    ranking.append({
        "nombre": nombre,
        "tiempo": tiempo,
        "dibujo": dibujo
    })

    ranking.sort(key=lambda x: x["tiempo"])
    ranking = ranking[:MAX_JUGADORES]

    f = open(RANKING_FILE, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(f, fieldnames=["nombre", "tiempo", "dibujo"])
    writer.writeheader()
    writer.writerows(ranking)
    f.close()

import csv
import os

def generaArchivo(arr, name):
    file = open(name,'w')
    for key, values in arr.items():
        file.write(key +","+str(values) + '\n')
def lectura():
    archivo = []
    f = open('../valores_actuales.csv', 'r')
    for line in f:
        archivo.append((line.strip(',').split(',')))
    for linea in archivo:
        linea.pop(0)
        linea.pop(len(linea)-1)
    for i in range(len(archivo)):
        for j in range(len(archivo[i])):
            archivo[i][j] = float(archivo[i][j])
    return archivo
def lecturaArchivo(name):
    diccionario = {}
    with open(name,'r') as f:
        reader = csv.reader(f)
        for line in reader:
            diccionario[line[0]] = list(map(float , line[1:]))
    return diccionario

def actualizar_csv(nuevos_resultados, nombre_archivo="resultados_combinados.csv"):
    datos_actuales = {}
    # Si el archivo ya existe, lo leemos y convertimos los datos en listas
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode="r", newline="") as f:
            reader = csv.reader(f)
            for fila in reader:
                metrica = fila[0]
                valores = list(map(float, fila[1:]))  # convertimos a números
                datos_actuales[metrica] = valores

    # Ahora actualizamos los datos
    for metrica, nuevo_valor in nuevos_resultados.items():
        if metrica in datos_actuales:
            datos_actuales[metrica].append(nuevo_valor)
        else:
            datos_actuales[metrica] = [nuevo_valor]

    # Guardamos los datos actualizados
    with open(nombre_archivo, mode="w", newline="") as f:
        writer = csv.writer(f)
        # Escribimos cabecera dinámica según cuántos valores tenga la métrica más larga
        max_length = max(len(v) for v in datos_actuales.values())

        for metrica, valores in datos_actuales.items():
            writer.writerow([metrica] + valores)
def data():
    rangosdeServicios = {
        "Temperatura": [15, 39],
        "Humedad": [60, 90],
        "Ruido": [30, 90],
        "Luminosidad": [100, 500]
    }
    return rangosdeServicios
if __name__ == '__main__':
    archivo = lecturaArchivo("EDA.csv")
    print(archivo)

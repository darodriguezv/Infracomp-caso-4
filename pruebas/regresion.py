import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

carpeta_resultados = "resultados"

if not os.path.exists(carpeta_resultados):
    print(f"La carpeta {carpeta_resultados} no existe.")
else:
    archivos = os.listdir(carpeta_resultados)

    archivos_csv = [f for f in archivos if f.startswith('results') and f.endswith('.csv')]

    archivos_csv.sort(key=lambda x: int(x.split('results')[1].split('.csv')[0]))

    if len(archivos_csv) == 0:
        print("No se encontraron archivos CSV en la carpeta.")
    else:
        solicitudes_totales = []
        solicitudes_mas_3_segundos = []

        for archivo in archivos_csv:
            ruta_archivo = os.path.join(carpeta_resultados, archivo)
            
            print(f"Procesando archivo: {archivo}")

            df = pd.read_csv(ruta_archivo, header=None)

            ultima_columna = df.shape[1] - 1

            df = df.dropna(subset=[0, ultima_columna])  

            df[0] = pd.to_numeric(df[0], errors='coerce')
            df[ultima_columna] = pd.to_numeric(df[ultima_columna], errors='coerce')

            solicitudes_mas_3 = df[df[ultima_columna] > 3000] 

            solicitudes_totales.append(len(df))
            solicitudes_mas_3_segundos.append(len(solicitudes_mas_3))

        X = np.array(solicitudes_totales).reshape(-1, 1)
        y = np.array(solicitudes_mas_3_segundos)

        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)

        coeficiente = model.coef_[0]
        interseccion = model.intercept_

        print(f"Coeficiente de regresión (pendiente): {coeficiente}")
        print(f"Intersección (ordenada al origen): {interseccion}")

        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.scatter(solicitudes_totales, solicitudes_mas_3_segundos, color='blue', label='Datos Reales')
        plt.plot(solicitudes_totales, y_pred, color='red', label='Regresión Lineal')

        plt.xlabel('Solicitudes Totales')
        plt.ylabel('Solicitudes > 3 segundos')
        plt.title('Regresión Lineal: Solicitudes Totales vs Solicitudes > 3 segundos')

        plt.legend()

        plt.tight_layout()
        plt.show()

import os
import pandas as pd
import matplotlib.pyplot as plt

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
        nombres_archivos = []
        solicitudes_totales = []
        solicitudes_mas_3_segundos = []
        porcentaje_mas_3_segundos = []

        for archivo in archivos_csv:
            ruta_archivo = os.path.join(carpeta_resultados, archivo)
            
            print(f"Procesando archivo: {archivo}")

            df = pd.read_csv(ruta_archivo, header=None)

            ultima_columna = df.shape[1] - 1

            df = df.dropna(subset=[0, ultima_columna])

            df[0] = pd.to_numeric(df[0], errors='coerce')
            df[ultima_columna] = pd.to_numeric(df[ultima_columna], errors='coerce')

            solicitudes_mas_3 = df[df[ultima_columna] > 3000] 

            porcentaje = (len(solicitudes_mas_3) / len(df)) * 100 if len(df) > 0 else 0

            nombres_archivos.append(archivo)
            solicitudes_totales.append(len(df))
            solicitudes_mas_3_segundos.append(len(solicitudes_mas_3))
            porcentaje_mas_3_segundos.append(porcentaje)

        fig, ax = plt.subplots(figsize=(10, 6))

        x = range(len(nombres_archivos))

        ax.bar(x, solicitudes_totales, label='Solicitudes Totales', color='b', alpha=0.6)
        ax.bar(x, solicitudes_mas_3_segundos, label='Solicitudes > 3 segundos', color='r', alpha=0.6)

        for i in range(len(nombres_archivos)):
            ax.text(x[i], solicitudes_totales[i] + 5, f"{porcentaje_mas_3_segundos[i]:.2f}%", 
                    ha='center', va='bottom', color='black', fontsize=9)

        ax.set_xlabel('Archivos')
        ax.set_ylabel('Número de Solicitudes')
        ax.set_title('Solicitudes Totales vs Solicitudes > 3 segundos por Test')

        ax.set_xticks(x)
        ax.set_xticklabels(nombres_archivos, rotation=45, ha='right')

        ax.legend()

        plt.tight_layout()
        plt.show()

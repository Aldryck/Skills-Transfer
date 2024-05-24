import os
import pandas as pd 
import numpy as np

write_name = input("Write how you want to name the file\n")
features_file_name = ("C:/Users/Owner/Skill Transfer/Features/Saved data/{0}_Features.csv".format(write_name))
# Especifica la ruta completa de la carpeta que contiene los archivos CSV
read_file = 'C:/Users/Owner/Skill Transfer/EMG Data/Read data'

# Paso 1: Obtener la lista de archivos CSV en la carpeta especificada
csv_files = [file for file in os.listdir(read_file) if file.endswith('.csv')]

# Paso 2: Procesar cada archivo CSV
dataframes = []
for file in csv_files:
    # Cargar el archivo CSV
    archivo_csv = os.path.join(read_file, file)
    data = pd.read_csv(archivo_csv)

    # Iterar por el DataFrame en grupos de 20 filas
    for i in range(0, len(data), 10):
        segment = data[i:i+10]

        if not segment.empty:
            # Obtener los datos del DataFrame
            datos1 = segment['s1'].values
            datos2 = segment['s2'].values
            label = segment.iloc[0, -1]

            # Calcular las características
            media_signal1 = np.mean(datos1)
            desviacion_estandar_signal1 = np.std(datos1)
            rms_signal1 = np.sqrt(np.mean(datos1**2))
            media_signal2 = np.mean(datos2)
            desviacion_estandar_signal2 = np.std(datos2)
            rms_signal2 = np.sqrt(np.mean(datos1**2))

            # Crear un nuevo DataFrame con las características
            features = pd.DataFrame({
                'Media_Signal1': [media_signal1],
                'Standard_Deviation_Signal1': [desviacion_estandar_signal1],
                'RMS_Signal1': [rms_signal1],
                'Media_Signal2': [media_signal2],
                'Standard_Deviation_Signal2': [desviacion_estandar_signal2],
                'RMS_Signal2': [rms_signal2],
                'Label': [label]
            })

            dataframes.append(features)

# Paso 3: Combinar los dataframes en uno solo
features = pd.concat(dataframes, ignore_index=True)

# Paso 4: Guardar el DataFrame en un archivo CSV
features.to_csv(features_file_name, index=False)
print("\nThe data has been successfully saved in", features_file_name)

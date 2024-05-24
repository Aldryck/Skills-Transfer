import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Paso 1: Cargar el archivo CSV con las características y las etiquetas
file_name = 'Aldryck_Features.csv'
features = pd.read_csv('C:/Users/Owner/Skill Transfer/Features/Read data/{0}'.format(file_name))

# Paso 2: Dividir los datos en características (X) y etiquetas (y)
X = features[['Media_Signal1', 'Standard_Deviation_Signal1', 'RMS_Signal1', 'Media_Signal2', 'Standard_Deviation_Signal2', 'RMS_Signal2']]
y = features['Label']

# Paso 3: Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de Árbol de Decisión
# Crear y entrenar el modelo de Árbol de Decisión
tree_model = DecisionTreeClassifier()
tree_model.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred_tree = tree_model.predict(X_test)

# Calcular la precisión del modelo
accuracy_tree = accuracy_score(y_test, y_pred_tree)
print("Precisión del modelo de Árbol de Decisión: {:.2f}".format(accuracy_tree))

# Modelo SVM
# Crear y entrenar el modelo SVM
svm_model = SVC()
svm_model.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred_svm = svm_model.predict(X_test)

# Calcular la precisión del modelo
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print("Precisión del modelo SVM: {:.2f}".format(accuracy_svm))

# Modelo de Random Forest
# Crear y entrenar el modelo de Random Forest
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred_rf = rf_model.predict(X_test)

# Calcular la precisión del modelo
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print("Precisión del modelo de Random Forest: {:.2f}".format(accuracy_rf))

# Guardar el modelo con mejor precisión en un archivo pkl
best_model = None
if accuracy_tree >= accuracy_svm and accuracy_tree >= accuracy_rf:
    best_model = tree_model
    model_name = 'decision_tree_model.pkl'
elif accuracy_svm >= accuracy_tree and accuracy_svm >= accuracy_rf:
    best_model = svm_model
    model_name = 'svm_model.pkl'
else:
    best_model = rf_model
    model_name = 'random_forest_model.pkl'

joblib.dump(best_model, model_name)
print("Se ha guardado el modelo con mejor precisión en un archivo pkl:", model_name)
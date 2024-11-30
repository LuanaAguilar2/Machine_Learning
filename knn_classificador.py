import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Função para treinar o modelo KNN
def treinar_knn():
    # Carregar o arquivo CSV com os dados de treinamento
    data = pd.read_csv('./src/assets/data/pontuacao_classificacao.csv')

    # Separar as características (respostas) e o rótulo (nível)
    X = data.drop('Nível', axis=1) # Recebe todas as colunas, menos a última
    y = data['Nível'] # Recebe a última coluna, que é a coluna Nível (classificação do usuário: Júnior, Pleno, Sênior)
    
    # Dividir o conjunto de dados em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Normalizar as características para melhorar o desempenho do KNN
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Treinar o modelo KNN com k=3
    knn_classificador = KNeighborsClassifier(n_neighbors=3)
    knn_classificador.fit(X_train_scaled, y_train)

    # Avaliar a acurácia do modelo
    y_pred = knn_classificador.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print("\nAccuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    exibir_matrix_confusao(y_test, y_pred)

    return knn_classificador, scaler

# Função para prever o nível com base na pontuação
def prever_nivel(knn_classificador, scaler, pontuacao_usuario):
    # Normalizar a pontuação do usuário para prever
    pontuacao_normalizada = scaler.transform([pontuacao_usuario])
    nivel_previsto = knn_classificador.predict(pontuacao_normalizada)
    return nivel_previsto[0]

def exibir_matrix_confusao(y_test, y_pred):
  # Calculando a matriz de confusão
  cm = confusion_matrix(y_test, y_pred)

  # Obtendo os valores da matriz de confusão
  #tn, fp, fn, tp = cm.ravel()

  # Plotando a matriz de confusão
  sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, square=True)
  plt.xlabel('Valor Previsto')
  plt.ylabel('Valor Real')
  plt.title('Matriz de Confusão')
  plt.show()
# Utilise Python 3.10 comme base
FROM python:3.10

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier requirements.txt
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code du projet
COPY . .

# Lance l'application
CMD ["python", "src/app.py"]


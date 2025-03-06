# Utilisation d'une image de base avec Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /usr/src/app

# Copier le fichier requirements.txt
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet Django
COPY . .

# Exposer le port utilisé par Django
EXPOSE 8000

# Démarrer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

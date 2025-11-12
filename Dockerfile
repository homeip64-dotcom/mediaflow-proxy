FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# On définit la variable d'environnement ici
ENV API_PASSWORD=skystrem-support1@2mail.co

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

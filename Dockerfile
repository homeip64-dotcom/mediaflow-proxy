FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .

ENV API_PASSWORD=skystrem-support1@2mail.co

EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.9-slim

WORKDIR /app

COPY lexicalAnalyser.py .

ENTRYPOINT ["python", "lexicalAnalyser.py"]

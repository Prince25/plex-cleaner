FROM python:3.11-slim
WORKDIR /plex-cleaner
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "main.py"]

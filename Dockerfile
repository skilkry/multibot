# Usa una imagen de Python 3.11 sobre Debian slim
FROM python:3.11-slim

#Actualiza e instala paquetes, -y para no necesitar verificación
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    ffmpeg \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

#crea el directorio /app para trabajar
WORKDIR /app

#copia el archivo de requerimientos de local al docker
COPY requirements.txt .

# Instala los paquetes listados en requirements.txt sin usar la caché de pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos del proyecto al docker
COPY . .

## Ejecuta el bot de Telegram al iniciar el docker
CMD ["python3", "telegram_bot.py"]
# Bot Multifunción para Telegram (Python + Docker)

Este repositorio contiene el código de un bot de Telegram modular y extensible, diseñado para realizar tareas de automatización complejas. El proyecto está construido con un enfoque en el código limpio, la mantenibilidad y las prácticas modernas de DevOps, incluyendo la containerización con Docker para un despliegue sencillo.

## Funcionalidades Actuales (Módulos v1.0)

* ** Lector de OCR:** El bot es capaz de recibir una imagen (como una factura o un recibo), procesarla con un motor de OCR (Tesseract) y devolver el texto extraído. El módulo incluye pasos de preprocesamiento de imagen (escala de grises, autocontraste) para maximizar la precisión.

* ** Descargador de Contenido Universal:** A través de un comando `/descargar`, el bot puede recibir una URL de cientos de sitios (YouTube, X, TikTok etc.) y descargar el vídeo correspondiente usando la librería`yt-dlp`. Incluye una lógica de **compresión de vídeo inteligente con `ffmpeg`** que ajusta el bitrate para asegurar que el archivo final no supere el límite de 50MB de Telegram.

## Stack Tecnológico

* **Lenguaje:** Python 3.11+
* **Framework de Bot:** `aiogram`
* **Procesamiento de Imagen y OCR:** `Pillow`, `pytesseract`
* **Descarga de Contenido:** `yt-dlp`
* **Procesamiento de Vídeo:** `ffmpeg` (a través de `subprocess`)
* **DevOps:** Docker

## Arquitectura Modular

El proyecto está diseñado para ser fácilmente extensible. La lógica principal del bot (`main_bot.py`) actúa como un "orquestador", manejando la comunicación con la API de Telegram. Cada funcionalidad principal reside en su propio módulo aislado dentro de la carpeta `bots/`, permitiendo añadir nuevos "superpoderes" al bot sin modificar el código central.

```
/skilkry-bot/
├── bots/
│   ├── ocr_reader.py
│   └── content_downloader.py
│
├── downloads/              # Carpeta para descargas temporales
├── .env                    # Archivo para secretos (API Token)
├── .gitignore
├── Dockerfile              # Receta para la containerización
├── main_bot.py             # Orquestador principal del bot
└── requirements.txt        # Dependencias de Python
```

## Configuración y Despliegue

Este bot está diseñado para ser desplegado fácilmente en cualquier plataforma que soporte Docker.

### 1. Requisitos Previos

* Docker Desktop instalado.
* Un token de bot de Telegram.

### 2. Configuración Local

1.  Clona el repositorio.
2.  Crea un archivo `.env` en la raíz del proyecto y añade tu token:
    ```
    TELEGRAM_TOKEN="AQUI_VA_TU_TOKEN"
    ```
3.  (Opcional, para desarrollo local sin Docker) Crea un entorno virtual e instala las dependencias:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### 3. Despliegue con Docker

El método recomendado para ejecutar este bot es a través de Docker.

1.  **Construir la imagen de Docker:**
    Desde la carpeta raíz del proyecto, ejecuta:
    ```bash
    docker build -t skilkry-bot:latest .
    ```

2.  **Ejecutar el contenedor:**
    El bot leerá el token del archivo `.env` local.
    ```bash
    docker run --rm -it --env-file .env skilkry-bot:latest
    ```
    El bot se iniciará y empezará a escuchar los mensajes de Telegram.

## Hoja de Ruta (Próximas Features)

* [ ] **Persistencia de Datos:** Integración con una base de datos SQLite para guardar un historial de tareas.
* [ ] **Despliegue Automatizado (CI/CD):** Creación de un workflow con GitHub Actions para construir y desplegar automáticamente la imagen de Docker en un servicio en la nube (ej. Railway.app).
* [ ] **Nuevo Módulo:** Resumen inteligente de correos electrónicos.
````

import yt_dlp
import logging
from pathlib import Path
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def compress_video_to_target_size(input_path: str, output_path: str, target_mb=48):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", input_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    duration = float(result.stdout)

    target_bitrate = (target_mb * 8192) / duration
    video_bitrate = target_bitrate - 128

    command = [
        "ffmpeg",
        "-i", input_path,
        "-b:v", f"{int(video_bitrate)}k",
        "-b:a", "128k",
        "-c:v", "libx264",
        "-preset", "fast",
        output_path
    ]
    subprocess.run(command, check=True)

    final_size = Path(output_path).stat().st_size / (1024 * 1024)
    logging.info(f"Archivo comprimido final: {final_size:.2f} MB")

def download_media(url: str) -> dict:
    formats_to_try = [
        'bv*+ba/best[ext=mp4]/best',
        'best[ext=mp4]/best',
        'best'
    ]

    try:
        logging.info(f"Procesando URL: {url}")
        for fmt in formats_to_try:
            ydl_opts = {
                'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
                'format': fmt,
                'noplaylist': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    filename = ydl.prepare_filename(info_dict)

                    logging.info(f"Iniciando descarga con formato: {fmt}")
                    ydl.download([url])
                break
            except Exception as e:
                logging.warning(f"Error con formato '{fmt}': {e}")
                continue
        else:
            raise Exception("No se pudo descargar el video con ningún formato")

        size_mb = Path(filename).stat().st_size / (1024 * 1024)
        logging.info(f"Tamaño del archivo descargado: {size_mb:.2f} MB")

        if size_mb > 49:
            compressed_path = str(DOWNLOAD_DIR / f"compressed_{Path(filename).name}")
            logging.info("Archivo muy grande, comprimiendo...")
            compress_video_to_target_size(filename, compressed_path)
            Path(filename).unlink()
            filename = compressed_path

        return {
            "status": "success",
            "filepath": filename,
            "title": info_dict.get('title', 'Sin título')
        }

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error al descargar: {error_message}")
        return {
            "status": "error",
            "message": error_message
        }

if __name__ == '__main__':
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = download_media(test_url)

    print("\n--- RESULTADO DE LA DESCARGA ---")
    if result["status"] == "success":
        print(f" Título: {result['title']}")
        print(f" Guardado en: {result['filepath']}")
    else:
        print(f" Error: {result['message']}")
    print("--------------------------------\n")

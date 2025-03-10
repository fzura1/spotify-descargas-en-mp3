import os
import subprocess

def download_music(url):
    downloads_folder = os.path.join(os.getcwd(), "descargas")
    os.makedirs(downloads_folder, exist_ok=True)
    
    try:
        subprocess.run(["spotdl", url, "--output", os.path.join(downloads_folder, "{title}.mp3")], check=True)
        print(f"✅ Descarga completada. Archivos guardados en: {downloads_folder}")
    except subprocess.CalledProcessError:
        print("❌ Error al descargar la canción. Verifica el enlace y tu conexión a internet.")

if __name__ == "__main__":
    while True:
        song_url = input("🎵 Ingresa el enlace de la canción o playlist de Spotify (o escribe 'salir' para terminar): ")
        if song_url.lower() == 'salir':
            break
        download_music(song_url)

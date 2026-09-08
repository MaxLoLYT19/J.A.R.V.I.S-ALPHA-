import asyncio
import edge_tts
import pygame
import os

# Lista de voces en español excelentes:
# "es-ES-AlvaroNeural" (Hombre, España - tono formal muy estilo asistente)
# "es-MX-JorgeNeural"
# "en-US-BrianNeural" (Si prefieres el Jarvis original en inglés)
VOZ = "es-MX-JorgeNeural"

async def generar_audio(texto, archivo_salida="voz_jarvis.mp3"):
    comunicador = edge_tts.Communicate(texto, VOZ)
    await comunicador.save(archivo_salida)

def hablar(texto):
    print(f"Jarvis: {texto}")
    archivo = "voz_temporal.mp3"

    # Generamos el audio con la voz neuronal
    asyncio.run(generar_audio(texto, archivo))

    # Reproducimos el archivo generado
    pygame.mixer.init()
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

    # Limpieza del archivo temporal
    if os.path.exists(archivo):
        os.remove(archivo)

if __name__ == "__main__":
    hablar("Hola. Los sistemas principales están completamente operativos.")
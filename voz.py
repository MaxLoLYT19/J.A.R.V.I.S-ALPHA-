import edge_tts
import asyncio
import os
import pygame

# Tu voz configurada
VOZ_JARVIS = "es-MX-JorgeNeural" 

def hablar(texto):
    pygame.mixer.init()
    
    # 1. REPRODUCIR EL SONIDO DE SISTEMA (BIP)
    try:
        # Carga y reproduce el sonido de tu carpeta
        pygame.mixer.music.load("beep.mp3")
        pygame.mixer.music.play()
        
        # Esperamos a que termine el bip corto antes de seguir
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception:
        # Si se te olvida poner el archivo beep.mp3, el código no se rompe, solo sigue adelante
        pass 
        
    # 2. GENERAR LA RESPUESTA DE JARVIS
    async def _generar_audio():
        comunicador = edge_tts.Communicate(texto, VOZ_JARVIS)
        await comunicador.save("temp_jarvis.mp3")
        
    asyncio.run(_generar_audio())
    
    # 3. REPRODUCIR LA VOZ
    try:
        pygame.mixer.music.load("temp_jarvis.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error reproduciendo voz: {e}")
        
    # Limpieza de archivos temporales
    pygame.mixer.quit()
    try:
        os.remove("temp_jarvis.mp3")
    except:
        pass
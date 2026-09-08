import google.generativeai as genai
import os
import pywhatkit
import webbrowser
import subprocess
import sys
from dotenv import load_dotenv

# Importamos las funciones de tus otros archivos
from oido import escuchar
from voz import hablar

# Configuración de seguridad y validación
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Validación para evitar errores si tu amigo olvida el archivo .env
if not API_KEY:
    # Mostramos el mensaje en consola por si la voz falla
    print("\n[ERROR CRÍTICO] Falta la clave de la API.")
    print("Por favor, asegúrate de haber creado el archivo .env con la variable GEMINI_API_KEY.")
    
    # Intentamos que Jarvis avise por voz antes de cerrarse
    try:
        hablar("Error crítico. No encontré la clave de la API en el archivo de configuración. Por favor, asegúrate de que el archivo punto env exista.")
    except:
        pass
    
    # Detenemos el programa limpiamente
    sys.exit()

# Si la clave existe, configuramos Gemini
genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    system_instruction="Eres Jarvis, un asistente virtual avanzado. Sé muy conciso, directo y conversacional. No uses asteriscos, negritas ni listas largas."
)

def pensar_y_responder(texto_usuario):
    print("🧠 Jarvis está pensando...")
    return modelo.generate_content(texto_usuario).text

# El bucle principal actualizado
if __name__ == "__main__":
    hablar("Sistemas en línea. Conexión neuronal establecida.")
    
    while True:
        comando = escuchar()
        
        if comando == "":
            continue 
            
        # Jarvis se apagará si detecta cualquiera de estas palabras clave
        if "apágate" in comando or "salir" in comando or "apagar" in comando:
            hablar("Apagando sistemas. Hasta luego.")
            break   
            
        # --- HABILIDADES DE CONTROL DE PC (Modificadas para portabilidad) ---
        
        # 1. Reproducir música o videos en YouTube
        elif "reproduce" in comando:
            cancion = comando.replace("reproduce", "").strip()
            hablar(f"Enseguida. Reproduciendo {cancion} en YouTube.")
            pywhatkit.playonyt(cancion)
            
        # 2. Buscar en Google
        elif "busca" in comando:
            busqueda = comando.replace("busca", "").strip()
            hablar(f"Buscando {busqueda} en internet.")
            pywhatkit.search(busqueda)
            
        # 3. Abrir páginas web específicas
        elif "entra a youtube" in comando or "abre youtube" in comando:
            hablar("Abriendo la página principal de YouTube.")
            webbrowser.open("https://www.youtube.com")
            
        # 4. Abrir programas de forma universal (Sin rutas absolutas)
        elif "abre el bloc de notas" in comando:
            hablar("Abriendo el bloc de notas.")
            # notepad.exe es universal en cualquier PC con Windows
            subprocess.Popen("notepad.exe")
            
        elif "abre steam" in comando:
            hablar("Iniciando Steam.")
            # Esto usa el protocolo URL de Steam, funciona en cualquier disco
            webbrowser.open("steam://open/main")
            
        elif "abre spotify" in comando:
            hablar("Abriendo Spotify.")
            # Protocolo universal para abrir la app de Spotify
            webbrowser.open("spotify:")
                
        # --- SI NO ES NINGUNA ORDEN DE SISTEMA, CONVERSAR CON GEMINI ---
        else:
            respuesta_ia = pensar_y_responder(comando)
            hablar(respuesta_ia)
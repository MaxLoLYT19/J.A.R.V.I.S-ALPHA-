import google.generativeai as genai
import os
import subprocess
import sys
import threading
import time
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# --- NUEVAS LIBRERÍAS PARA SELENIUM ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from oido import escuchar
from voz import hablar

# Configuración de Gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("[ERROR] Falta GEMINI_API_KEY en el archivo .env")
    sys.exit()

genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    system_instruction="Eres Jarvis, un asistente virtual avanzado. Sé conciso, directo y conversacional. No uses asteriscos, negritas ni listas largas."
)

def pensar_y_responder(texto_usuario):
    return modelo.generate_content(texto_usuario).text

# --- MOTOR DEL NAVEGADOR DE JARVIS (SELENIUM) ---
navegador_jarvis = None

def obtener_navegador():
    global navegador_jarvis
    # Si el navegador no existe o fue cerrado, creamos uno nuevo
    try:
        if navegador_jarvis is None or not navegador_jarvis.window_handles:
            opciones = Options()
            opciones.add_experimental_option("detach", True)
            
            # --- AQUÍ ESTÁ LA CORRECCIÓN ---
            # Forzamos el uso de Brave indicando su ruta exacta en Windows
            opciones.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            
            # Nueva línea usando el gestor inteligente de Selenium
            navegador_jarvis = webdriver.Chrome(options=opciones)
    except Exception as e:
        print(f"Error con el navegador: {e}")
        
    return navegador_jarvis

# --- INICIO DEL SERVIDOR WEB FLASK ---
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar_comando():
    global navegador_jarvis
    data = request.json
    comando = data.get('comando', '').lower()
    comando_detectado = comando

    if comando == "modo_voz":
        comando_detectado = escuchar()
        comando = comando_detectado
        if not comando:
            return jsonify({"comando_detectado": "", "respuesta": "No logré escuchar nada."})

    def ejecutar_voz_en_segundo_plano(texto):
        threading.Thread(target=hablar, args=(texto,), daemon=True).start()

    respuesta_final = ""

    # 1. APAGADO Y CIERRE DEL SERVIDOR
    if "apágate" in comando or "salir" in comando or "apagar" in comando:
        respuesta_final = "Apagando sistemas. Hasta luego, señor."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        
        if navegador_jarvis:
            try:
                navegador_jarvis.quit() # Cierra el navegador fantasma si estaba abierto
            except:
                pass

        def apagar_servidor():
            os._exit(0)
            
        threading.Timer(3.0, apagar_servidor).start()
        
    # 2. CONTROL AVANZADO DE PESTAÑAS (SELENIUM)
    elif "cierra la pestaña de" in comando:
        objetivo = comando.replace("cierra la pestaña de", "").strip()
        
        if navegador_jarvis:
            try:
                pestanas = navegador_jarvis.window_handles
                cerrada = False
                
                # Revisamos una por una las pestañas abiertas
                for pestana in pestanas:
                    navegador_jarvis.switch_to.window(pestana)
                    # Si el título de la página o la URL coinciden con lo que pediste
                    if objetivo in navegador_jarvis.title.lower() or objetivo in navegador_jarvis.current_url.lower():
                        navegador_jarvis.close() # Cierra solo esa pestaña
                        cerrada = True
                        break
                        
                if cerrada:
                    respuesta_final = f"Pestaña de {objetivo} cerrada."
                    # Regresamos el control a la primera pestaña que haya quedado abierta
                    if navegador_jarvis.window_handles:
                        navegador_jarvis.switch_to.window(navegador_jarvis.window_handles[0])
                    else:
                        navegador_jarvis = None # Si era la última, reiniciamos la variable
                else:
                    respuesta_final = f"No encontré ninguna pestaña abierta relacionada con {objetivo}."
            except Exception as e:
                respuesta_final = "Hubo un error al intentar leer las pestañas actuales."
        else:
            respuesta_final = "Actualmente no estoy controlando ningún navegador."
            
        ejecutar_voz_en_segundo_plano(respuesta_final)

    # 3. NAVEGACIÓN CON SELENIUM
    elif "abre youtube" in comando or "entra a youtube" in comando:
        respuesta_final = "Abriendo YouTube en mis sistemas."
        driver = obtener_navegador()
        
        # Si el navegador acaba de abrirse y solo tiene una pestaña en blanco ("data:,"), 
        # navegamos directamente en esa pestaña inicial.
        if len(driver.window_handles) == 1 and driver.current_url == "data:,":
            driver.get('https://www.youtube.com')
        else:
            # Si ya estabas navegando en otra cosa, abrimos una pestaña nueva
            driver.execute_script("window.open('https://www.youtube.com', '_blank');")
            
        ejecutar_voz_en_segundo_plano(respuesta_final)

    elif "busca" in comando and "en internet" in comando: 
        busqueda = comando.replace("busca", "").replace("en internet", "").strip()
        respuesta_final = f"Buscando {busqueda}."
        driver = obtener_navegador()
        url = f"https://www.google.com/search?q={busqueda}"
        
        if len(driver.window_handles) == 1 and driver.current_url == "data:,":
            driver.get(url)
        else:
            driver.execute_script(f"window.open('{url}', '_blank');")
            
        ejecutar_voz_en_segundo_plano(respuesta_final)

    # 4. ABRIR JUEGOS Y PROGRAMAS (Mantenemos lo que ya funcionaba perfecto)
    elif "abre steam" in comando:
        respuesta_final = "Iniciando Steam."
        try:
            os.startfile("steam://open/main")
        except Exception:
            subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe")            
        ejecutar_voz_en_segundo_plano(respuesta_final)
        
    elif "abre quaver" in comando or "jugar quaver" in comando:
        respuesta_final = "Iniciando Quaver. Que te diviertas."
        try:
            os.startfile("steam://rungameid/980610")
        except Exception:
            respuesta_final = "Hubo un problema de conexión."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        
    elif "abre left 4 dead 2" in comando or "jugar left 4 dead 2" in comando or "abre l4d2" in comando or "jugar l4d2" in comando:
        respuesta_final = "Iniciando Left 4 Dead 2. Preparando armas contra la horda."
        try:
            os.startfile("steam://rungameid/550")
        except Exception:
            respuesta_final = "Hubo un problema al intentar iniciar el juego."
        ejecutar_voz_en_segundo_plano(respuesta_final)
    elif "abre plantas versus zombis" in comando or "jugar plantas versus zombis" in comando or "jugar plantas vs zombis" in comando or "abre plantas vs zombis" in comando or "abre plantas vs zombies" in comando or "jugar pvz" in comando or "abre pvz" in comando:
            respuesta_final = "Iniciando plantas versus zombis. Preparando plantas contra la horda."
            try:
                os.startfile("steam://rungameid/3590")
            except Exception:
                    respuesta_final = "Hubo un problema al intentar iniciar el juego no van a haber platans hoy señor lo siento."
            ejecutar_voz_en_segundo_plano(respuesta_final)
        
    # 5. CERRAR PROGRAMAS EN MASA
    elif "cierra todo" in comando:
        respuesta_final = "Iniciando protocolo de limpieza. Cerrando aplicaciones."
        os.system("taskkill /IM steam.exe /F")
        os.system("taskkill /IM left4dead2.exe /F")
        os.system("taskkill /IM quaver.exe /F")
        os.system("taskkill /IM notepad.exe /F")
        os.system("taskkill /IM brave.exe /F")
        os.system("taskkill /IM pvz /F")
        if navegador_jarvis:
            navegador_jarvis.quit()
            navegador_jarvis = None
            
        ejecutar_voz_en_segundo_plano(respuesta_final)

    else:
        respuesta_final = pensar_y_responder(comando)
        ejecutar_voz_en_segundo_plano(respuesta_final)

    return jsonify({
        "comando_detectado": comando_detectado,
        "respuesta": respuesta_final
    })

if __name__ == '__main__':
    def abrir_interfaz():
        time.sleep(1.5)
        # Aquí usamos el webbrowser estándar de Python para abrir la interfaz de Jarvis
        # en tu Brave normal, así no estorba al Selenium.
        import webbrowser
        webbrowser.open("http://127.0.0.1:5000")
        
    threading.Thread(target=abrir_interfaz).start()
    app.run(port=5000, debug=False)
import os
import subprocess
import threading
import time
import webbrowser  # LIBRERÍA NATIVA ULTRA RÁPIDA
import random      # LIBRERÍA NATIVA PARA RESPUESTAS ALEATORIAS
from flask import Flask, render_template, request, jsonify

from oido import escuchar
from voz import hablar

# --- CEREBRO LOCAL (REEMPLAZO DE GEMINI) ---
def pensar_y_responder(texto_usuario):
    texto_usuario = texto_usuario.lower()
    
    saludos = ["hola", "buenos días", "buenas tardes", "buenas noches", "jarvis"]
    agradecimientos = ["gracias", "te lo agradezco", "perfecto"]
    
    if any(palabra in texto_usuario for palabra in saludos):
        return random.choice([
            "Sistemas en línea. A su entera disposición, señor.",
            "Es un placer saludarle de nuevo, señor. ¿En qué le asisto?",
            "Todos los protocolos operativos. ¿Qué haremos el día de hoy, señor?"
        ])
        
    elif any(palabra in texto_usuario for palabra in agradecimientos):
        return random.choice([
            "El placer es mío, señor.",
            "Para eso fui diseñado.",
            "A la orden, como siempre."
        ])
        
    elif "cómo estás" in texto_usuario or "estado de sistemas" in texto_usuario:
        return "Funcionando a la perfección y con todos los sistemas operativos, señor."
        
    elif "quién eres" in texto_usuario:
        return "Soy Jarvis, su asistente virtual personal, diseñado para ayudarle en sus tareas diarias."
        
    # --- AQUÍ AGREGAMOS LA LÓGICA DE LOS CHISTES ---
    elif "chiste" in texto_usuario or "broma" in texto_usuario:
        chistes = [
            "¿Por qué los desarrolladores odian la luz del sol? Porque tiene muchos bugs.",
            "Hay 10 tipos de personas en el mundo: las que entienden binario y las que no.",
            "¿Qué le dice un bit al otro? Nos vemos en el bus.",
            "Señor, mi módulo de humor está en fase beta, pero aquí va uno: ¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"
        ]
        return random.choice(chistes)

    else:
        return random.choice([
            "Mis disculpas, señor. Esa orden no figura en mi base de datos local.",
            "Me temo que no he comprendido la instrucción, señor. ¿Podría formularla de otra manera?",
            "Protocolo no encontrado. Le sugiero indicarme que abra algún archivo o ejecute un programa."
        ])

# --- INICIO DEL SERVIDOR WEB FLASK ---
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar_comando():
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
        
        def apagar_servidor():
            os._exit(0)
        threading.Timer(3.0, apagar_servidor).start()
        
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    # 2. BÚSQUEDAS ESPECÍFICAS EN GOOGLE
    if "busca" in comando and "en internet" in comando: 
        busqueda = comando.replace("busca", "").replace("en internet", "").strip()
        respuesta_final = f"Buscando {busqueda}."
        webbrowser.open(f"https://www.google.com/search?q={busqueda}")
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    # 3. ABRIR JUEGOS Y PROGRAMAS (Excepciones directas)
    if "abre steam" in comando:
        respuesta_final = "Iniciando Steam."
        try:
            os.startfile("steam://open/main")
        except Exception:
            subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe")            
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})
        
    elif "abre quaver" in comando or "jugar quaver" in comando:
        respuesta_final = "Iniciando Quaver."
        try:
            os.startfile("steam://rungameid/980610")
        except Exception:
            respuesta_final = "Hubo un problema de conexión."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})
        
    elif "abre left 4 dead 2" in comando or "jugar left 4 dead 2" in comando or "abre l4d2" in comando or "jugar l4d2" in comando:
        respuesta_final = "Iniciando Left 4 Dead 2."
        try:
            os.startfile("steam://rungameid/550")
        except Exception:
            respuesta_final = "Hubo un problema al intentar iniciar el juego."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    elif "abre plantas versus zombis" in comando or "jugar plantas versus zombis" in comando or "jugar plantas vs zombis" in comando or "abre plantas vs zombis" in comando or "abre plantas vs zombies" in comando or "jugar pvz" in comando or "abre pvz" in comando:
        respuesta_final = "Iniciando Plantas versus Zombis."
        try:
            os.startfile("steam://rungameid/3590")
        except Exception:
            respuesta_final = "Hubo un problema al intentar iniciar el juego."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    elif "abre hollow knight" in comando or "jugar hollow knight" in comando or "abre hollow" in comando or "jugar hollow" in comando:
        respuesta_final = "Iniciando Hollow Knight."
        try:
            os.startfile("steam://rungameid/367520")
        except Exception:
            respuesta_final = "Hubo un problema de conexión con Steam."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})
        
    elif "abre silksong" in comando or "jugar silksong" in comando:
        respuesta_final = "Iniciando Silksong."
        try:
            os.startfile("steam://rungameid/1030300")
        except Exception:
            respuesta_final = "Hubo un problema de conexión con Steam."
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    elif "abre youtube" in comando or "entra a youtube" in comando:
        respuesta_final = "Abriendo YouTube en mis sistemas."
        webbrowser.open('https://www.youtube.com')
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    elif "abre newgrounds" in comando or "entra a newgrounds" in comando:
        respuesta_final = "Abriendo Newgrounds de inmediato."
        webbrowser.open('https://www.newgrounds.com')
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    # 4. COMANDO INTELIGENTE DE NAVEGACIÓN WEB (CUALQUIER OTRA PÁGINA)
    elif "abre" in comando or "entra a" in comando or "ve a" in comando:
        afirmaciones = ["Enseguida, señor.", "A la orden.", "Como usted disponga, señor.", "Procediendo."]
        
        # Limpiar el comando para quedarse solo con el nombre del sitio
        sitio_solicitado = comando.replace("ve a la página de", "")\
                                  .replace("abre la página de", "")\
                                  .replace("entra a", "")\
                                  .replace("abre", "").strip()
        
        respuesta_final = f"{random.choice(afirmaciones)} Redirigiendo a {sitio_solicitado}."
        
        # EL TRUCO: Usar DuckDuckGo con el modificador '\' para ir al primer resultado directamente
        url_busqueda = f"https://duckduckgo.com/?q=\\{sitio_solicitado}"
        webbrowser.open(url_busqueda)
        
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    # 5. CERRAR PROGRAMAS EN MASA
    elif "cierra todo" in comando:
        respuesta_final = "Iniciando protocolo de limpieza."
        os.system("taskkill /IM steam.exe /F")
        os.system("taskkill /IM left4dead2.exe /F")
        os.system("taskkill /IM quaver.exe /F")
        os.system("taskkill /IM notepad.exe /F")
        os.system("taskkill /IM brave.exe /F")
        os.system("taskkill /IM pvz.exe /F")
        os.system("taskkill /IM silksong.exe /F")
        os.system("taskkill /IM hollow_knight.exe /F")
                
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

    # 6. RESPUESTAS CONVERSACIONALES DEL CEREBRO (Si no fue ninguna orden anterior)
    else:
        respuesta_final = pensar_y_responder(comando)
        ejecutar_voz_en_segundo_plano(respuesta_final)
        return jsonify({"comando_detectado": comando_detectado, "respuesta": respuesta_final})

if __name__ == '__main__':
    def abrir_interfaz():
        time.sleep(1.2)
        webbrowser.open("http://127.0.0.1:5000")
        threading.Thread(target=hablar, args=("Sistemas en línea. Bienvenido de nuevo, señor.",), daemon=True).start()
        
    threading.Thread(target=abrir_interfaz).start()
    app.run(port=5000, debug=False)
import speech_recognition as sr
import tkinter as tk
from tkinter import simpledialog

def entrada_texto_manual():
    """Abre una ventana emergente para escribir el comando."""
    # Creamos la ventana principal pero la ocultamos para que solo se vea el cuadro de diálogo
    root = tk.Tk()
    root.withdraw() 
    
    # Abrimos la ventana de texto
    texto = simpledialog.askstring("Jarvis - Entrada Manual", "No detecté voz. Escribe tu comando aquí:")
    
    # Cerramos el proceso de la ventana al terminar
    root.destroy()
    
    # Si el usuario escribió algo y le dio a Aceptar
    if texto:
        return texto.lower()
    else:
        return "" # Si le dio a Cancelar o cerró la ventana

def escuchar():
    recognizer = sr.Recognizer()
    
    try:
        # Intentamos usar el micrófono
        with sr.Microphone() as source:
            print("Ajustando ruido de fondo...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("\n🎤 Jarvis te está escuchando. ¡Habla ahora!")
            
            try:
                # Esperamos 5 segundos a que hables
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Procesando audio...")
                
                texto = recognizer.recognize_google(audio, language="es-ES")
                print(f"Tú dijiste (por voz): {texto}")
                return texto.lower()
                
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                print("No detecté voz clara. Abriendo ventana de escritura...")
                return entrada_texto_manual()
                
            except sr.RequestError:
                print("Fallo en la conexión con Google. Abriendo ventana de escritura...")
                return entrada_texto_manual()
                
    except OSError:
        # Este error ocurre si literalmente no hay ningún micrófono conectado a la PC
        print("¡No se detectó ningún micrófono físico! Abriendo ventana de escritura...")
        return entrada_texto_manual()

# Bloque de prueba
if __name__ == "__main__":
    comando_final = escuchar()
    print(f"\nEl comando que Jarvis procesará es: {comando_final}")
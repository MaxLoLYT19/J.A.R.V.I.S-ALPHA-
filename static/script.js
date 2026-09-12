// --- LÓGICA DE LA INTERFAZ Y COMUNICACIÓN CON PYTHON ---
const historial = document.getElementById('historial');
const inputTexto = document.getElementById('texto-entrada');
const btnEnviar = document.getElementById('btn-enviar');
const btnMic = document.getElementById('btn-mic');
const MAX_CARACTERES = 200; 

window.onload = () => {
    escribirMensajeAnimado("Sistemas en línea. Conexión local establecida. Esperando directrices...", "jarvis");
    inputTexto.addEventListener('keypress', function(event) {
        if(event.key === 'Enter') enviarTexto();
    });
};

function alternarInterfaz(estado) {
    inputTexto.disabled = !estado;
    btnEnviar.disabled = !estado;
    btnMic.disabled = !estado;
    if(estado) inputTexto.focus();
}

function agregarMensaje(texto, emisor) {
    if (!texto) return;
    const div = document.createElement('div');
    div.className = `mensaje ${emisor}`;
    div.textContent = texto; 
    historial.appendChild(div);
    hacerScrollAbajo();
}

function escribirMensajeAnimado(texto, emisor) {
    if (!texto) return;
    const div = document.createElement('div');
    div.className = `mensaje ${emisor}`;
    historial.appendChild(div);
    
    let i = 0;
    const velocidad = 20; 

    function escribir() {
        if (i < texto.length) {
            div.textContent += texto.charAt(i);
            i++;
            hacerScrollAbajo();
            setTimeout(escribir, velocidad);
        }
    }
    escribir();
}

function hacerScrollAbajo() {
    historial.scrollTop = historial.scrollHeight;
}

async function procesarComando(comandoData) {
    alternarInterfaz(false); 

    try {
        const respuesta = await fetch('/procesar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comando: comandoData })
        });

        if (!respuesta.ok) throw new Error(`Error de red: ${respuesta.status}`);

        const datos = await respuesta.json();
        
        if(comandoData === "modo_voz" && datos.comando_detectado) { 
            agregarMensaje(`[Micrófono]: ${datos.comando_detectado}`, "usuario"); 
        }
        
        escribirMensajeAnimado(datos.respuesta, "jarvis");

    } catch (error) {
        console.error("Error en conexión:", error);
        agregarMensaje("Error crítico: Conexión con el núcleo Python interrumpida.", "error");
    } finally {
        btnMic.classList.remove("escuchando");
        btnMic.textContent = "🎤 Hablar";
        alternarInterfaz(true);
    }
}

function enviarTexto() {
    let texto = inputTexto.value.trim();
    if (texto === "") return;
    if (texto.length > MAX_CARACTERES) {
        texto = texto.substring(0, MAX_CARACTERES);
    }
    agregarMensaje(`[Teclado]: ${texto}`, "usuario");
    inputTexto.value = "";
    procesarComando(texto);
}

function activarMicrofono() {
    btnMic.classList.add("escuchando");
    btnMic.textContent = "Escuchando...";
    agregarMensaje("Calibrando sensores de audio...", "jarvis");
    procesarComando("modo_voz"); 
}

// --- LÓGICA DEL EFECTO VISUAL MATRIX (CÓDIGO CAYENDO) ---
const canvasMatriz = document.getElementById('lienzo-matrix');
const ctxMatriz = canvasMatriz.getContext('2d');

canvasMatriz.width = window.innerWidth;
canvasMatriz.height = window.innerHeight;

const caracteres = '0101010101ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%""\'#&_(),.;:?!\\|{}<>[]^~';
const tamanoFuente = 14;
let columnas = canvasMatriz.width / tamanoFuente;
let gotas = [];

function inicializarGotas() {
    columnas = canvasMatriz.width / tamanoFuente;
    gotas = [];
    for(let x = 0; x < columnas; x++) {
        gotas[x] = 1;
    }
}

inicializarGotas();

function dibujarFondoCodigo() {
    ctxMatriz.fillStyle = 'rgba(5, 8, 16, 0.05)';
    ctxMatriz.fillRect(0, 0, canvasMatriz.width, canvasMatriz.height);

    ctxMatriz.fillStyle = '#00ffcc'; 
    ctxMatriz.font = tamanoFuente + 'px Consolas';

    for(let i = 0; i < gotas.length; i++) {
        const textoElegido = caracteres.charAt(Math.floor(Math.random() * caracteres.length));
        ctxMatriz.fillText(textoElegido, i * tamanoFuente, gotas[i] * tamanoFuente);

        if(gotas[i] * tamanoFuente > canvasMatriz.height && Math.random() > 0.975) {
            gotas[i] = 0;
        }
        gotas[i]++;
    }
}

setInterval(dibujarFondoCodigo, 33);

window.addEventListener('resize', () => {
    canvasMatriz.width = window.innerWidth;
    canvasMatriz.height = window.innerHeight;
    inicializarGotas();
});
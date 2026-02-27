import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ==========================================
# 🎨 ESTILOS ITESARC (Verde, Azul y Amarillo)
# ==========================================
def aplicar_estilos():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        
        /* Títulos en Azul Institucional */
        .titulo-colegio { font-size: 45px; font-weight: 900; text-align: center; color: #004d99; margin-top: 10px;}
        
        /* Subtítulos en Verde Institucional */
        .subtitulo { text-align: center; color: #2e8b57; font-size: 20px; margin-bottom: 30px; font-weight: bold; }
        
        /* Tarjetas con borde Amarillo */
        .tarjeta { background-color: #ffffff; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 6px solid #ffcc00; margin-bottom: 30px;}
        
        .pregunta-titulo { font-size: 26px !important; font-weight: bold !important; text-align: center; color: #004d99; }
        
        /* Botones personalizados */
        div.stButton > button { width: 100%; height: 60px; border-radius: 12px; font-size: 18px; font-weight: bold; transition: 0.3s; }
        
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🧠 CEREBRO (LÓGICA CHASIDE)
# ==========================================
class CerebroProfesional:
    def __init__(self):
        self.GRIMORIO = {
            "C - Administrativas": {"tags": ["Administrativo", "Lógico-matemática"], "desc": "Organización, manejo de datos y liderazgo."},
            "H - Humanísticas": {"tags": ["Social", "Lingüística", "Interpersonal"], "desc": "Comprensión humana, comunicación y ciencias sociales."},
            "A - Artísticas": {"tags": ["Arte", "Espacial", "Musical", "Corporal"], "desc": "Expresión creativa, diseño y estética."},
            "S - Salud": {"tags": ["Salud", "Interpersonal", "Intrapersonal"], "desc": "Cuidado de la vida, empatía y biología."},
            "I - Ingeniería": {"tags": ["Tecnología", "Lógico-matemática", "Espacial"], "desc": "Diseño de sistemas, tecnología y lógica."},
            "D - Defensa": {"tags": ["Defensa", "Corporal", "Interpersonal"], "desc": "Protección, estrategia y orden público."},
            "E - Ciencias Exactas": {"tags": ["Ciencia", "Lógico-matemática", "Intrapersonal"], "desc": "Investigación, método científico y naturaleza."}
        }

    def calcular_perfil(self, puntajes):
        resultados = []
        for area, datos in self.GRIMORIO.items():
            score = sum(puntajes.get(tag, 0) for tag in datos["tags"])
            porcentaje = min((score / 3) * 100, 100)
            if porcentaje > 0:
                resultados.append({"Área": area, "Afinidad (%)": round(porcentaje), "Descripción": datos["desc"]})
        resultados.sort(key=lambda x: x["Afinidad (%)"], reverse=True)
        return resultados

def enviar_correo(email_destino, nombre_estudiante, resultados):
    # --- CONFIGURACIÓN DEL EMISOR ---
    remitente = "testvocacionalitesarc@gmail.com" # Pon aquí la nueva cuenta entre las comillas
    password = "amsgqpggzbawsnuk"          # Pega aquí las 16 letras (sin espacios)

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = email_destino
    msg['Subject'] = f"🎓 Resultados Test Vocacional ITESARC - {nombre_estudiante}"

    # Cuerpo del mensaje con los resultados
    cuerpo = f"Hola {nombre_estudiante},\n\n"
    cuerpo += "¡Felicidades por completar tu proceso de orientación vocacional en el ITESARC!\n\n"
    cuerpo += "Tus resultados de afinidad son:\n"
    
    for res in resultados:
        cuerpo += f"- {res['Área']}: {res['Afinidad (%)']}%\n"
    
    cuerpo += f"\nTu área principal recomendada es: {resultados[0]['Área']}\n"
    cuerpo += "\nEste es un primer paso en tu proyecto de vida. ¡Muchos éxitos!\n"
    cuerpo += "Departamento de Psicoorientación - ITESARC"
    
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        # Conexión al servidor de Google (SMTP)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Seguridad
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        st.success(f"📩 ¡Resultados enviados con éxito a {email_destino}!")
    except Exception as e:
        st.error(f"Ocurrió un error al enviar el correo: {e}")
# ==========================================
# 🌐 INTERFAZ WEB (SISTEMA DE PANTALLAS)
# ==========================================
def main():
    st.set_page_config(page_title="Orientación ITESARC", page_icon="🏫", layout="centered")
    aplicar_estilos()
    
    if 'pantalla' not in st.session_state:
        st.session_state.pantalla = "inicio"
        st.session_state.indice = 0
        st.session_state.puntajes = {k: 0 for k in ["Administrativo", "Social", "Arte", "Salud", "Tecnología", "Defensa", "Ciencia", "Lógico-matemática", "Lingüística", "Interpersonal", "Intrapersonal", "Espacial", "Musical", "Corporal"]}

    # --- PANTALLA 1: BIENVENIDA ---
    if st.session_state.pantalla == "inicio":
        
        # --- LÓGICA DEL LOGO ---
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            # Revisa si pusiste el archivo logo.png o logo.jpg
            if os.path.exists("logo.png"):
                st.image("logo.png", use_container_width=True)
            elif os.path.exists("logo.jpg"):
                st.image("logo.jpg", use_container_width=True)
            else:
                st.markdown("<p style='text-align:center; color:#7f8c8d; font-size:12px;'>(Guarda tu imagen como 'logo.png' en la misma carpeta del código para que aparezca aquí)</p>", unsafe_allow_html=True)
                
        st.markdown("<div class='titulo-colegio'>ITESARC</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitulo'>Departamento de Psicoorientación | Test Vocacional</div>", unsafe_allow_html=True)
        
        st.info("👋 **¡Hola!** Este test te ayudará a descubrir tus talentos ocultos basándose en el modelo CHASIDE y las Inteligencias Múltiples. No hay respuestas correctas ni incorrectas, solo sé honesto contigo mismo.")
        
        st.divider()
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🚀 COMENZAR TEST", type="primary"):
                st.session_state.pantalla = "test"
                st.rerun()

    # --- PANTALLA 2: EL TEST ---
    elif st.session_state.pantalla == "test":
        preguntas = [
            {"cat": "Administrativo", "q": "¿Te imaginas organizando la economía o dirigiendo un equipo de trabajo?"},
            {"cat": "Social", "q": "¿Te ofrecerías para organizar la fiesta de graduación de tu curso?"},
            {"cat": "Lógico-matemática", "q": "¿Te sientes súper cómodo usando matemáticas o programando?"},
            {"cat": "Arte", "q": "¿Disfrutas expresarte a través del dibujo, la pintura o el diseño visual?"},
            # Puedes añadir más preguntas aquí...
        ]

        pregunta_actual = preguntas[st.session_state.indice]
        
        st.progress(st.session_state.indice / len(preguntas), text=f"Pregunta {st.session_state.indice + 1} de {len(preguntas)}")
        
        st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
        st.markdown(f'<div class="pregunta-titulo">{pregunta_actual["q"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 0.1, 1]) 
        with col1:
            if st.button("¡Totalmente! 😎", key=f"y_{st.session_state.indice}"):
                st.session_state.puntajes[pregunta_actual["cat"]] += 1
                avanzar(preguntas)
        with col3:
            if st.button("Nah, paso 🙅‍♂️", key=f"n_{st.session_state.indice}"):
                avanzar(preguntas)

    # --- PANTALLA 3: RESULTADOS Y CORREO ---
    elif st.session_state.pantalla == "resultados":
        st.balloons()
        st.markdown("<h2 style='text-align: center; color: #004d99;'>¡Análisis Completado! 🎉</h2>", unsafe_allow_html=True)
        
        cerebro = CerebroProfesional()
        resultados = cerebro.calcular_perfil(st.session_state.puntajes)
        
        if resultados:
            df = pd.DataFrame(resultados)
            top_1 = resultados[0]
            st.success(f"🌟 **Tu área más fuerte es: {top_1['Área']} ({top_1['Afinidad (%)']}%)**")
            st.bar_chart(df.set_index("Área")["Afinidad (%)"], color="#2e8b57") # Gráfico verde ITESARC
            
            # --- SECCIÓN DE ENVÍO POR CORREO ---
            st.divider()
            st.markdown("### 📥 Recibe tu informe detallado")
            st.write("Ingresa tus datos para enviarte el resultado completo a ti y al departamento de psicoorientación.")
            
            with st.form("formulario_correo"):
                nombre = st.text_input("Tu Nombre Completo:")
                correo = st.text_input("Tu Correo Electrónico:")
                enviar = st.form_submit_button("Enviar Resultados por Correo", type="primary")
                
                if enviar:
                    if nombre and "@" in correo:
                        enviar_correo(correo, nombre, resultados)
                    else:
                        st.error("Por favor ingresa un nombre y un correo válido.")
                        
        st.divider()
        if st.button("🔄 Volver al Inicio"):
            st.session_state.clear()
            st.rerun()

def avanzar(preguntas):
    if st.session_state.indice < len(preguntas) - 1:
        st.session_state.indice += 1
    else:
        st.session_state.pantalla = "resultados"
    st.rerun()

if __name__ == "__main__":
    main()
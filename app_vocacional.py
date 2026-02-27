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
        .titulo-colegio { font-size: 45px; font-weight: 900; text-align: center; color: #004d99; margin-top: 10px;}
        .subtitulo { text-align: center; color: #2e8b57; font-size: 20px; margin-bottom: 30px; font-weight: bold; }
        .tarjeta { background-color: #ffffff; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 6px solid #ffcc00; margin-bottom: 30px;}
        .pregunta-titulo { font-size: 24px !important; font-weight: bold !important; text-align: center; color: #004d99; }
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
        
        # Diccionario dinámico: cuántas preguntas hay de cada categoría
        conteo_preguntas = {
            "Administrativo": 3, "Social": 3, "Arte": 3, "Salud": 3, 
            "Tecnología": 3, "Defensa": 3, "Ciencia": 3,
            "Lógico-matemática": 0, "Lingüística": 0, "Interpersonal": 0, 
            "Intrapersonal": 0, "Espacial": 0, "Musical": 0, "Corporal": 0
        }
        
        for area, datos in self.GRIMORIO.items():
            score = 0
            total_maximo = 0
            for tag in datos["tags"]:
                score += puntajes.get(tag, 0)
                total_maximo += conteo_preguntas.get(tag, 0)
            
            if total_maximo > 0:
                porcentaje = (score / total_maximo) * 100
                if porcentaje > 0:
                    resultados.append({"Área": area, "Afinidad (%)": round(porcentaje), "Descripción": datos["desc"]})
        
        resultados.sort(key=lambda x: x["Afinidad (%)"], reverse=True)
        return resultados

# ==========================================
# 📧 MOTOR DE CORREOS REAL
# ==========================================
def enviar_correo(email_destino, nombre_estudiante, resultados):
    # 👇 ¡PON AQUÍ TU CORREO Y TUS 16 LETRAS! 👇
    remitente = "testvocacionalitesarc@gmail.com" 
    password = "xliklyqdwxzqnqww"          

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = email_destino
    msg['Subject'] = f"🎓 Resultados Test Vocacional ITESARC - {nombre_estudiante}"

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
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        st.success(f"📩 ¡Resultados enviados con éxito a {email_destino}!")
    except Exception as e:
        st.error(f"Ocurrió un error al enviar el correo. Verifica tu contraseña de 16 letras.")

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
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            if os.path.exists("logo.png"):
                st.image("logo.png", use_container_width=True)
            elif os.path.exists("logo.jpg"):
                st.image("logo.jpg", use_container_width=True)
                
        st.markdown("<div class='titulo-colegio'>ITESARC</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitulo'>Departamento de Psicoorientación | Test Vocacional</div>", unsafe_allow_html=True)
        st.info("👋 **¡Hola!** Este test te ayudará a descubrir tus talentos ocultos basándose en el modelo CHASIDE. No hay respuestas correctas ni incorrectas, solo sé honesto contigo mismo.")
        
        st.divider()
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🚀 COMENZAR TEST", type="primary"):
                st.session_state.pantalla = "test"
                st.rerun()

    # --- PANTALLA 2: EL TEST (21 Preguntas) ---
    elif st.session_state.pantalla == "test":
        preguntas = [
            {"cat": "Administrativo", "q": "1. ¿Aceptarías trabajar escribiendo artículos en la sección económica de un diario?"},
            {"cat": "Administrativo", "q": "2. ¿Organizas tu dinero de manera que te alcance hasta el próximo cobro?"},
            {"cat": "Administrativo", "q": "3. ¿Te gustaría ser el responsable de la gestión de una gran empresa?"},
            {"cat": "Social", "q": "4. ¿Te ofrecerías para organizar la despedida de soltero de uno de tus amigos?"},
            {"cat": "Social", "q": "5. ¿Escuchas atentamente los problemas que te plantean tus amigos?"},
            {"cat": "Social", "q": "6. ¿Te gustaría trabajar en una institución de ayuda a menores abandonados?"},
            {"cat": "Arte", "q": "7. ¿Diseñarías el vestuario para una obra de teatro o película?"},
            {"cat": "Arte", "q": "8. ¿Pasarías varias horas al día ensayando con un instrumento musical?"},
            {"cat": "Arte", "q": "9. ¿Te gustaría trabajar en una galería de arte o museo?"},
            {"cat": "Salud", "q": "10. ¿Te dedicarías a socorrer a personas accidentadas o en emergencias?"},
            {"cat": "Salud", "q": "11. ¿Estarías dispuesto a trabajar en un hospital en horarios nocturnos?"},
            {"cat": "Salud", "q": "12. ¿Te interesaría investigar la cura de nuevas enfermedades?"},
            {"cat": "Tecnología", "q": "13. ¿Te interesaba saber de niño cómo estaban construidos tus juguetes?"},
            {"cat": "Tecnología", "q": "14. ¿Te gustaría diseñar programas de computación o videojuegos?"},
            {"cat": "Tecnología", "q": "15. ¿Te atrae el funcionamiento de los motores de los autos?"},
            {"cat": "Defensa", "q": "16. ¿Te gustaría pertenecer a un cuerpo de seguridad como la policía o el ejército?"},
            {"cat": "Defensa", "q": "17. ¿Te sientes capaz de mantener la calma en situaciones de alto riesgo?"},
            {"cat": "Defensa", "q": "18. ¿Te gustaría planear estrategias de rescate en desastres naturales?"},
            {"cat": "Ciencia", "q": "19. ¿Te atraen los misterios de la naturaleza más que la tecnología?"},
            {"cat": "Ciencia", "q": "20. ¿Pasarías tiempo en un laboratorio analizando muestras de suelo o plantas?"},
            {"cat": "Ciencia", "q": "21. ¿Te gustaría descubrir nuevas leyes de la física o la química?"}
        ]

        pregunta_actual = preguntas[st.session_state.indice]
        st.progress((st.session_state.indice + 1) / len(preguntas), text=f"Pregunta {st.session_state.indice + 1} de {len(preguntas)}")
        
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

    # --- PANTALLA 3: RESULTADOS ---
    elif st.session_state.pantalla == "resultados":
        st.balloons()
        st.markdown("<h2 style='text-align: center; color: #004d99;'>¡Análisis Completado! 🎉</h2>", unsafe_allow_html=True)
        
        cerebro = CerebroProfesional()
        resultados = cerebro.calcular_perfil(st.session_state.puntajes)
        
        if resultados:
            df = pd.DataFrame(resultados)
            top_1 = resultados[0]
            st.success(f"🌟 **Tu área más fuerte es: {top_1['Área']} ({top_1['Afinidad (%)']}%)**")
            st.bar_chart(df.set_index("Área")["Afinidad (%)"], color="#2e8b57")
            
            st.divider()
            st.markdown("### 📥 Recibe tu informe detallado")
            st.write("Ingresa tus datos para enviarte el resultado completo a tu correo.")
            
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
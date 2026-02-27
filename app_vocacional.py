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
            "Administrativo": 14, "Social": 14, "Arte": 14, "Salud": 14, 
            "Tecnología": 14, "Defensa": 14, "Ciencia": 14,
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
 # 📚 EL CUESTIONARIO CHASIDE COMPLETO (98 Preguntas Oficiales)
        preguntas = [
            {"cat": "Administrativo", "q": "1. ¿Aceptarías trabajar escribiendo artículos en la sección económica de un diario?"},
            {"cat": "Social", "q": "2. ¿Te ofrecerías para organizar la despedida de soltero de uno de tus amigos?"},
            {"cat": "Tecnología", "q": "3. ¿Te gustaría dirigir un proyecto de urbanización en tu provincia?"},
            {"cat": "Salud", "q": "4. ¿A una frustración siempre opones un pensamiento positivo?"},
            {"cat": "Salud", "q": "5. ¿Te dedicarías a socorrer a personas accidentadas o atacadas por asaltantes?"},
            {"cat": "Social", "q": "6. ¿Cuando eras chico, te interesaba saber cómo estaban construidos tus juguetes?"},
            {"cat": "Ciencia", "q": "7. ¿Te interesan más los misterios de la naturaleza que los secretos de la tecnología?"},
            {"cat": "Social", "q": "8. ¿Escuchas atentamente los problemas que te plantean tus amigos?"},
            {"cat": "Social", "q": "9. ¿Te ofrecerías para explicar a tus compañeros un determinado tema que ellos no entendieron?"},
            {"cat": "Administrativo", "q": "10. ¿Eres exigente y crítico con tu equipo de trabajo?"},
            {"cat": "Arte", "q": "11. ¿Te atrae armar rompecabezas o descubrir mensajes ocultos?"},
            {"cat": "Ciencia", "q": "12. ¿Puedes establecer la diferencia conceptual entre macroeconomía y microeconomía?"},
            {"cat": "Salud", "q": "13. ¿Usarías uniforme en tu trabajo?"},
            {"cat": "Defensa", "q": "14. ¿Participarías como profesional en un espectáculo de acrobacia aérea?"},
            {"cat": "Administrativo", "q": "15. ¿Organizas tu dinero de manera que te alcance hasta el próximo cobro?"},
            {"cat": "Social", "q": "16. ¿Convences fácilmente a otras personas sobre la validez de tus argumentos?"},
            {"cat": "Ciencia", "q": "17. ¿Estás informado sobre los nuevos descubrimientos referidos al Big Bang?"},
            {"cat": "Salud", "q": "18. ¿Ante una emergencia epidémica participarías en una campaña brindando tu ayuda?"},
            {"cat": "Arte", "q": "19. ¿Te quedarías horas leyendo un libro de tu interés?"},
            {"cat": "Tecnología", "q": "20. ¿Participarías en una investigación sobre agujeros negros?"},
            {"cat": "Administrativo", "q": "21. ¿Dejas para mañana lo que puedes hacer hoy?"},
            {"cat": "Administrativo", "q": "22. ¿Creés que un buen negocio es aquel en el que todas las partes se benefician?"},
            {"cat": "Arte", "q": "23. ¿Te gusta escribir poemas o cuentos?"},
            {"cat": "Ciencia", "q": "24. ¿Te interesaría aprender sobre la estructura del ADN y la genética?"},
            {"cat": "Social", "q": "25. ¿Defenderías públicamente una causa justa aunque eso te traiga problemas?"},
            {"cat": "Defensa", "q": "26. ¿Te atrae la idea de pilotar un avión o dirigir un barco?"},
            {"cat": "Tecnología", "q": "27. ¿Te resulta fácil comprender el funcionamiento de aparatos electrónicos?"},
            {"cat": "Salud", "q": "28. ¿Te gustaría estudiar la anatomía y el funcionamiento del cuerpo humano?"},
            {"cat": "Administrativo", "q": "29. ¿Te gustaría planificar y administrar el presupuesto de una gran empresa?"},
            {"cat": "Defensa", "q": "30. ¿Estarías dispuesto a seguir una disciplina estricta en un ambiente militar?"},
            {"cat": "Social", "q": "31. ¿Sueles ser el mediador cuando hay conflictos entre tus amigos?"},
            {"cat": "Tecnología", "q": "32. ¿Te gustaría diseñar el plano de una casa o edificio?"},
            {"cat": "Arte", "q": "33. ¿Disfrutas visitando museos, galerías de arte o exposiciones?"},
            {"cat": "Ciencia", "q": "34. ¿Te atrae la idea de investigar la vida de microorganismos en un laboratorio?"},
            {"cat": "Defensa", "q": "35. ¿Te gustaría pertenecer a un grupo de fuerzas especiales o de rescate?"},
            {"cat": "Salud", "q": "36. ¿Sientes empatía inmediata cuando ves a alguien sufriendo dolor físico?"},
            {"cat": "Administrativo", "q": "37. ¿Te sientes cómodo liderando un grupo y asignando tareas?"},
            {"cat": "Ciencia", "q": "38. ¿Te gustaría trabajar en la preservación de especies en peligro de extinción?"},
            {"cat": "Arte", "q": "39. ¿Tienes facilidad para dibujar, pintar o esculpir?"},
            {"cat": "Tecnología", "q": "40. ¿Te gustaría programar tu propio software, aplicación o videojuego?"},
            {"cat": "Social", "q": "41. ¿Te interesaría estudiar el comportamiento humano y la psicología?"},
            {"cat": "Defensa", "q": "42. ¿Te atrae la idea de investigar la escena de un crimen?"},
            {"cat": "Salud", "q": "43. ¿Estarías dispuesto a trabajar en un hospital con turnos rotativos nocturnos?"},
            {"cat": "Administrativo", "q": "44. ¿Sueles leer las noticias de economía y finanzas?"},
            {"cat": "Tecnología", "q": "45. ¿Te gusta reparar objetos que se han dañado en tu casa?"},
            {"cat": "Arte", "q": "46. ¿Te gustaría tocar un instrumento musical en una orquesta o banda?"},
            {"cat": "Ciencia", "q": "47. ¿Te interesa el estudio de las reacciones químicas y los elementos?"},
            {"cat": "Social", "q": "48. ¿Te gustaría enseñar a niños pequeños en una escuela?"},
            {"cat": "Defensa", "q": "49. ¿Mantienes la calma y piensas rápido en situaciones de emergencia?"},
            {"cat": "Salud", "q": "50. ¿Te gustaría trabajar en el desarrollo de nuevas vacunas o medicinas?"},
            {"cat": "Administrativo", "q": "51. ¿Te resulta fácil organizar eventos con muchas personas y logística?"},
            {"cat": "Arte", "q": "52. ¿Te atrae el diseño gráfico, la fotografía o la edición de videos?"},
            {"cat": "Tecnología", "q": "53. ¿Te gustaría diseñar y construir puentes, carreteras o represas?"},
            {"cat": "Ciencia", "q": "54. ¿Te apasiona la astronomía y el estudio de los planetas?"},
            {"cat": "Social", "q": "55. ¿Te gustaría trabajar en una ONG ayudando a comunidades vulnerables?"},
            {"cat": "Defensa", "q": "56. ¿Te atraen los deportes de riesgo o las artes marciales?"},
            {"cat": "Salud", "q": "57. ¿Te gustaría investigar terapias para mejorar la salud mental?"},
            {"cat": "Administrativo", "q": "58. ¿Te ves trabajando en un banco o en la bolsa de valores?"},
            {"cat": "Tecnología", "q": "59. ¿Disfrutas armando circuitos electrónicos o trabajando con robótica?"},
            {"cat": "Arte", "q": "60. ¿Te gustaría ser actor, actriz o trabajar en el mundo del cine?"},
            {"cat": "Ciencia", "q": "61. ¿Te interesa entender cómo los cambios climáticos afectan al ecosistema?"},
            {"cat": "Social", "q": "62. ¿Te resulta fácil aprender diferentes idiomas y conocer otras culturas?"},
            {"cat": "Defensa", "q": "63. ¿Te gustaría ser abogado penalista o trabajar en el sistema judicial?"},
            {"cat": "Salud", "q": "64. ¿Te atrae la idea de trabajar como odontólogo o fisioterapeuta?"},
            {"cat": "Administrativo", "q": "65. ¿Eres bueno calculando probabilidades y estadísticas en tu cabeza?"},
            {"cat": "Ciencia", "q": "66. ¿Te gustaría analizar muestras de tierra para mejorar la agricultura?"},
            {"cat": "Arte", "q": "67. ¿Tienes buen gusto para la decoración de interiores o la moda?"},
            {"cat": "Tecnología", "q": "68. ¿Te gustaría trabajar mejorando la inteligencia artificial de las computadoras?"},
            {"cat": "Social", "q": "69. ¿Te interesa la historia de la humanidad y las ciencias políticas?"},
            {"cat": "Defensa", "q": "70. ¿Te sientes cómodo utilizando armas de fuego en un entorno de entrenamiento legal?"},
            {"cat": "Salud", "q": "71. ¿Podrías asistir en una cirugía médica sin impresionarte por la sangre?"},
            {"cat": "Administrativo", "q": "72. ¿Te gustaría tener tu propio emprendimiento comercial?"},
            {"cat": "Tecnología", "q": "73. ¿Te atrae el diseño de sistemas de energía renovable (paneles solares, eólica)?"},
            {"cat": "Arte", "q": "74. ¿Disfrutas analizando la estructura de una obra literaria clásica?"},
            {"cat": "Ciencia", "q": "75. ¿Te gustaría realizar investigaciones en la Antártida o en el fondo del mar?"},
            {"cat": "Social", "q": "76. ¿Sientes vocación por ayudar a la rehabilitación de personas con adicciones?"},
            {"cat": "Defensa", "q": "77. ¿Te atrae la estrategia política y la diplomacia internacional?"},
            {"cat": "Salud", "q": "78. ¿Te gustaría estudiar nutrición para ayudar a mejorar la dieta de las personas?"},
            {"cat": "Administrativo", "q": "79. ¿Te gusta llevar un registro detallado de tus gastos personales mensuales?"},
            {"cat": "Arte", "q": "80. ¿Sueles fijarte en la arquitectura de los edificios cuando caminas por la ciudad?"},
            {"cat": "Tecnología", "q": "81. ¿Te interesa el mantenimiento y diseño de redes informáticas y ciberseguridad?"},
            {"cat": "Ciencia", "q": "82. ¿Te gustaría estudiar el comportamiento de los animales en su hábitat natural?"},
            {"cat": "Social", "q": "83. ¿Participas activamente en debates sobre problemas sociales actuales?"},
            {"cat": "Defensa", "q": "84. ¿Te atrae trabajar en la aduana o en el control de fronteras?"},
            {"cat": "Salud", "q": "85. ¿Te gustaría trabajar con personas de la tercera edad para mejorar su calidad de vida?"},
            {"cat": "Administrativo", "q": "86. ¿Te sientes capaz de evaluar el rendimiento laboral de otras personas?"},
            {"cat": "Arte", "q": "87. ¿Te gustaría trabajar en la producción de un programa de radio o televisión?"},
            {"cat": "Tecnología", "q": "88. ¿Te atrae la mecánica automotriz o la aviación comercial?"},
            {"cat": "Ciencia", "q": "89. ¿Te gustaría trabajar en un laboratorio farmacéutico analizando compuestos químicos?"},
            {"cat": "Social", "q": "90. ¿Te interesa el periodismo de investigación social o reportajes comunitarios?"},
            {"cat": "Defensa", "q": "91. ¿Te gustaría ser perito forense y analizar evidencias físicas?"},
            {"cat": "Salud", "q": "92. ¿Estarías dispuesto a trabajar en zonas de desastre o guerra como médico sin fronteras?"},
            {"cat": "Administrativo", "q": "93. ¿Te gustaría dirigir el departamento de recursos humanos de una multinacional?"},
            {"cat": "Arte", "q": "94. ¿Te gustaría dedicarte a la coreografía o la danza profesional?"},
            {"cat": "Tecnología", "q": "95. ¿Te interesaría la ingeniería de sonido o trabajar en un estudio de grabación?"},
            {"cat": "Ciencia", "q": "96. ¿Te atraen temas de genética molecular o clonación?"},
            {"cat": "Social", "q": "97. ¿Te gustaría trabajar en el departamento de relaciones públicas de una organización?"},
            {"cat": "Defensa", "q": "98. ¿Te visualizas asumiendo la responsabilidad de la seguridad nacional o ciudadana?"}
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
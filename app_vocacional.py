import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
# ==========================================
# 🎨 ESTILOS ITESARC (Verde, Azul y Amarillo)
# ==========================================
def aplicar_estilos():
    st.markdown("""
        <style>
        /* Ocultar elementos por defecto de Streamlit */
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        
        /* Textos principales */
        .titulo-colegio { font-size: 45px; font-weight: 900; text-align: center; color: #004d99; margin-top: 10px;}
        .subtitulo { text-align: center; color: #2e8b57; font-size: 20px; margin-bottom: 30px; font-weight: bold; }
        
        /* 🪄 AQUÍ ESTÁ LA MAGIA: Tarjeta transparente y sin bordes molestos */
        .tarjeta { 
            background-color: transparent; /* Fondo transparente */
            padding: 20px 0px; 
            margin-bottom: 30px;
            border-bottom: 3px solid #ffcc00; /* Solo una línea amarilla sutil abajo */
        }
        
        /* Texto de la pregunta más grande e imponente */
        .pregunta-titulo { 
            font-size: 28px !important; 
            font-weight: 900 !important; 
            text-align: center; 
            color: #004d99; 
        }
        
        /* Botones redondeados y modernos */
        div.stButton > button { 
            width: 100%; 
            height: 60px; 
            border-radius: 15px; 
            font-size: 18px; 
            font-weight: bold; 
            transition: 0.3s; 
            border: 2px solid #004d99;
        }
        div.stButton > button:hover {
            border-color: #2e8b57;
            color: #2e8b57;
        }
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
# 📧 MOTOR DE CORREOS REAL (CON CARRERAS)
# ==========================================
def enviar_correo(email_destino, nombre_estudiante, resultados):
    # 👇 ¡RECUERDA PONER TU CORREO Y TUS 16 LETRAS AQUÍ! 👇
    remitente = "testvocacionalitesarc@gmail.com" 
    password = "xliklyqdwxzqnqww"          

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = email_destino
    msg['Subject'] = f"🎓 Resultados Test Vocacional ITESARC - {nombre_estudiante}"

    # 🎯 NUEVO: Catálogo de Carreras CHASIDE
    carreras_recomendadas = {
        "C - Administrativas": "Administración de Empresas, Economía, Contaduría Pública, Negocios Internacionales, Marketing, Recursos Humanos.",
        "H - Humanísticas": "Psicología, Derecho, Comunicación Social, Trabajo Social, Sociología, Filosofía, Licenciaturas/Docencia.",
        "A - Artísticas": "Diseño Gráfico, Arquitectura, Artes Plásticas, Diseño de Modas, Producción Audiovisual, Música, Animación 3D.",
        "S - Salud": "Medicina, Enfermería, Odontología, Fisioterapia, Nutrición, Veterinaria, Bacteriología.",
        "I - Ingeniería": "Ingeniería de Sistemas, Ingeniería Civil, Ingeniería Industrial, Mecatrónica, Desarrollo de Software, Arquitectura.",
        "D - Defensa": "Ciencias Militares, Ciencias Policiales, Criminalística, Criminología, Derecho Penal, Gestión del Riesgo.",
        "E - Ciencias Exactas": "Biología, Química, Matemáticas, Ingeniería Ambiental, Biotecnología, Física, Ingeniería Agronómica."
    }

    # Identificamos el área ganadora (la número 1)
    area_ganadora = resultados[0]['Área']
    
    # Buscamos las carreras para esa área (si no la encuentra por algún error, pone un texto genérico)
    carreras = carreras_recomendadas.get(area_ganadora, "Múltiples carreras universitarias y técnicas afines.")

    # 📝 Construcción del mensaje
    cuerpo = f"Hola {nombre_estudiante},\n\n"
    cuerpo += "¡Felicidades por completar tu proceso de orientación vocacional en el ITESARC!\n\n"
    cuerpo += "📊 Tus resultados de afinidad son:\n"
    
    for res in resultados:
        cuerpo += f"- {res['Área']}: {res['Afinidad (%)']}%\n"
    
    cuerpo += f"\n🏆 Tu área principal recomendada es: {area_ganadora}\n"
    cuerpo += f"\n🎓 POSIBLES CARRERAS Y PROFESIONES PARA TI:\n"
    cuerpo += f"> {carreras}\n"
    cuerpo += "\nRecuerda que este es un primer paso en tu proyecto de vida. ¡Muchos éxitos en tu futuro profesional!\n"
    cuerpo += "Departamento de Psicoorientación - ITESARC"
    
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False
# ==========================================
# 📊 MOTOR DE BASE DE DATOS (ESCRITURA)
# ==========================================
def guardar_en_excel(nombre, correo, area_fuerte, porcentaje, resultados):
    try:
        alcances = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        if "GOOGLE_CREDENTIALS" in st.secrets and len(st.secrets["GOOGLE_CREDENTIALS"]) > 10:
            creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"].strip())
            credenciales = Credentials.from_service_account_info(creds_dict, scopes=alcances)
        else:
            credenciales = Credentials.from_service_account_file('credenciales.json', scopes=alcances)
        
        cliente = gspread.authorize(credenciales)
        hoja = cliente.open("Base de Datos - Test ITESARC").sheet1
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
# 1. Primero, sacamos todos los porcentajes de la variable 'resultados'
        porcentajes = {r['Área']: r['Afinidad (%)'] for r in resultados}
        
        # 2. Llenamos las "cajitas" (letras) con el número exacto de cada área. 
        # Si por algún error un área no tiene puntaje, le ponemos un 0 para que el Excel no se descuadre.
        c = porcentajes.get("C - Administrativas", 0)
        h = porcentajes.get("H - Humanísticas", 0)
        a = porcentajes.get("A - Artísticas", 0)
        s = porcentajes.get("S - Salud", 0)
        i = porcentajes.get("I - Ingeniería", 0)
        d = porcentajes.get("D - Defensa", 0)
        e = porcentajes.get("E - Ciencias Exactas", 0)
        
        # 3. AHORA SÍ, el robot manda la fila completa.
        # Como las letras ya tienen los números guardados, el robot pegará: Nombre, Correo, Area, 85, Fecha, 70, 40, 90...
        hoja.append_row([nombre, correo, area_fuerte, porcentaje, fecha_actual, c, h, a, s, i, d, e], table_range="A1")
        return True
        
    except Exception as e:
        st.error(f"⚠️ Error interno con la base de datos: {e}")
        return False

# ==========================================
# 📈 MOTOR DE LECTURA (PARA EL DASHBOARD)
# ==========================================
def leer_excel():
    try:
        alcances = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        
        # 🔑 Sistema de llaves inteligente (Nube o Local)
        if "GOOGLE_CREDENTIALS" in st.secrets and len(st.secrets["GOOGLE_CREDENTIALS"]) > 10:
            creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"].strip())
            credenciales = Credentials.from_service_account_info(creds_dict, scopes=alcances)
        else:
            credenciales = Credentials.from_service_account_file('credenciales.json', scopes=alcances)
            
        cliente = gspread.authorize(credenciales)
        hoja = cliente.open("Base de Datos - Test ITESARC").sheet1
        
        datos = hoja.get_all_values()
        if len(datos) > 1:
            # Convertimos a tabla de datos (DataFrame)
            df = pd.DataFrame(datos[1:], columns=datos[0])
            return df
        return pd.DataFrame()
            
    except Exception as e:
        st.error(f"⚠️ Error al leer la base de datos: {e}")
        return pd.DataFrame()
# ==========================================
# 🌐 INTERFAZ WEB (SISTEMA DE PANTALLAS)
# ==========================================
def main():
    st.set_page_config(page_title="Orientación ITESARC", page_icon="🏫", layout="centered")
    aplicar_estilos()
    
    # --- 1. MEMORIA DE LA APP ---
    if 'pantalla' not in st.session_state:
        st.session_state.pantalla = "inicio"
    if 'indice' not in st.session_state:
        st.session_state.indice = 0
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    if 'puntajes' not in st.session_state:
        st.session_state.puntajes = {k: 0 for k in ["Administrativo", "Social", "Arte", "Salud", "Tecnología", "Defensa", "Ciencia", "Lógico-matemática", "Lingüística", "Interpersonal", "Intrapersonal", "Espacial", "Musical", "Corporal"]}

    # --- 2. BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.markdown("### 🔐 Acceso Docentes")
        if not st.session_state.autenticado:
            pwd = st.text_input("Contraseña:", type="password", key="login_admin_secret")
            if pwd == "ITESARC2026":
                st.session_state.autenticado = True
                st.rerun()
        else:
            st.write("✅ Sesión Iniciada")
            if st.button("📊 Abrir Panel de Control", key="btn_ir_dashboard"):
                st.session_state.pantalla = "dashboard"
                st.rerun()
            if st.button("🔴 Cerrar Sesión", key="btn_logout_docente"):
                st.session_state.autenticado = False
                st.session_state.pantalla = "inicio"
                st.rerun()

    # --- 3. NAVEGACIÓN DE PANTALLAS (ORDENADA) ---
    
    # --- PANTALLA 1: INICIO ---
    if st.session_state.pantalla == "inicio":
        st.markdown("<div class='titulo-colegio'>ITESARC</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitulo'>Departamento de Psicoorientación | Test Vocacional</div>", unsafe_allow_html=True)
        st.info("👋 **¡Hola!** Este test te ayudará a descubrir tus talentos ocultos basándose en el modelo CHASIDE.")
        
        # EL BOTÓN AHORA ESTÁ DENTRO DEL IF (CORREGIDO)
        if st.button("🚀 COMENZAR TEST", type="primary", key="btn_inicio_principal"):
            st.session_state.pantalla = "test"
            st.session_state.indice = 0
            st.rerun()

    # --- PANTALLA 2: EL TEST (98 Preguntas) ---
    elif st.session_state.pantalla == "test":
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
            {"cat": "Administrativo", "q": "86. ¿Te siente capaz de evaluar el rendimiento laboral de otras personas?"},
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
            st.markdown("### 📥 Registro de Resultados")
            
            tipo_usuario = st.radio(
                "¿Eres estudiante activo del ITESARC?", 
                ("Selecciona una opción...", "Sí, soy estudiante", "No, solo soy un visitante"),
                key="tipo_usuario_radio"
            )
            
            if tipo_usuario == "Sí, soy estudiante":
                st.info("Tus resultados se guardarán en la base de datos de la psicoorientadora.")
                with st.form("formulario_estudiante"):
                    nombre = st.text_input("Tu Nombre Completo:")
                    correo = st.text_input("Tu Correo Electrónico:")
                    enviar = st.form_submit_button("Guardar y Enviar a mi Correo", type="primary")
                    
                    if enviar:
                        if nombre and "@" in correo:
                            with st.spinner("Procesando datos institucionales..."):
                                correo_ok = enviar_correo(correo, nombre, resultados)
                                excel_ok = guardar_en_excel(nombre, correo, top_1['Área'], top_1['Afinidad (%)'], resultados)
                                if correo_ok and excel_ok:
                                    st.success("✅ ¡Todo listo! Datos guardados y enviados.")
                        else:
                            st.error("Por favor ingresa un nombre y un correo válido.")
                            
            elif tipo_usuario == "No, solo soy un visitante":
                with st.form("formulario_visitante"):
                    nombre_vis = st.text_input("Tu Nombre:")
                    correo_vis = st.text_input("Tu Correo:")
                    enviar_vis = st.form_submit_button("Solo enviarme mis resultados", type="primary")
                    if enviar_vis:
                        if nombre_vis and "@" in correo_vis:
                            enviar_correo(correo_vis, nombre_vis, resultados)
                            st.success("📩 ¡Enviado!")

        st.divider()
        if st.button("🔄 Volver al Inicio", key="btn_reset"):
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
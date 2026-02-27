import streamlit as st
import pandas as pd

# ==========================================
# 🎨 ESTILOS CSS PERSONALIZADOS (MAGIA VISUAL)
# ==========================================
def aplicar_estilos():
    st.markdown("""
        <style>
        /* Ocultar el menú superior y el pie de página de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Estilo para la pregunta principal (Letra grande y centrada) */
        .pregunta-titulo {
            font-size: 30px !important;
            font-weight: 800 !important;
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
            line-height: 1.4;
        }

        /* Contenedor tipo tarjeta para la pregunta */
        .tarjeta {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            border-top: 5px solid #6c5ce7;
        }
        
        /* Ajustar los botones nativos de Streamlit */
        div.stButton > button {
            width: 100%;
            height: 70px;
            border-radius: 15px;
            font-size: 20px;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🧠 CEREBRO: LÓGICA CHASIDE & GARDNER
# ==========================================
class CerebroProfesional:
    def __init__(self):
        # Taxonomía basada en tu guía oficial
        self.GRIMORIO = {
            "C - Administrativas y Contables": {
                "tags": ["Administrativo", "Lógico-matemática"],
                "desc": "Organización, manejo de datos y liderazgo empresarial."
            },
            "H - Humanísticas y Sociales": {
                "tags": ["Social", "Lingüística", "Interpersonal"],
                "desc": "Comprensión humana, comunicación y ciencias sociales."
            },
            "A - Artísticas": {
                "tags": ["Arte", "Espacial", "Musical", "Corporal"],
                "desc": "Expresión creativa, diseño y sensibilidad estética."
            },
            "S - Ciencias de la Salud": {
                "tags": ["Salud", "Interpersonal", "Intrapersonal"],
                "desc": "Cuidado de la vida, empatía y ciencias biológicas."
            },
            "I - Ingeniería y Computación": {
                "tags": ["Tecnología", "Lógico-matemática", "Espacial"],
                "desc": "Diseño de sistemas, tecnología y resolución lógica."
            },
            "D - Defensa y Seguridad": {
                "tags": ["Defensa", "Corporal", "Interpersonal"],
                "desc": "Protección, estrategia y orden público."
            },
            "E - Ciencias Exactas y Agrarias": {
                "tags": ["Ciencia", "Lógico-matemática", "Intrapersonal"],
                "desc": "Investigación pura, método científico y naturaleza."
            }
        }

    def calcular_perfil(self, puntajes):
        resultados = []
        for area, datos in self.GRIMORIO.items():
            # Sumamos los puntos de las etiquetas correspondientes al área
            score = sum(puntajes.get(tag, 0) for tag in datos["tags"])
            
            # Calculamos el porcentaje (Ajustar el '4' según cantidad de preguntas por área)
            porcentaje = min((score / 3) * 100, 100) # Tope en 100%
            
            if porcentaje > 0:
                resultados.append({
                    "Área": area,
                    "Afinidad (%)": round(porcentaje),
                    "Descripción": datos["desc"]
                })
        
        # Ordenar de mayor a menor afinidad
        resultados.sort(key=lambda x: x["Afinidad (%)"], reverse=True)
        return resultados

# ==========================================
# 🌐 INTERFAZ WEB ATRACTIVA
# ==========================================
def main():
    st.set_page_config(page_title="Descubre tu Vocación", page_icon="🎓", layout="centered")
    aplicar_estilos() 
    
    # Inicializar la memoria de la sesión
    if 'indice' not in st.session_state:
        st.session_state.indice = 0
        st.session_state.puntajes = {k: 0 for k in [
            "Administrativo", "Social", "Arte", "Salud", "Tecnología", 
            "Defensa", "Ciencia", "Lógico-matemática", "Lingüística", 
            "Interpersonal", "Intrapersonal", "Espacial", "Musical", "Corporal"
        ]}
        st.session_state.finalizado = False

    # 🌟 BATERÍA AMPLIADA DE PREGUNTAS (Extraídas del Manual Oficial)
    preguntas = [
        # --- PREGUNTAS CHASIDE (Aptitudes e Intereses) ---
        {"cat": "Administrativo", "q": "¿Te imaginas organizando la economía o dirigiendo un equipo de trabajo?"},
        {"cat": "Social", "q": "¿Te ofrecerías para organizar la fiesta de graduación de tu curso o una despedida?"},
        {"cat": "Salud", "q": "¿Te dedicarías a socorrer a personas heridas o en situaciones de emergencia?"},
        {"cat": "Tecnología", "q": "¿De pequeño desarmabas tus juguetes para ver cómo estaban construidos?"},
        {"cat": "Ciencia", "q": "¿Te interesan más los misterios de la naturaleza que la última tecnología?"},
        {"cat": "Arte", "q": "¿Diseñarías la campaña publicitaria de un nuevo producto?"},
        {"cat": "Arte", "q": "¿Te gustaría hacer el proyecto arquitectónico de un complejo de edificios?"},
        {"cat": "Ciencia", "q": "¿Te gustaría dirigir un proyecto de excavación arqueológica?"},
        {"cat": "Defensa", "q": "¿Te atraen las actividades donde se requiere valentía, estrategia y protección a otros?"},
        
        # --- PREGUNTAS GARDNER (Inteligencias Múltiples) ---
        {"cat": "Lingüística", "q": "¿Te resulta fácil decir lo que piensas durante una discusión o debate argumentativo?"},
        {"cat": "Lógico-matemática", "q": "¿Te sientes súper cómodo usando calculadoras, matemáticas o programando computadoras?"},
        {"cat": "Lógico-matemática", "q": "¿Puedes sumar o multiplicar mentalmente con mucha rapidez?"},
        {"cat": "Corporal", "q": "¿Aprendes rápidamente los pasos de un baile nuevo o un deporte físico?"},
        {"cat": "Espacial", "q": "¿Prefieres hacer un mapa que explicarle a alguien con palabras cómo tiene que llegar a un lugar?"},
        {"cat": "Espacial", "q": "¿Siempre distingues el Norte del Sur, estés donde estés?"},
        {"cat": "Musical", "q": "¿Sabes tocar (o antes sabías tocar) algún instrumento musical?"},
        {"cat": "Musical", "q": "¿Sueles asociar la música directamente con tus estados de ánimo?"},
        {"cat": "Intrapersonal", "q": "¿Si estás enojado o contento, generalmente sabes exactamente por qué es?"},
        {"cat": "Interpersonal", "q": "¿Eres esa persona a la que todos sus amigos buscan para contarle sus problemas?"},
        {"cat": "Interpersonal", "q": "¿Te das cuenta bastante bien de lo que las otras personas piensan de ti?"}
    ]

    # --- PANTALLA DE PREGUNTAS ---
    if not st.session_state.finalizado:
        pregunta_actual = preguntas[st.session_state.indice]
        
        st.markdown("<h3 style='text-align: center; color: #6c5ce7;'>🚀 Explorador de Talentos</h3>", unsafe_allow_html=True)
        
        # Barra de progreso
        progreso = st.session_state.indice / len(preguntas)
        st.progress(progreso)
        st.markdown(f"<p style='text-align: center; color: #888;'>Pregunta {st.session_state.indice + 1} de {len(preguntas)}</p>", unsafe_allow_html=True)
        
        # Tarjeta de la pregunta
        st.markdown('<div class="tarjeta">', unsafe_allow_html=True)
        st.markdown(f'<div class="pregunta-titulo">{pregunta_actual["q"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botones de Acción
        col1, col2, col3 = st.columns([1, 0.1, 1]) 
        
        with col1:
            if st.button("¡Totalmente! 😎", key=f"yes_{st.session_state.indice}"):
                st.session_state.puntajes[pregunta_actual["cat"]] += 1
                avanzar(preguntas)
                
        with col3:
            if st.button("Nah, paso 🙅‍♂️", key=f"no_{st.session_state.indice}"):
                avanzar(preguntas)

    # --- PANTALLA DE RESULTADOS ---
    else:
        st.balloons() # Animación de celebración
        st.markdown("<h1 style='text-align: center; color: #27ae60;'>¡Análisis Completado! 🎉</h1>", unsafe_allow_html=True)
        st.write("Hemos procesado tus respuestas basándonos en tu perfil CHASIDE y tus Inteligencias Múltiples.")
        
        cerebro = CerebroProfesional()
        resultados = cerebro.calcular_perfil(st.session_state.puntajes)
        
        if resultados:
            df = pd.DataFrame(resultados)
            
            # Mostrar el resultado principal
            top_1 = resultados[0]
            st.success(f"🌟 **Tu área más fuerte es:\n {top_1['Área']} ({top_1['Afinidad (%)']}%)**\n\n{top_1['Descripción']}")
            
            # Gráfico de barras
            st.write("### Tu mapa de talentos")
            st.bar_chart(df.set_index("Área")["Afinidad (%)"], color="#6c5ce7")
            
            # Mostrar tabla detallada
            with st.expander("Ver detalles de todas las áreas"):
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Necesitamos más datos para definir tu perfil. Tus intereses están muy equilibrados.")
            
        st.divider()
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🔄 Hacer el test de nuevo", use_container_width=True):
                st.session_state.clear()
                st.rerun()

def avanzar(preguntas):
    if st.session_state.indice < len(preguntas) - 1:
        st.session_state.indice += 1
    else:
        st.session_state.finalizado = True
    st.rerun()

if __name__ == "__main__":
    main()
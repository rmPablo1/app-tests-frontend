import streamlit as st
import random
from st_supabase_connection import SupabaseConnection

# -----------------------------
# Supabase connection
# -----------------------------
conn = st.connection("supabase", type=SupabaseConnection)

# -----------------------------
# Topics dictionary
# -----------------------------
TOPICS_DICTIONARY = {
 "TEMA 1": "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno. Título I. Transparencia de la actividad pública: capítulo III",
 "TEMA 2": "Ley 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía delos derechos digitales: Título I: disposiciones generales. Título II: principios de protecciónde datos. Título III: derechos de las personas. Título V: responsable y encargado del tratamiento: capítulo III",
 "TEMA 3": "Constitución Española: Título I. De los derechos y deberes fundamentales. Título III de las cortes generales: Capítulo Segundo. De la elaboración de las leyes.",
 # "TEMA 4": "Real Decreto de 24 de julio de 1889 por el que se publica el Código Civil: Título Preliminar. De las normas jurídicas, su aplicación y eficacia: Capítulos I, II y III.",
 # "TEMA 5": "Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público: Título Preliminar: Disposiciones generales, principios de actuación y funcionamiento del sector público: Capítulos I y II, III, IV, V y VI.",
 # "TEMA 6": "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas. Título I: De los interesados en el procedimiento. Título II: De la actividad de las Administraciones Públicas. Título III: de los actos administrativos. Título IV: de las disposiciones sobre el procedimiento administrativo común. Título V: de la revisión de los actos en vía administrativa. Título VI: de la iniciativa legislativa y de la potestad para dictar reglamentos y otras disposiciones.",
 # "TEMA 7": "Ley Orgánica 3/2007, de 22 de marzo, para la igualdad efectiva de mujeres y hombres. Título preliminar. Título I: el principio de igualdad y la tutela contra la discriminación. Título IV: el derecho al trabajo en igualdad de oportunidades: capítulo I y II. Título V: el principio de igualdad en el empleo público: capítulo I. Ley 15/2022, de 12 de julio, Integral para la Igualdad de trato y la no discriminación. Título Preliminar. Título I: disposiciones generales: Capítulo I.",
 # "TEMA 8": "Real Decreto Legislativo 5/2015, de 30 de octubre, por el que se aprueba el texto refundido del Estatuto Básico del Empleado Público. Títulos I a VIII: objeto y ámbito de aplicación; personal al servicio de las AAPP; derechos y deberes y código de conducta; adquisición y pérdida de la relación de servicio; ordenación de la actividad profesional; situaciones administrativas; régimen disciplinario; cooperación entre Administraciones Públicas.",
 # "TEMA 9": "Real Decreto Legislativo 2/2015, de 23 de octubre, Estatuto de los Trabajadores. Título I: relación individual de trabajo (capítulo I, capítulo II sección 1ª y capítulo III secciones 3ª y 4ª). Título II: derechos de representación colectiva y de reunión (capítulo I sección 1ª).",
 # "TEMA 10": "Ley 5/2023, de 7 de junio, de la Función Pública de Andalucía. Título I: disposiciones generales (capítulos I y III).",
 # "TEMA 11": "Reglamento 2/2025 por el que se regula la Evaluación del Desempeño y la Carrera Profesional Horizontal del PTGAS de la Universidad de Córdoba.",
 # "TEMA 12": "Decreto 212/2017, de 26 de diciembre, Estatutos de la Universidad de Córdoba. Títulos I a VIII: naturaleza y fines; comunidad universitaria; funciones; estructura; gobierno y administración; servicios a la comunidad universitaria; régimen patrimonial, económico y financiero; reforma de los estatutos.",
 # "TEMA 13": "Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales. Capítulos I, III y IV: objeto y ámbito de aplicación; derechos y obligaciones; servicios de prevención.",
 # "TEMA 14": "Ley Orgánica 2/2023, del Sistema Universitario. Títulos I a V y IX: funciones y autonomía universitaria; creación y calidad del sistema; organización de enseñanzas; investigación y transferencia del conocimiento; cooperación y coordinación; régimen específico de universidades públicas.",
 # "TEMA 15": "Ley 1/2026, Universitaria para Andalucía. Título II: comunidad universitaria (capítulos III y IV). Título VI: régimen económico, financiero y patrimonial (capítulo II: financiación de las universidades públicas).",
 # "TEMA 16": "Ley 14/2011, de la Ciencia, la Tecnología y la Innovación. Título Preliminar y Título II: recursos humanos dedicados a la investigación (capítulos I y III).",
 # "TEMA 17": "Reglamento 25/2022 de ingreso, provisión de puestos de trabajo y promoción profesional del Personal de Administración y Servicios de la Universidad de Córdoba (excepto preámbulo y anexos).",
 # "TEMA 18": "Reglamento 17/2023 sobre jornada de trabajo, horario, vacaciones, permisos y licencias del PAS de la Universidad de Córdoba.",
 # "TEMA 19": "Normativa del Personal Docente e Investigador de la Universidad de Córdoba: concursos de acceso a cuerpos docentes universitarios, promoción interna y provisión de plazas; ingreso de profesorado contratado doctor y contratado no estable.",
 # "TEMA 20": "Plan Propio de Investigación 'Enrique Aguilar Benítez de Lugo' de la Universidad de Córdoba.",
 # "TEMA 21": "Ley 38/2003, de 17 de noviembre, General de Subvenciones. Título Preliminar: disposiciones generales.",
 # "TEMA 22": "Reglamento 33/2022 de la Universidad de Córdoba sobre gestión de subvenciones (artículos 1 a 5 y 8 a 10).",
 # "TEMA 23": "Real Decreto 822/2021, de 28 de septiembre, por el que se establece la organización de las enseñanzas universitarias y el aseguramiento de su calidad.",
 # "TEMA 24": "Real Decreto 99/2011, de 28 de enero, por el que se regulan las enseñanzas oficiales de doctorado.",
 # "TEMA 25": "Real Decreto 1002/2010 sobre expedición de títulos universitarios oficiales y Real Decreto 534/2024 sobre acceso a estudios de grado y admisión universitaria.",
 # "TEMA 26": "Reglamento 24/2019 de Régimen Académico de los Estudios de Grado de la Universidad de Córdoba.",
 # "TEMA 27": "Reglamento 35/2019 de los Estudios de Máster Universitario de la Universidad de Córdoba.",
 # "TEMA 28": "Reglamento 30/2024 de los Estudios de Doctorado de la Universidad de Córdoba.",
 # "TEMA 29": "Presupuesto de la Universidad de Córdoba (texto articulado): capítulos I a IV.",
 # "TEMA 30": "Presupuesto de la Universidad de Córdoba (texto articulado): capítulos V a X.",
 # "TEMA 31": "Presupuesto de la Universidad de Córdoba (anexos): indemnizaciones por razón de servicio y fórmula de reparto presupuestario (asignación a centros).",
 # "TEMA 32": "Ley 9/2017, de 8 de noviembre, de Contratos del Sector Público. Título Preliminar: capítulo II, sección 1ª."
}

# -----------------------------
# Fetch questions
# -----------------------------
@st.cache_data(ttl=600)
def get_questions():
 return conn.table("questions").select("*").execute().data

def shuffle_questions():
 data = get_questions()
 random.shuffle(data)
 return data

# -----------------------------
# Session state init
# -----------------------------
if "questions" not in st.session_state:
 st.session_state.questions = shuffle_questions()

if "submitted" not in st.session_state:
 st.session_state.submitted = False

if "selected_topic" not in st.session_state:
 st.session_state.selected_topic = None

# -----------------------------
# Reset quiz
# -----------------------------
def reset_quiz():
 st.session_state.questions = shuffle_questions()
 st.session_state.submitted = False
 st.session_state.selected_topic = None

 for i in range(1, 500):
  st.session_state.pop(f"answer_{i}", None)

# -----------------------------
# Show all questions
# -----------------------------
def show_all_questions():
 st.session_state.selected_topic = None
 st.session_state.submitted = False

# -----------------------------
# UI HEADER
# -----------------------------
st.title("Tests para la oposición al grupo C1 de la Escala Administrativa de la Universidad de Córdoba")

col1, col2, col3 = st.columns(3)

with col1:
 st.button(
  "Corregir Test",
  on_click=lambda: st.session_state.update({"submitted": True})
 )

with col2:
 st.button("Reiniciar Test 🔄", on_click=reset_quiz)

with col3:
 st.button("📖 Todos los temas", on_click=show_all_questions)

# -----------------------------
# TOPIC FILTERS
# -----------------------------
st.subheader("📚 Temas")

cols = st.columns(4)

for idx, (tema, desc) in enumerate(TOPICS_DICTIONARY.items()):
 col = cols[idx % 4]

 if col.button(tema, key=f"btn_{tema}"):
  st.session_state.selected_topic = desc
  st.session_state.submitted = False

if st.session_state.selected_topic:
 st.info("🔎 Filtrando por tema seleccionado")

 if st.button("❌ Quitar filtro"):
  st.session_state.selected_topic = None
  st.session_state.submitted = False

else:
 st.info("📖 Mostrando todas las preguntas")

# -----------------------------
# FILTER QUESTIONS
# -----------------------------
all_questions = st.session_state.questions

if st.session_state.selected_topic:
 data = [
  q for q in all_questions
  if q["topic"] == st.session_state.selected_topic
 ]
else:
 data = all_questions

# -----------------------------
# CARD RENDER
# -----------------------------
def render_question_card(q, i):
 submitted = st.session_state.submitted
 user_answer = st.session_state.get(f"answer_{i}")
 correct = q["correct_answer"]

 is_correct = None
 if submitted and user_answer is not None:
  is_correct = (user_answer == correct)

 if not submitted:
  border_color = "#e6e6e6"
 elif is_correct:
  border_color = "#2ecc71"
 else:
  border_color = "#e74c3c"

 st.markdown(
  f"""
        <div style="
            border:2px solid {border_color};
            border-radius:12px;
            padding:16px;
            margin-bottom:12px;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
        ">
            <div style="font-size:13px;color:gray;">
                Tema: {q['topic']}
            </div>
            <h4>Pregunta {i}</h4>
            <div style="font-size:16px;">
                {q['question']}
            </div>
        </div>
        """,
  unsafe_allow_html=True
 )

 options = q["options"]

 st.radio(
  "Elige una respuesta:",
  list(options.keys()),
  format_func=lambda x: f"{x}: {options[x]}",
  key=f"q_{i}"
 )

 st.session_state[f"answer_{i}"] = st.session_state.get(f"q_{i}")

 if submitted:
  if is_correct:
   st.success("Correcta ✅")
  else:
   st.error(f"Incorrecto ❌ (La respuesta correcta es: {correct})")

  with st.expander("Explicación"):
   st.write(q["explanation"])

# -----------------------------
# RENDER QUESTIONS
# -----------------------------
for i, q in enumerate(data, start=1):
 render_question_card(q, i)

# -----------------------------
# SCORE
# -----------------------------
if st.session_state.submitted:
 score = sum(
  st.session_state.get(f"answer_{i}") == q["correct_answer"]
  for i, q in enumerate(data, start=1)
 )

 st.success(f"🎯 Final Score: {score} / {len(data)}")
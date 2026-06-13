import math
import random

from src.topics_dictionary import TOPICS_DICTIONARY
import streamlit as st
from st_supabase_connection import SupabaseConnection

# --------------------------------------------------
# Conexión a Supabase
# --------------------------------------------------
conn = st.connection("supabase", type=SupabaseConnection)


@st.cache_data(ttl=600)
def get_questions():
 return conn.table("questions").select("*").execute().data


def shuffle_questions():
 data = get_questions()
 random.shuffle(data)
 return data


# --------------------------------------------------
# Inicialización del Estado de la Sesión
# --------------------------------------------------
if "questions" not in st.session_state:
 st.session_state.questions = shuffle_questions()

if "submitted" not in st.session_state:
 st.session_state.submitted = False

if "selected_topic" not in st.session_state:
 st.session_state.selected_topic = None

if "page" not in st.session_state:
 st.session_state.page = 1


QUESTIONS_PER_PAGE = 10


# --------------------------------------------------
# Funciones Auxiliares
# --------------------------------------------------
def clear_answers():
 keys_to_remove = [
  key
  for key in st.session_state.keys()
  if key.startswith("q_") or key.startswith("answer_")
 ]
 for key in keys_to_remove:
  del st.session_state[key]


def reset_quiz():
 st.session_state.questions = shuffle_questions()
 st.session_state.submitted = False
 st.session_state.selected_topic = None
 st.session_state.page = 1
 clear_answers()


def show_all_questions():
 st.session_state.selected_topic = None
 st.session_state.submitted = False
 st.session_state.page = 1


# --------------------------------------------------
# Cabecera de la Aplicación
# --------------------------------------------------
st.title("📘 Aplicación de Cuestionarios")

col1, col2 = st.columns(2)

with col1:
 st.button(
  "Reiniciar examen 🔄",
  on_click=reset_quiz,
  use_container_width=True,
 )

with col2:
 st.button(
  "📖 Ver todas las preguntas",
  on_click=show_all_questions,
  use_container_width=True,
 )


# --------------------------------------------------
# Interfaz de Filtrado por Temas (Menú Desplegable)
# --------------------------------------------------
st.subheader("📚 Temas")

topic_options = ["--- Seleccionar un Tema ---"] + list(TOPICS_DICTIONARY.keys())

current_index = 0
if st.session_state.selected_topic:
 for tema, desc in TOPICS_DICTIONARY.items():
  if desc == st.session_state.selected_topic:
   current_index = topic_options.index(tema)
   break

selected_tema_name = st.selectbox(
 "Filtrar por tema:",
 options=topic_options,
 index=current_index,
 label_visibility="collapsed"
)

if selected_tema_name != "--- Seleccionar un Tema ---":
 new_desc = TOPICS_DICTIONARY[selected_tema_name]
 if st.session_state.selected_topic != new_desc:
  st.session_state.selected_topic = new_desc
  st.session_state.submitted = False
  st.session_state.page = 1
  st.rerun()
else:
 if st.session_state.selected_topic is not None:
  st.session_state.selected_topic = None
  st.session_state.submitted = False
  st.session_state.page = 1
  st.rerun()

if st.session_state.selected_topic:
 st.info("🔎 Filtrando por tema activo")
else:
 st.info("📖 Mostrando todas las preguntas")


# --------------------------------------------------
# Lógica de Filtrado de Datos
# --------------------------------------------------
all_questions = st.session_state.questions

if st.session_state.selected_topic:
 data = [
  q
  for q in all_questions
  if q["topic"] == st.session_state.selected_topic
 ]
else:
 data = all_questions


# --------------------------------------------------
# Cálculos de Paginación
# --------------------------------------------------
total_questions = len(data)
total_pages = max(1, math.ceil(total_questions / QUESTIONS_PER_PAGE))

st.session_state.page = min(st.session_state.page, total_pages)

start_idx = (st.session_state.page - 1) * QUESTIONS_PER_PAGE
end_idx = start_idx + QUESTIONS_PER_PAGE
page_data = data[start_idx:end_idx]


# --------------------------------------------------
# Componente Reutilizable de Controles de Paginación
# --------------------------------------------------
def render_pagination_controls(key_suffix):
 st.markdown("---")
 prev_col, info_col, next_col = st.columns([1, 2, 1])

 with prev_col:
  if st.button("⬅️ Anterior", key=f"prev_{key_suffix}", disabled=st.session_state.page == 1):
   st.session_state.page -= 1
   st.rerun()

 with info_col:
  st.markdown(
   f"""
            <div style="text-align:center; padding-top: 6px;">
                Página {st.session_state.page} de {total_pages} ({total_questions} preguntas)
            </div>
            """,
   unsafe_allow_html=True,
  )

 with next_col:
  if st.button("Siguiente ➡️", key=f"next_{key_suffix}", disabled=st.session_state.page == total_pages):
   st.session_state.page += 1
   st.rerun()


# --- PAGINACIÓN SUPERIOR ---
render_pagination_controls(key_suffix="top")
st.markdown("---")


# --------------------------------------------------
# Componente de Tarjeta de Pregunta
# --------------------------------------------------
def render_question_card(q, i):
 submitted = st.session_state.submitted

 user_answer = st.session_state.get(f"q_{i}")
 correct = q["correct_answer"]

 is_correct = (user_answer == correct) if (submitted and user_answer is not None) else None

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
            <div style="font-size:13px; color:gray;">
                Tema: {q['topic']}
            </div>
            <h4 style="margin-top: 6px; margin-bottom: 6px;">Pregunta {i}</h4>
            <div style="font-size:16px; font-weight: 500; margin-bottom: 4px;">
                {q['question']}
            </div>
        </div>
        """,
  unsafe_allow_html=True,
 )

 options = q["options"]

 st.radio(
  "Selecciona una respuesta:",
  list(options.keys()),
  format_func=lambda x: f"{x}: {options[x]}",
  key=f"q_{i}",
  label_visibility="collapsed"
 )

 st.session_state[f"answer_{i}"] = st.session_state.get(f"q_{i}")

 if submitted:
  if is_correct:
   st.success("Correcto ✅")
  else:
   st.error(f"Incorrecto ❌ (Correcta: {correct})")

  with st.expander("Explicación"):
   st.write(q["explanation"])


# --------------------------------------------------
# Renderizar Elementos de la Página Actual
# --------------------------------------------------
for i, q in enumerate(page_data, start=start_idx + 1):
 render_question_card(q, i)


# --- PAGINACIÓN INFERIOR ---
render_pagination_controls(key_suffix="bottom")


# --------------------------------------------------
# Controles Finales y Puntuación
# --------------------------------------------------
st.markdown("---")

# Botón de envío al final de la página
if not st.session_state.submitted:
 st.button(
  "Corregir Tests 🚀",
  on_click=lambda: st.session_state.update({"submitted": True}),
  use_container_width=True
 )

if st.session_state.submitted:
 score = sum(
  st.session_state.get(f"answer_{i}") == q["correct_answer"]
  for i, q in enumerate(data, start=1)
 )

 percentage = (score / len(data) * 100) if len(data) > 0 else 0

 st.success(
  f"🎯 Puntuación: {score}/{len(data)} ({percentage:.1f}%)"
 )
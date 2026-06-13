import streamlit as st
from st_supabase_connection import SupabaseConnection

conn = st.connection("supabase",type=SupabaseConnection)

rows = conn.query("*", table="questions", ttl="10m").execute()

for row in rows.data:
    st.write(f"{row['name']} has a :{row['pet']}:")

st.write("Tests para la oposición al grupo C1 de la escala administrativa de la Universidad de Córdoba")




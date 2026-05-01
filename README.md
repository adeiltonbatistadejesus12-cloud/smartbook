import streamlit as st

st.set_page_config(page_title="SmartBook", layout="wide")

st.title("SmartBook")
st.subheader("Estude com método, revise com inteligência")

st.write("Seu painel de estudos começou a funcionar.")

materia = st.text_input("Matéria")
assunto = st.text_input("Assunto")

col1, col2, col3 = st.columns(3)

with col1:
    questoes = st.number_input("Questões feitas", min_value=0)

with col2:
    acertos = st.number_input("Acertos", min_value=0)

with col3:
    erros = st.number_input("Erros", min_value=0)

if st.button("Salvar desempenho"):
    st.success("Desempenho salvo com sucesso!")

    st.write("Matéria:", materia)
    st.write("Assunto:", assunto)
    st.write("Questões:", questoes)
    st.write("Acertos:", acertos)
    st.write("Erros:", erros)

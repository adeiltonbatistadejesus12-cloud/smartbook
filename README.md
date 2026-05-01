import streamlit as st

st.set_page_config(page_title="SmartBook", layout="wide")

st.title("SmartBook")
st.subheader("Estude com método, revise com inteligência")

st.divider()

st.header("Painel de Estudos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Progresso", "0%")

with col2:
    st.metric("Tempo estudado", "00:00")

with col3:
    st.metric("Questões feitas", "0")

with col4:
    st.metric("Erros para corrigir", "0")

st.divider()

st.header("Meu Edital")

materia = st.text_input("Matéria")
assunto = st.text_input("Assunto")

if st.button("Adicionar ao edital"):
    st.success(f"Adicionado: {materia} - {assunto}")

st.divider()

st.header("Questões Feitas")

questoes = st.number_input("Quantidade de questões", min_value=0)
acertos = st.number_input("Quantidade de acertos", min_value=0)
erros = st.number_input("Quantidade de erros", min_value=0)

if st.button("Salvar desempenho"):
    st.success("Desempenho salvo com sucesso.")

    if questoes > 0:
        percentual = (acertos / questoes) * 100
        st.write(f"Aproveitamento: {percentual:.1f}%")

st.divider()

st.header("Caderno de Erros")

questao = st.text_area("Questão que errou")
motivo = st.text_area("Por que errou?")
explicacao = st.text_area("Explicação correta")

if st.button("Salvar erro"):
    st.success("Erro salvo no caderno de erros.")

import streamlit as st

st.title("👩‍🔬 Endpoints do administrativo para pesquisadores")

st.header("`/ResearcherRest/Query`")
with st.expander("Consultar dados básicos de um pesquisador"):
    st.title("")

st.header("`/ResearcherRest/Query/Count`")
with st.expander("Consultar número total de pesquisadores"):
    st.title("")

st.header("`/ResearcherRest/Delete`")
with st.expander("Deletar dados de um pesquisador"):
    st.title("")

st.header("`/ResearcherRest/Insert`")
with st.expander("Inserir novo pesquisador"):
    st.title("")

st.header("`/ResearcherRest/InsertGrant`")
with st.expander("Inserir subsídio para um pesquisador"):
    st.title("")

import streamlit as st

st.title(
    "👨‍🔬 Endpoints do administrativo para pesquisadores de programas de pós-graduação"
)

st.header("`/GraduateProgramResearcherRest/Query`")
with st.expander("Consultar pesquisadores de programas de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramResearcherRest/Query/Count`")
with st.expander(
    "Consultar número total de pesquisadores de programas de pós-graduação"
):
    st.title("")

st.header("`/GraduateProgramResearcherRest/Delete`")
with st.expander("Deletar pesquisador de programa de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramResearcherRest/Insert`")
with st.expander("Inserir novo pesquisador em programa de pós-graduação"):
    st.title("")

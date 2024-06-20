import streamlit as st

st.title("🎓 Endpoints do administrativo para programas de pós-graduação")

st.header("`/GraduateProgramRest/Query`")
with st.expander("Consultar programas de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramRest/Query/Count`")
with st.expander("Consultar número total de programas de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramRest/Delete`")
with st.expander("Deletar programa de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramRest/Fix`")
with st.expander("Corrigir programa de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramRest/Insert`")
with st.expander("Inserir novo programa de pós-graduação"):
    st.title("")

st.header("`/GraduateProgramRest/Update`")
with st.expander("Atualizar programa de pós-graduação"):
    st.title("")

import streamlit as st

st.title("👩‍🏫 endpoints do administrativo para o SIMCC")

st.header("`/InstitutionRest/Insert`")
with st.expander("adicionar uma nova institutição"):
    st.title("")

st.header("`/InstitutionRest/Query`")
with st.expander("consultar dados basicos de uma instituição"):
    st.title("")
st.header("`/InstitutionRest/Query/Count`")
with st.expander("consultar dados completos de uma instituição"):
    st.title("")

import streamlit as st
from funzioni import *

stagione_in_corso='2022-23'

st.set_page_config(page_title="Mantra Cevapci")

st.title("Mantra Cevapci")
st.subheader("Lega fantacalcio bosniaca affiliata alla federazione _ULMI_")

st.header("Alcuni numeri:")

col1, col2, col3 = st.columns(3)
col1.metric("Anno fondazione",2019)
col2.metric("Squadre partecipanti",10)
col3.metric("Quota partecipazione","40 €")

col4, col5, col6 = st.columns(3)
col4.metric("Competizioni nazionali",3)
col5.metric("Monte stipendi attuale",'€{:,.2f}'.format(sum(voti_arricchiti().loc[(voti_arricchiti()['Stagione']==stagione_in_corso) & (voti_arricchiti()['Squadra']!='nan'),'Stipendio'])))
col6.metric("Giornate giocate",int(campionato.shape[0]/5))
import streamlit as st
st.set_page_config(page_title="Mantra Cevapci")
from PIL import Image
import requests
from io import BytesIO
from funzioni import *

stagione_in_corso='2022-23'

st.title("Mantra Cevapci")
st.image(Image.open(BytesIO(requests.get(load_images_cup()[0]).content)))

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

st.info("Numero di squadre che si qualificheranno alla prossima stagione ULMI: 4")
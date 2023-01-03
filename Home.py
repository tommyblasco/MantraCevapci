import streamlit as st
st.set_page_config(page_title="Mantra Cevapci")
from funzioni import *

st.title("Mantra Cevapci")

st.subheader("Lega fantacalcio bosniaca affiliata alla federazione _ULMI_")

colcup1, colcup2, colcup3 = st.columns(3)
with colcup1:
    st.image(Image.open(BytesIO(requests.get(load_images_cup()[0]).content)),caption='MantraCevapci',use_column_width=True)
with colcup2:
    st.image(Image.open(BytesIO(requests.get(load_images_cup()[1]).content)),caption='Coppa Luk',use_column_width=True)
with colcup3:
    st.image(Image.open(BytesIO(requests.get(load_images_cup()[2]).content)),caption='SuperCup Ivanica',use_column_width=True)

st.header("Alcuni numeri:")
col1, col2, col3 = st.columns(3)
col1.metric("📅 Anno fondazione",2019)
col2.metric("👕 Squadre partecipanti",10)
col3.metric("💸 Quota partecipazione","40 €")

col4, col5, col6 = st.columns(3)
col4.metric("🏆 Competizioni nazionali",3)
try:
    col5.metric("💰 Monte stipendi attuale",'€{:,.2f}'.format(sum(voti_arricchiti().loc[(voti_arricchiti()['Stagione']==stagione_in_corso) & (voti_arricchiti()['Squadra']!='nan'),'Stipendio'])))
except:
    col5.metric("💰 Monte stipendi attuale",'€ 0')
col6.metric("⚽ Giornate giocate",int(campionato.shape[0]/5))

st.info("🏅 Numero di squadre che si qualificheranno alla prossima stagione ULMI: 4")
st.info("📝 Leggi il [regolamento](https://docs.google.com/document/d/1Di1ChzoPGegAzvwQeXAXGv_CyMjieh9879f2cwKhA0g/edit)")

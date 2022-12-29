import streamlit as st
from funzioni import *

@st.cache
def load_data(df):
    l_data=pd.read_csv("https://raw.githubusercontent.com/tommyblasco/MantraCevapci/main/Dati/"+df+".csv",sep=";")
    return l_data

ruolo=load_data("Ruolo")
campionato=load_data("Campionato")
giocatori=load_data("Giocatori")
deco_prizes=load_data("Deco_prizes")
premi_extra=load_data("Premi_extra")
mercato=load_data("Mercato")
quotazioni=load_data("Quotazioni_new")
voti=load_data("Voti_new")
moduli=load_data("Moduli")

voti['Data']=voti['Data'].apply(pd.to_datetime)
mercato['deco_op']=['PRE' if x.startswith('PRE') else x for x in mercato['Tipo_operazione']]
ruoli_dif=['Por','DD; DS; E','DC','DD; DC','DS; DC','DD; DC; E','DS; DC; E','DD; DS; E','DS; E','DD; E','DD; E; M','DS; E; M','DD; DS; DC']
ruoli_cen=['E','E; M','E; W','E; C','M; C','M','C; T','C','C; W','C; W; T','W','W; T','T']
ruoli_att=['W; A','W; T; A','T; A','A','PC']

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
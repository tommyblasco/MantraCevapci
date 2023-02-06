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
    v_filt=voti_arricchiti()[(voti_arricchiti()['Stagione'] == stagione_in_corso) & (voti_arricchiti()['Squadra'] != 'nan')]
    mx_gio=max(v_filt['Giornata'])
    v_filt_last=v_filt[v_filt['Giornata']==mx_gio]
    col5.metric("💰 Monte stipendi attuale",'€{:,.2f}'.format(sum(v_filt['Stipendio'])),
                delta=round(sum(v_filt_last['Stipendio']),2))
except:
    col5.metric("💰 Monte stipendi attuale",'€ 0')
col6.metric("⚽ Giornate giocate",int(campionato.shape[0]/5))

st.info("🏅 Numero di squadre che si qualificheranno alla prossima stagione ULMI: 4")
st.info("📝 Leggi il [regolamento](https://docs.google.com/document/d/1Di1ChzoPGegAzvwQeXAXGv_CyMjieh9879f2cwKhA0g/edit)")
st.info("💳 [Salda il conto](https://www.paypal.com/paypalme/mantracevapci?country.x=IT&locale.x=it_IT)")

# with st.sidebar:
#     st.write('Ultima giornata:')
#     max_gio=int(max(campionato.loc[campionato['Stagione']==stagione_in_corso,'Giornata']))
#     st.text('Stagione '+stagione_in_corso+', Giornata '+str(max_gio))
#     last_day=campionato[(campionato['Stagione']==stagione_in_corso) & (campionato['Giornata']==max_gio)]
#     cols1, cols2, cols3, cols4 = st.columns(4)
#     with cols1:
#         for ht in last_day['Home']:
#             img=Image.open(BytesIO(requests.get(load_images(ht)[0]).content))
#             img_rsz=img.resize((60,60))
#             st.image(img_rsz)
#     with cols2:
#         for gfh in last_day['GH']:
#             st.markdown('<h1 style="font-size:30px;">{}</h1>'.format(str(gfh)), unsafe_allow_html=True)
#     with cols3:
#         for gfa in last_day['GA']:
#             st.markdown('<h1 style="font-size:30px;">{}</h1>'.format(str(gfa)), unsafe_allow_html=True)
#     with cols4:
#         for ha in last_day['Away']:
#             img = Image.open(BytesIO(requests.get(load_images(ha)[0]).content))
#             img_rsz=img.resize((60,60))
#             st.image(img_rsz)
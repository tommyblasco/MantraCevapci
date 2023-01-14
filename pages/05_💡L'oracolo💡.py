import streamlit
from funzioni import *

st.title("Formazione consigliata per la prossima giornata:")
st.subheader("Il primo algoritmo, testato dal maestro, che vi farà vincere al 100%")

list_team=tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan'])))
sel_team=st.selectbox('Scegli una squadra',list_team)

max_gio=int(max(voti_arricchiti().loc[voti_arricchiti()['Stagione']==stagione_in_corso,'Giornata']))
rosa=rosa_oggi(team=sel_team)
q=quotazioni[quotazioni['Stagione'] == max(quotazioni['Stagione'])].rename({'Nome':'ID'},axis=1)
info_rosa1=pd.merge(rosa[['Nome','Ruolo']], giocatori[['Nome','ID']], on='Nome',how='left')
info_rosa2=pd.merge(info_rosa1, q[['ID', 'QA']], on='ID', how='left').rename({'ID':'Giocatori'},axis=1)

gioc_filt=pd.merge(prob_form(),info_rosa2,on='Giocatori',how='inner')

df=stats_web(gioc_filt)
df['Prob']=[1 if x>=70 else 0.5 if (x<70) & (x>35) else 0 for x in df['Prob']]
df['Pre'] = [(x - min(df['Pre'])) / (max(df['Pre']) - min(df['Pre'])) for x in df['Pre']]
df['MFV'] = [(x - min(df['MFV'])) / (max(df['MFV']) - min(df['MFV'])) for x in df['MFV']]
df['Quo'] = [(x - min(df['QA'])) / (max(df['QA']) - min(df['QA'])) for x in df['QA']]
df['MFVPre'] = [x * y for x, y in zip(df['Pre'], df['MFV'])]
if max_gio > 4:
    df['Index'] = [(x + y + z + w) / 4 for x, y, z, w in zip(df['Prob'], df['Difficulty'], df['MFV'], df['Quo'])]
else:
    df['Index'] = [(x + y + z) / 3 for x, y, z in zip(df['Prob'], df['Difficulty'], df['Quo'])]
df = df[['Giocatori', 'Ruolo', 'Index']]

p_11=pred_b11(df,seas=stagione_in_corso)
p11pos = pd.merge(p_11, grafica, on=['Modulo', 'Pos'], how='left')
p11_chart = go.Figure()
p11_chart.add_trace(go.Scatter(y=p11pos['y'], x=p11pos['x'], mode='markers+text', marker_color='blue',
                               text=['<b>' + str(x) + '<b>'for x in p11pos['Giocatori']], textposition='bottom center',textfont_color='black'))
p11_chart.update_traces(mode='markers+text', marker_line_width=2, marker_size=10)
p11_chart.add_layout_image(dict(source=Image.open(BytesIO(requests.get(load_images_cup()[4]).content)),
                                layer="below", sizing='stretch', opacity=0.7, x=0, y=1, xanchor='left', yanchor='top',
                                sizex=1, sizey=1))
p11_chart.update_xaxes(showgrid=False, zeroline=False, visible=False)
p11_chart.update_yaxes(showgrid=False, zeroline=False, visible=False)
col20, col21 = st.columns(2)
with col20:
    st.write("Miglior 11 che puoi schierare")
    st.plotly_chart(p11_chart, use_container_width=True)
with col21:
    st.metric("Modulo", max(p_11['Modulo']))
    st.write("Lista giocatori")
    p_11['P']=[x.split('p')[0]+'0'+x.split('p')[1] if len(x)==2 else x for x in p_11['Pos']]
    p_11=p_11.sort_values('P')
    st.dataframe(p_11[['Giocatori']])
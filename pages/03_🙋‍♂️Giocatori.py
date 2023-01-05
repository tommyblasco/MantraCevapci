from funzioni import *

st.title("Giocatori")
sel_player=st.selectbox('Scegli un giocatore:',tuple(sorted(giocatori['ID'])))

tab10, tab11 = st.tabs(["Forma","Carriera"])
with tab10:
    col18, col19 = st.columns(2)
    with col18:
        st.write('Andamento FantaVoto')
        v=voti_arricchiti()[(voti_arricchiti()['Nome'] == sel_player) & (voti_arricchiti()['Stagione'] == stagione_in_corso)]
        v=v[['Giornata','Voto','FV']]
        v.set_index('Giornata',inplace=True)
        st.line_chart(v, use_container_width=True)
    with col19:
        st.metric('Media Voto', round(v['Voto'].mean(), 2))
        st.metric('Media FV',round(v['FV'].mean(),2))
        st.metric('Presenze', int(v[pd.notnull(v['FV'])].shape[0]))
with tab11:
    st.write("Statistiche carriera")
    vtot=voti_arricchiti()[voti_arricchiti()['Nome'] == sel_player]
    vtot['PreA']=[1 if x!='nan' else 0 for x in vtot['Voto']]
    vgroup=vtot.groupby(['Stagione','Squadra'],as_index=False).agg({'Data':['min','max'],'Titolarita':'sum','PreA':'sum','Voto':'mean','FV':'mean','Gf':'sum','Rf':'sum','Ass':'sum'})
    vgroup.columns=['Stagione','Squadra','Da','A','PreFanta','PreSerieA','MV','MFV','GF','RigF','Ass']
    vgroup=vgroup.sort_values(by=['Da'])
    vgroup['Da']=[x.date() for x in vgroup['Da']]
    vgroup['A'] = [x.date() for x in vgroup['A']]
    vgroup['MV'] = [round(x,2) for x in vgroup['MV']]
    vgroup['MFV'] = [round(x, 2) for x in vgroup['MFV']]
    vgroup['GF'] = [int(x) for x in vgroup['GF']]
    vgroup['RigF'] = [int(x) for x in vgroup['RigF']]
    vgroup['Ass'] = [int(x) for x in vgroup['Ass']]
    st.dataframe(vgroup)
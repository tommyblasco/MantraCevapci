import pandas as pd
import datetime

import streamlit

from funzioni import *

st.title("Aggiornamento operazioni di mercato")
text_input = st.text_input("Inserisci la parola magica per sbloccare il contenuto", placeholder='Vediamo se sei il maestro')

if text_input!='h0lz0ut':
    st.error("Non sei il maestro, perciò non sei autorizzato, pezzo di merda",icon='💩')
else:
    seas=stagione_in_corso
    day=st.date_input('Data evento:')
    type_m=st.radio("Tipologia",("Trattativa","Indennizzo","Svincolo","Rinnovo"),horizontal=True)
    if type_m=="Trattativa":
        colf1, colf2 = st.columns(2)
        with colf1:
            s1=st.selectbox('Scegli squadra 1',tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan']))))
            rosa1 = rosa_oggi(team=s1)
            rosa1=pd.merge(rosa1,giocatori[['Nome','ID']],on='Nome',how='left')
            c1=st.number_input("Quanto cash mette in gioco "+s1,min_value=0.0,max_value=30.0,step=0.05)
            g1=st.multiselect('Scegli i giocatori che vende '+s1,sorted(set(rosa1['ID'])),None)
            tc1,p1,lc1,an1=[],[],[],[]
            for play in g1:
                tc1.append(st.text_input('Tipo contratto per '+str(play),key='t'+str(play)))
                p1.append(st.checkbox(str(play)+" è primavera?",key='p'+str(play)))
                lc1.append(st.slider('Lunghezza contratto per '+str(play),min_value=1,max_value=5,key='lc'+str(play)))
                an1.append(list(rosa1.loc[rosa1['ID']==play,'Data nascita'])[0].year)
        with colf2:
            s2 = st.selectbox('Scegli squadra 2', tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan' and str(x)!=s1]))))
            rosa2 = rosa_oggi(team=s2)
            rosa2 = pd.merge(rosa2, giocatori[['Nome', 'ID']], on='Nome', how='left')
            c2 = st.number_input("Quanto cash mette in gioco "+s2, min_value=0.0, max_value=30.0,step=0.05)
            g2 = st.multiselect('Scegli i giocatori che vende '+s2,sorted(set(rosa2['ID'])), None)
            tc2, p2, lc2, an2 = [], [], [],[]
            for play in g2:
                tc2.append(st.text_input('Tipo contratto per ' + str(play), key='t' + str(play)))
                p2.append(st.checkbox(str(play) + " è primavera?", key='p' + str(play)))
                lc2.append(st.slider('Lunghezza contratto per ' + str(play), min_value=1, max_value=5, key='lc' + str(play)))
                an2.append(list(rosa2.loc[rosa2['ID'] == play, 'Data nascita'])[0].year)
        p_acquisti_s1, p_acquisti_s2 =[],[]
        for i in list(range(len(g2))):
            p_acquisti_s1.append({'Nome':g2[i],'Contract_Type':tc2[i],'Lunghezza':lc2[i],'Primavera':p2[i],'AnnoN':an2[i]})
        for i in list(range(len(g1))):
            p_acquisti_s2.append({'Nome':g1[i],'Contract_Type':tc1[i],'Lunghezza':lc1[i],'Primavera':p1[i],'AnnoN':an1[i]})
        info_s1={'Team':s1,'Acquisti':p_acquisti_s1,'Spesa':c1}
        info_s2={'Team':s2,'Acquisti':p_acquisti_s2,'Spesa':c2}
        if len(g1)+len(g2)>0:
            run_fun_tratt=trattativa(s=seas,day=day,is1=info_s1,is2=info_s2)
            st.dataframe(run_fun_tratt)
        if st.button('Submit trattativa'):
            uq = update_tratt(run_fun_tratt)[0]
            um=update_tratt(run_fun_tratt)[1]
            st.dataframe(um[um['Nome'].isin(run_fun_tratt['Nome'])])
            st.dataframe(uq[uq['Nome'].isin(run_fun_tratt['Nome'])])
            update_file_git(df=um,nome_file="Mercato",comm_mex="tratt "+' '.join(g1+g2))
            update_file_git(df=uq,nome_file="Quotazioni_new",comm_mex="quot "+' '.join(g1+g2))

    elif type_m=='Indennizzo':
        s3 = st.selectbox('Scegli squadra', tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan']))))
        rosa3 = rosa_oggi(team=s3)
        rosa3 = pd.merge(rosa3, giocatori[['Nome', 'ID']], on='Nome', how='left')
        g3 = st.selectbox('Scegli giocatore emigrato', sorted(set(rosa3['ID'])))
        if st.button('Submit indennizzo'):
            inde=indennizzo(s=seas,day=day,da=s3,player=g3)
            st.dataframe(inde[inde['Nome']==g3])
            update_file_git(df=inde, nome_file="Mercato", comm_mex="indennizzo " + g3)

    elif type_m=='Svincolo':
        s4 = st.selectbox('Scegli squadra', tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan']))))
        rosa4 = rosa_oggi(team=s4)
        rosa4 = pd.merge(rosa4, giocatori[['Nome', 'ID']], on='Nome', how='left')
        g4 = st.selectbox('Scegli giocatore da svincolare', sorted(set(rosa4['ID'])))
        c4 = st.number_input("Prezzo di svincolo", min_value=0.0, max_value=30.0, step=0.05)
        if st.button('Submit svincolo'):
            ciao=svincolo(s=seas,day=day,team=s4,player=g4,pre_svi=c4)
            st.dataframe(ciao[ciao['Nome']==g4])
            update_file_git(df=ciao, nome_file="Mercato", comm_mex="svincolo " + g4)

    elif type_m == 'Rinnovo':
        s5 = st.selectbox('Scegli squadra', tuple(sorted(set([x for x in mercato['A'] if str(x) != 'nan']))))
        rosa5 = rosa_oggi(team=s5)
        rosa5 = pd.merge(rosa5, giocatori[['Nome', 'ID']], on='Nome', how='left')
        g5 = st.selectbox('Scegli giocatore da rinnovare', sorted(set(rosa5['ID'])))
        lun5 = st.slider('Durata rinnovo per '+str(g5), min_value=1, max_value=5)
        if st.button('Submit rinnovo'):
            ancora=rinnovo(s=seas,day=day,team=s5,player=g5,l_rin=lun5)
            st.dataframe(ancora[ancora['Nome']==g5])
            update_file_git(df=ancora, nome_file="Mercato", comm_mex="rinnovo " + g5)
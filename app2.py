#---------------Construction app st-----------------------------------------
import streamlit as st  
import plotly.express as px  
#Importer pleins de cryptos
#Choisir quels cryptos on veut investir + montant
#Choisir la date début (simultanée pour tt le monde)
#Fonction valeurs selon les inputs

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Comparatif portfolio/ETF 2022 ", 
                   page_icon=":bar_chart:", 
                   layout="wide")
from datetime import datetime, timedelta

# ---- MAINPAGE ----
st.title(":bar_chart: Comparatif portfolio/ETF")
st.markdown("##")





test_date=datetime.now()
diff = 1
if test_date.weekday() == 0:
    diff = 3
elif test_date.weekday() == 6:
    diff = 2
else :
    diff = 1
res = test_date - timedelta(days=diff)
#date_fin=str(res)[:10]
date_f=st.date_input("Entrer la date de fin voulue",res)
date_fin=str(date_f)[:10]

#--------------------------création du dataset avec yahoo finance--------------
import yfinance as yf
#définition ticker
#ETF
cac_40='^FCHI'
BT_C='BTC=F'
SP_500='ES=F'

#Cryptos du portfolio
LINK='LINK-USD'
ETH='ETH-USD'
AVAX='AVAX-USD'
TH='THETA-USD'
BNB='BNB-USD'
XRP='XRP-USD'
ADA='ADA-USD'
PLG='MATIC-USD'
DOG='DOGE-USD'

#récupération données
cac40=yf.Ticker(cac_40)
BTC=yf.Ticker(BT_C)
SP500=yf.Ticker(SP_500)
ETF=[cac40,SP500,BTC]

LINK=yf.Ticker(LINK)
ETH=yf.Ticker(ETH)
AVAX=yf.Ticker(AVAX)
TH=yf.Ticker(TH)
BNB=yf.Ticker(BNB)
XRP=yf.Ticker(XRP)
ADA=yf.Ticker(ADA)
PLG=yf.Ticker(PLG)
DOG=yf.Ticker(DOG)

CRYPTOS=[LINK,ETH,AVAX,TH,BNB,XRP,ADA,PLG,DOG,BTC]
#récupéation prix sur un pas journalier sur la péiode voulue
date_debut=st.date_input("Entrer la date de début voulue",datetime(2022,1,1))
d=str(date_debut)[:10]
for i in range(len(ETF)):
    ETF[i]=ETF[i].history(period='1d',
                      start=d,
                      end= date_fin)['Close']
for j in range(len(CRYPTOS)):
    CRYPTOS[j]=CRYPTOS[j].history(period='1d',
                      start=d,
                      end= date_fin)['Close']
def liste_index(actif):
    "lister les dates"
    liste_dates=[str(actif.index.tolist()[k])[:10] for k in range(len(actif))]
    return liste_dates
liste_ref=liste_index(CRYPTOS[0]) #N'importe quelle liste de cryptos btc exclu fait l'affaire

        
def mise_a_niveau(liste, num):
    """Fill valeur précédente si le jour concerné était fermé"""
    A = ETF[num]
    ref = liste_ref
    liste_dates = [str(A.index.tolist()[k])[:10] for k in range(len(A))]
    liste = liste.tolist()
    k = 0
    #u=len(ref)-len(liste_dates)
    #for k in range(u):
     #   liste_dates.append('palier à la diffde len')
    while k < len(ref) - 1:
        if liste_dates[k] != ref[k]:
            liste.insert(k, liste[k])
            liste_dates.insert(k, ref[k])
        else:
            k += 1
    return (liste)

#groupement des difféents dataset en gardant des entiers
import pandas as pd

#Mettre la valeur de départ en atttribut aussi. Fonction conversion avec


for k in range(len(ETF)):
    #Mise à  niveau des dates d'ETF
    ETF[k] = mise_a_niveau(ETF[k], k)

#---Sidebar---#
C=['LINK','ETH','AVAX','TH','BNB','XRP','ADA','PLG','DOG','BTC']
st.sidebar.header("Filtrez les cryptos voulues dans votre portfolio")
Cryptos = st.sidebar.multiselect("Selectionnez les cryptos:",options=C,default=C)
Liste_invests=[]
liste_fromage=[]
liste_index_fromage=[]

for k in range(len(C)):
    if C[k] in Cryptos:
        number = st.number_input('Indiquer la somme à investir dans '+C[k])
        Liste_invests.append(number)
        liste_fromage.append(C[k])
        liste_index_fromage.append(k)
        
    else:
        Liste_invests.append(0)
        
        

def nb_asset(num_asset):
    """
    fonction qui renvoi la liste des valeurs journalières d'une crypto
    """
    invest_depart=Liste_invests[num_asset]
    if invest_depart==0:
        return 0
    else:
        return invest_depart/CRYPTOS[num_asset][0]

#Séparer les listes puis les rassembler. D'abord la valeur de chaque crypto, pui on additionne tout 

d1 = []
CRYPTOS[-1]=ETF[2]
for j in range(len(CRYPTOS[0])):
    R=0
    for i in range(len(Liste_invests)):
        R+=int(nb_asset(i)*CRYPTOS[i][j])
    d1.append(R)

  
# Conversion à  l'investissement
a1 = [int(k * d1[0] / ETF[0][0]) for k in ETF[0]]
b1 = [int(k * d1[0] / ETF[1][0]) for k in ETF[1]]

# On met la valeur proportionnel du BTC après avoir fais le calcul pour le pf
c1 = [int(k * d1[0] / ETF[2][0]) for k in ETF[2]]

df = pd.DataFrame(zip(a1, b1, c1, d1)
                  , index=liste_ref
                  , columns=['cac40', 'S&P500', 'BTC', 'Portfolio'])
  
#--------------Fonctions KPI-------------------------------
def perf(indice):
    ret=(indice[-1]-indice[0])/d1[0]
    return str(round(100*ret,1))+'%'
def gain(indice):
    ret=int(indice[-1]-indice[0])
    return str(ret)+'$'
def correlation(x,y):
    
    mX = sum(x)/len(x)
    mY = sum(y)/len(y)
    cov = sum((a - mX) * (b - mY) for (a,b) in zip(x,y)) / len(x)
    stdevX = (sum((a - mX)**2 for a in x)/len(x))**0.5
    stdevY = (sum((b - mY)**2 for b in y)/len(y))**0.5
    if cov==0 or stdevX==0 or stdevY==0:
        return("En attente des dates")
    result = round(cov/(stdevX*stdevY),3)
    return(str(round(result*100,1))+'%')


# TOP KPI's
indice_perf = pd.DataFrame({'Indices':['cac40','S&P50','BTC','Portfolio'],
                           'Performances' :[perf(df['cac40']),
                                            perf(df['S&P500']),
                                            perf(df['BTC']),
                                            perf(df['Portfolio'])]})

valeur_actuelle = str(df['Portfolio'][-1])+'$'
#On fera la même pour les autres actifs
corrélation_BTC = correlation(df['Portfolio'], df['BTC'])

first_column, second_column, last_column = st.columns(3)

first_column.metric(label='valeur initiale du portfolio',
                    value=str(d1[0])+'$') 

second_column.metric(label='valeur actuelle du portfolio',
                    value=valeur_actuelle,
                    delta=perf(df['Portfolio']))  

last_column.metric(label='Corrélation du portfolio au BTC',
                    value=corrélation_BTC) 

st.markdown("""---""")

#----graphs----
new_df=df.assign(Date=liste_ref)
courbe = px.line(new_df,x='Date', y=['cac40',
                                 'S&P500',
                                 'BTC',
                                 'Portfolio'],
                 title='Comparatif portfolio/indices',
                 width=620,
                 labels={
                     "value" : "valeur investissement ($)",
                     "x" : "Dates",
                     "variable" : "Indices"
                 })

#Rapport crypto/invest
CR=[]
for k in range(len(CRYPTOS)):
    if k in liste_index_fromage:
        CR.append(int(nb_asset(k)*CRYPTOS[k][-1]))


fromage = px.pie(values=CR, names=liste_fromage,title="Répartition du portfolio",width=450)
left_column, right_column = st.columns([2,1])
left_column.plotly_chart(courbe)
right_column.plotly_chart(fromage)

st.markdown("""---""")

a,b,c,d=st.columns(4)

a.metric(label='Bénéfice cac40',
         value=gain(df['cac40']),
         delta=perf(df['cac40']))
b.metric(label='Bénéfice S&P500',
         value=gain(df['S&P500']),
         delta=perf(df['S&P500']))
c.metric(label='Bénéfice BTC',
         value=gain(df['BTC']),
         delta=perf(df['BTC']))
d.metric(label='Bénéfice Portfolio',
         value=gain(df['Portfolio']),
         delta=perf(df['Portfolio']))       
         


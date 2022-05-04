import numpy as np 
import pandas as pd
forecast = pd.read_json("https://raw.githubusercontent.com/giovanniardenghi/dpc-covid-data/main/SUIHTER/MCMC_forecasts/Controlled_5.json")
forecastL = pd.read_json("https://raw.githubusercontent.com/giovanniardenghi/dpc-covid-data/main/SUIHTER/MCMC_forecasts/Controlled_025.json")
forecastU = pd.read_json("https://raw.githubusercontent.com/giovanniardenghi/dpc-covid-data/main/SUIHTER/MCMC_forecasts/Controlled_975.json")

data = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')

print(data['deceduti'].diff())

data['Deceduti giornalieri'] = np.concatenate([data['deceduti'].diff()])

comp = ['Nuovi positivi', 'Positivi', 'Ricoverati (non in terapia intensiva)', 'Ricoverati in terapia intensiva',  'Deceduti giornalieri']
label = ['Casi giornalieri', 'Positivi', 'Ricoverati in reparti ordinari', 'Ricoverati in terapia intensiva',  'Deceduti giornalieri']
comp2 = ['nuovi_positivi', 'totale_positivi', 'ricoverati_con_sintomi', 'terapia_intensiva',  'Deceduti giornalieri']

table = pd.DataFrame(columns=['Compartment','Past week','Next week','trend','Next week 0.025','Next week 0.975'])

for i in range(5):
#    print(data[comp2[i]].iloc[-7:])
#    print(forecast[comp[i]].iloc[1:8])
    if int(forecast[comp[i]].iloc[1:8].mean()) > int(data[comp2[i]].iloc[-7:].mean()):
        trend = '&uArr;'
    else:
        trend = '&dArr;'
    table = table.append({'Compartment': label[i], 
                          'Past week': int(data[comp2[i]].iloc[-7:].mean()),
                          'Next week': int(forecast[comp[i]].iloc[1:8].mean()),
                          'trend': trend,
                          'Next week 0.025': int(forecastL[comp[i]].iloc[1:8].mean()),
                          'Next week 0.975': int(forecastU[comp[i]].iloc[1:8].mean())}, ignore_index=True)
    #print(comp[i],int(data[comp2[i]].iloc[-7:].mean()),int(forecast[comp[i]].iloc[1:8].mean()),int(forecastL[comp[i]].iloc[1:8].mean()),int(forecastU[comp[i]].iloc[1:8].mean()))


table.to_csv('data.csv')

print(table)

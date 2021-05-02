import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import datetime
import os
import sys

import csv

iadays=14
dias=[]
csvin=sys.argv[1]
try:
    #with open(csvin, 'r', encoding="ISO-8859-1") as f:
    with open(csvin, 'r') as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
        dias=headers[0].split(",")
        dias=headers
        # Borrar el último elemento porque el ; del final hace que añada un campo vacío
        del dias[len(dias)-1]
        del dias[len(dias)-1]
except:
    print("No puedo leer el csv1")

dias7=dias

    

#print(dias)
shpmap = "PARA_FTP_V2/CB_MUNICIPIOS_5000_ETRS89.shp"
mapa = gpd.read_file(shpmap)
#mapa.plot(figsize=(10, 10))
#plt.show()
#pd.set_option('display.max_rows', None)
#print(mapa.head(5))
os.makedirs("dailymaps", exist_ok=True)

#Usar solamente los 14 últimos días
numdias=len(dias)
del dias[0:numdias - iadays]
del dias7[0:(len(dias7)) - 7]
print(dias7)


def plotmap(df, datacol, vmax, filename, title):
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=0, vmax=vmax))
    fig, ax = plt.subplots(1, figsize=(35, 20))
    ax.axis("off") 
    ax.set_title(title, fontdict={'fontsize': '25', 'fontweight' : '3'}) 
    ax.annotate("Gobierno Vasco / Elaboración propia", xy=(0.48, 0.11), 
    xycoords='figure fraction', fontsize=25, color='#555555')
    sm.set_array([])
    cbar=fig.colorbar(sm, ax=ax, extend="max")
    for t in cbar.ax.get_yticklabels():
     t.set_fontsize(20)
    df['coords'] = df['geometry'].apply(lambda x: x.representative_point().coords[:]) 
    df['coords'] = [coords[0] for coords in df['coords']]
    for idx, row in df.iterrows():
        #plt.annotate(s=row['NOMBRE_TOP'], xy=row['coords'],horizontalalignment='center') 
        df.plot(column=datacol, cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', vmax=vmax) 
    fig.savefig(filename, dpi=50)

#df = pd.read_csv (r'datos_municipios.csv',encoding='iso-8859-1',low_memory=False, delimiter=';',usecols=dias)
try:
    #print(dias7)
    df = pd.read_csv (csvin,low_memory=False, delimiter=',',usecols=dias)
    df2 = pd.read_csv (csvin,low_memory=False, delimiter=',',usecols=dias7)
    df["total14dias"] = df.sum(axis=1)
    df["total7dias"] = df2.sum(axis=1)

    df1 = pd.read_csv (r'municipios_poblacion_postal.csv')

    finaldf = pd.concat([df1, df], axis=1, join='inner')

    finaldf['IA14'] = finaldf['total14dias']/finaldf['Biztanleak/Población']*100000
    finaldf['IA14']= finaldf['IA14'].astype(int)
    finaldf['IA7'] = finaldf['total7dias']/finaldf['Biztanleak/Población']*100000
    finaldf['IA7']= finaldf['IA7'].astype(int)

    #finaldf.to_csv('result.csv')
    #print(finaldf["Udalerria kodea / Código municipio"])
    print("Opening "+csvin)

    merged_df2 = mapa.merge(finaldf, how="left", left_on="NOMBRE_TOP", right_on="Udalerria / Municipio")

    hdate = dias[len(dias)-1]
    stamp = hdate.replace("/","_")

    pd.set_option('display.max_rows', None)
    #print(merged_df2)
    plotmap(merged_df2, "IA14", 500, f"dailymaps/map_IA14_{stamp}.png", f"IA 14 días 100.000 habitantes [{hdate}]")
    plotmap(merged_df2, "IA7", 500, f"dailymaps/map_IA7_{stamp}.png", f"IA 7 días 100.000 habitantes [{hdate}]")
    plotmap(merged_df2, hdate, 200, f"dailymaps/map_abs_{stamp}.png", f"# casos por municipio [{hdate}]")
except:
    print("No puedo leer el csv2")
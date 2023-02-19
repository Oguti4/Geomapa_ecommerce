#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pylab import rcParams
import matplotlib.pyplot as plt
import dash_auth

import plotly.graph_objects as go
from datetime import datetime

import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input,Output


# In[2]:


ALL_DATA=pd.read_csv('DATOS.csv', encoding="ISO-8859-1")
ALL_DATA['FECHA_ven']=pd.to_datetime(ALL_DATA.Fecha_ven)


# In[3]:


DF2=ALL_DATA[ALL_DATA['SUCURSAL']=='SUCURSAL_3']
DF3=ALL_DATA[ALL_DATA['SUCURSAL']=='SUCURSAL_2']
DF4=ALL_DATA[ALL_DATA['SUCURSAL']=='SUCURSAL_1']
DF2['SUCURSAL']='AMAZON'
DF3['SUCURSAL']='MERCADOLIBRE'
DF4['SUCURSAL']='INTERNET'
ALL_DATA=pd.concat([DF2,DF3,DF4])
del DF2,DF3,DF4


# In[4]:


grades=ALL_DATA.TOTAL_VENTA.tolist()
ALL_DATA['TOTAL_VENTA']=[float(g) for g in grades]
ALL_DATA=ALL_DATA[ALL_DATA['TOTAL_VENTA']>=10]

grades=ALL_DATA.CODIGO_BARRAS.tolist()
ALL_DATA['BARRAS']=[str(g) for g in grades]
ALL_DATA['BARRAS']=ALL_DATA.BARRAS.str.split(".", expand = True)[0]

grades=ALL_DATA.MES.tolist()
ALL_DATA['MES']=[str(g) for g in grades]
ALL_DATA['MES']=ALL_DATA.MES.str.split(".", expand = True)[0]

grades=ALL_DATA.PERIODO.tolist()
ALL_DATA['PERIODO']=[str(g) for g in grades]
ALL_DATA['PERIODO']=ALL_DATA.PERIODO.str.split(".", expand = True)[0]


# In[5]:


# fecha de un dia antes
Fecha_inicio='2023-01-01'
Fecha_inicio_top='2023-01-01'
Fecha_fin='2023-02-06'
Fecha_inicio_2022='2023-01-01'
mes='Feb'
dia='-06'
date_fin=mes+dia
date_inicio_top='Feb-01'


# In[6]:


ALL_DATA_22=ALL_DATA[(ALL_DATA['FECHA_ven']>=Fecha_inicio_2022)&(ALL_DATA['FECHA_ven']<=Fecha_fin)]  ##primera linea

ALL_DATA_22_gral=pd.concat([ALL_DATA_22])
ALL_DATA_22_gral['SUCURSAL']='TOTAL CADENA'
ALL_DATA_22=pd.concat([ALL_DATA_22,ALL_DATA_22_gral])

#base libros
ALL_22=ALL_DATA[(ALL_DATA['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA['FECHA_ven']>=Fecha_inicio)&(ALL_DATA['FECHA_ven']<=Fecha_fin)]
ALL_22_gral=pd.concat([ALL_22])
ALL_22_gral['SUCURSAL']='TOTAL CADENA'
ALL_22=pd.concat([ALL_22,ALL_22_gral])


ALL_22_sub=ALL_DATA[(ALL_DATA['TIPO_PRODUCTO']=='Producto 1')&(ALL_DATA['FECHA_ven']>=Fecha_inicio_top)&(ALL_DATA['FECHA_ven']<=Fecha_fin)]
ALL_22_sub_gral=pd.concat([ALL_22_sub])
ALL_22_sub_gral['SUCURSAL']='TOTAL CADENA'
ALL_22_sub=pd.concat([ALL_22_sub,ALL_22_sub_gral])

#base accesorios
ALL_22_acce=ALL_DATA[(ALL_DATA['TIPO_PRODUCTO']=='Producto 2')&(ALL_DATA['FECHA_ven']>=Fecha_inicio)&(ALL_DATA['FECHA_ven']<=Fecha_fin)]
ALL_22_acce_gral=pd.concat([ALL_22_acce])
ALL_22_acce_gral['SUCURSAL']='TOTAL CADENA'
ALL_22_acce=pd.concat([ALL_22_acce,ALL_22_acce_gral])

ALL_22_sub_acce=ALL_DATA[(ALL_DATA['TIPO_PRODUCTO']=='Producto 2')&(ALL_DATA['FECHA_ven']>=Fecha_inicio_top)&(ALL_DATA['FECHA_ven']<=Fecha_fin)]
ALL_22_sub_acce_gral=pd.concat([ALL_22_sub_acce])
ALL_22_sub_acce_gral['SUCURSAL']='TOTAL CADENA'
ALL_22_sub_acce=pd.concat([ALL_22_sub_acce,ALL_22_sub_acce_gral])

del ALL_DATA_22_gral, ALL_22_gral,ALL_22_sub_gral,ALL_22_acce_gral,ALL_22_sub_acce_gral


# In[7]:


VENTAS1=ALL_22_sub.groupby(['SUCURSAL','BARRAS','TITULO','PROVEEDOR']).sum().reset_index().sort_values(by='CANTIDAD_VENTA',ascending=False)
VENTAS2=ALL_22_sub[ALL_22_sub['FECHA_ven']==Fecha_fin].groupby(['SUCURSAL','BARRAS','TITULO','PROVEEDOR']).sum().reset_index().sort_values(by='CANTIDAD_VENTA',ascending=False)

DFF1=ALL_22_sub.groupby(['SUCURSAL','BARRAS','TITULO','PROVEEDOR','FOLIO_VENTA']).count()[['PERIODO']].reset_index()
DFF1=DFF1.groupby(['SUCURSAL','BARRAS','TITULO','PROVEEDOR']).count()[['FOLIO_VENTA']].reset_index()
DFF1.columns=['SUCURSAL','BARRAS','TITULO','PROVEEDOR','FOLIOS']
VENTAS1=pd.merge( VENTAS1,DFF1, on=['SUCURSAL','BARRAS','TITULO','PROVEEDOR'], how='outer').head(len(VENTAS1)).fillna(0)

DFF1=ALL_22_sub[ALL_22_sub['FECHA_ven']==Fecha_fin].groupby(['SUCURSAL','BARRAS','TITULO','PROVEEDOR','FOLIO_VENTA']).count()[['PERIODO']].reset_index()
DFF1=DFF1.groupby(['SUCURSAL','BARRAS','TITULO','PROVEEDOR']).count()[['FOLIO_VENTA']].reset_index()
DFF1.columns=['SUCURSAL','BARRAS','TITULO','PROVEEDOR','FOLIOS']
VENTAS2=pd.merge( VENTAS2,DFF1, on=['SUCURSAL','BARRAS','TITULO','PROVEEDOR'], how='outer').head(len(VENTAS2)).fillna(0)

VENTAS1['CLAVE']=VENTAS1['SUCURSAL']+VENTAS1['BARRAS']
VENTAS2['CLAVE']=VENTAS2['SUCURSAL']+VENTAS2['BARRAS']


# In[8]:


lista=VENTAS1.SUCURSAL.unique().tolist()
DAT1=pd.DataFrame()
DAT11=pd.DataFrame()
for i in lista:
    DAT2=VENTAS1[VENTAS1['SUCURSAL']==i].head(50)
    DAT22=VENTAS2[VENTAS2['SUCURSAL']==i].head(50)
    DAT1=pd.concat([DAT1,DAT2])
    DAT11=pd.concat([DAT11,DAT22])


# In[9]:


ALL_DATA_22=ALL_DATA_22.groupby(['SUCURSAL','FECHA_ven','LINEA_NEGOCIO','TIPO_PRODUCTO']).sum()[['CANTIDAD_VENTA','TOTAL_VENTA']].reset_index()
ALL_DATA_22['FECHA_ven']=pd.to_datetime(ALL_DATA_22.FECHA_ven)

ALL_DATA_22['Año'] = ALL_DATA_22['FECHA_ven'].dt.year 
ALL_DATA_22['Mes'] = ALL_DATA_22['FECHA_ven'].dt.month 
ALL_DATA_22['Dia'] = ALL_DATA_22['FECHA_ven'].dt.day 
look_up = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May',
            6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
ALL_DATA_22['Mes'] = ALL_DATA_22['Mes'].apply(lambda x: look_up[x])

#base de linea de negocio y tipo de producto


# In[10]:


### LIBROS


# In[11]:


lista=ALL_22.SUCURSAL.unique().tolist()
RESET=pd.DataFrame()
for i in lista:
    DAT=ALL_22[ALL_22['SUCURSAL']==i]
    DAT2=ALL_22_sub[ALL_22_sub['SUCURSAL']==i]
    top=DAT2.groupby(['SUBTEMA_']).sum().sort_values(by='TOTAL_VENTA',ascending=False).head(20).reset_index()[['SUBTEMA_']]
    top['top']='SI'
    ALL_22_TOP=pd.merge( DAT,top, on='SUBTEMA_', how='outer').head(len(DAT))
    ALL_22_1=ALL_22_TOP[ALL_22_TOP['top']=='SI']
    ALL_22_2=ALL_22_TOP[ALL_22_TOP['top']!='SI']
    ALL_22_2['SUBTEMA_']='OTROS'
    ALL_22_TOP=pd.concat([ALL_22_1,ALL_22_2])
    RESET=pd.concat([RESET,ALL_22_TOP])
    
VENTA_DIARIA=pd.DataFrame()
for i in lista:
    DAT=RESET[RESET['SUCURSAL']==i]
    top=DAT.groupby(['SUBTEMA_']).sum().sort_values(by='TOTAL_VENTA',ascending=False).reset_index()[['SUBTEMA_']]
    sub=top.SUBTEMA_.tolist()[::-1]
    AREAT=pd.DataFrame()
    for j in sub:
        day = DAT[DAT['SUBTEMA_']==j]
        test=pd.DataFrame({'FECHA':day.FECHA_ven, 'VENTA':day.TOTAL_VENTA,'CANTIDAD_VENTA':day.CANTIDAD_VENTA})
        days=test.groupby(pd.Grouper(key='FECHA',freq='1d')).sum()
        days['SUBTEMA']=j
        AREAT=pd.concat([days,AREAT])  
    AREAT['SUCURSAL']=i
    VENTA_DIARIA=pd.concat([AREAT,VENTA_DIARIA])


# In[12]:


lista=ALL_22.SUCURSAL.unique().tolist()
RESET=pd.DataFrame()
for i in lista:
    DAT=ALL_22[ALL_22['SUCURSAL']==i]
    DAT2=ALL_22_sub[ALL_22_sub['SUCURSAL']==i]
    top=DAT2.groupby(['SUBTEMA_']).sum().sort_values(by='TOTAL_VENTA',ascending=False).head(20).reset_index()[['SUBTEMA_']]
    top['top']='SI'
    ALL_22_TOP=pd.merge( DAT,top, on='SUBTEMA_', how='outer').head(len(DAT))
    ALL_22_1=ALL_22_TOP[ALL_22_TOP['top']=='SI']
    ALL_22_2=ALL_22_TOP[ALL_22_TOP['top']!='SI']
    ALL_22_2['SUBTEMA_']='OTROS'
    ALL_22_TOP=pd.concat([ALL_22_1,ALL_22_2])
    RESET=pd.concat([RESET,ALL_22_TOP])
    
VENTA_SEMANAL=pd.DataFrame()
for i in lista:
    DAT=RESET[RESET['SUCURSAL']==i]
    top=DAT.groupby(['SUBTEMA_']).sum().sort_values(by='TOTAL_VENTA',ascending=False).reset_index()[['SUBTEMA_']]
    sub=top.SUBTEMA_.tolist()[::-1]
    AREAT=pd.DataFrame()
    for j in sub:
        day = DAT[DAT['SUBTEMA_']==j]
        test=pd.DataFrame({'FECHA':day.FECHA_ven, 'VENTA':day.TOTAL_VENTA,'CANTIDAD_VENTA':day.CANTIDAD_VENTA})
        days=test.groupby(pd.Grouper(key='FECHA',freq='1w')).sum()
        days['SUBTEMA']=j
        AREAT=pd.concat([days,AREAT])  
    AREAT['SUCURSAL']=i
    VENTA_SEMANAL=pd.concat([AREAT,VENTA_SEMANAL])


# In[13]:


#PROVEEDOR
lista=ALL_22.SUCURSAL.unique().tolist()
RESET=pd.DataFrame()
for i in lista:
    DAT=ALL_22[ALL_22['SUCURSAL']==i]
    DAT2=ALL_22_sub[ALL_22_sub['SUCURSAL']==i]
    top=DAT2.groupby(['PROVEEDOR']).sum().sort_values(by='TOTAL_VENTA',ascending=False).head(20).reset_index()[['PROVEEDOR']]
    top['top']='SI'
    ALL_22_TOP=pd.merge( DAT,top, on='PROVEEDOR', how='outer').head(len(DAT))
    ALL_22_1=ALL_22_TOP[ALL_22_TOP['top']=='SI']
    ALL_22_2=ALL_22_TOP[ALL_22_TOP['top']!='SI']
    ALL_22_2['PROVEEDOR']='OTROS'
    ALL_22_TOP=pd.concat([ALL_22_1,ALL_22_2])
    RESET=pd.concat([RESET,ALL_22_TOP])
    
VENTA_DIARIA_prov=pd.DataFrame()
for i in lista:
    DAT=RESET[RESET['SUCURSAL']==i]
    top=DAT.groupby(['PROVEEDOR']).sum().sort_values(by='TOTAL_VENTA',ascending=False).reset_index()[['PROVEEDOR']]
    sub=top.PROVEEDOR.tolist()[::-1]
    AREAT=pd.DataFrame()
    for j in sub:
        day = DAT[DAT['PROVEEDOR']==j]
        test=pd.DataFrame({'FECHA':day.FECHA_ven, 'VENTA':day.TOTAL_VENTA,'CANTIDAD_VENTA':day.CANTIDAD_VENTA})
        days=test.groupby(pd.Grouper(key='FECHA',freq='1d')).sum()
        days['PROVEEDOR']=j
        AREAT=pd.concat([days,AREAT])  
    AREAT['SUCURSAL']=i
    VENTA_DIARIA_prov=pd.concat([AREAT,VENTA_DIARIA_prov])


# In[14]:


lista=ALL_22.SUCURSAL.unique().tolist()
RESET=pd.DataFrame()
for i in lista:
    DAT=ALL_22[ALL_22['SUCURSAL']==i]
    DAT2=ALL_22_sub[ALL_22_sub['SUCURSAL']==i]
    top=DAT2.groupby(['PROVEEDOR']).sum().sort_values(by='TOTAL_VENTA',ascending=False).head(20).reset_index()[['PROVEEDOR']]
    top['top']='SI'
    ALL_22_TOP=pd.merge( DAT,top, on='PROVEEDOR', how='outer').head(len(DAT))
    ALL_22_1=ALL_22_TOP[ALL_22_TOP['top']=='SI']
    ALL_22_2=ALL_22_TOP[ALL_22_TOP['top']!='SI']
    ALL_22_2['PROVEEDOR']='OTROS'
    ALL_22_TOP=pd.concat([ALL_22_1,ALL_22_2])
    RESET=pd.concat([RESET,ALL_22_TOP])
VENTA_SEMANAL_prov=pd.DataFrame()
for i in lista:
    DAT=RESET[RESET['SUCURSAL']==i]
    top=DAT.groupby(['PROVEEDOR']).sum().sort_values(by='TOTAL_VENTA',ascending=False).reset_index()[['PROVEEDOR']]
    sub=top.PROVEEDOR.tolist()[::-1]
    AREAT=pd.DataFrame()
    for j in sub:
        day = DAT[DAT['PROVEEDOR']==j]
        test=pd.DataFrame({'FECHA':day.FECHA_ven, 'VENTA':day.TOTAL_VENTA,'CANTIDAD_VENTA':day.CANTIDAD_VENTA})
        days=test.groupby(pd.Grouper(key='FECHA',freq='1w')).sum()
        days['PROVEEDOR']=j
        AREAT=pd.concat([days,AREAT])  
    AREAT['SUCURSAL']=i
    VENTA_SEMANAL_prov=pd.concat([AREAT,VENTA_SEMANAL_prov])


# In[15]:


VENTA_DIARIA=VENTA_DIARIA.reset_index()#.hist()
VENTA_SEMANAL=VENTA_SEMANAL.reset_index()#.hist()

VENTA_DIARIA.SUBTEMA=VENTA_DIARIA.SUBTEMA.str.split(" Y ",expand=True)[0]
VENTA_DIARIA.SUBTEMA=VENTA_DIARIA.SUBTEMA.str.split(" U ",expand=True)[0]

VENTA_SEMANAL.SUBTEMA=VENTA_SEMANAL.SUBTEMA.str.split(" Y ",expand=True)[0]
VENTA_SEMANAL.SUBTEMA=VENTA_SEMANAL.SUBTEMA.str.split(" U ",expand=True)[0]

VENTA_DIARIA['TIPO']='VENTA DIARIA'
VENTA_SEMANAL['TIPO']='VENTA SEMANAL'

df3=pd.concat([VENTA_DIARIA,VENTA_SEMANAL])
df3['Fecha']=pd.to_datetime(df3.FECHA)


# In[ ]:





# In[16]:


VENTA_DIARIA_prov=VENTA_DIARIA_prov.reset_index()#.hist()
VENTA_SEMANAL_prov=VENTA_SEMANAL_prov.reset_index()#.hist()

VENTA_DIARIA_prov.PROVEEDOR=VENTA_DIARIA_prov.PROVEEDOR.str.split(" Y ",expand=True)[0]
VENTA_DIARIA_prov.PROVEEDOR=VENTA_DIARIA_prov.PROVEEDOR.str.split(" U ",expand=True)[0]

VENTA_SEMANAL_prov.PROVEEDOR=VENTA_SEMANAL_prov.PROVEEDOR.str.split(" Y ",expand=True)[0]
VENTA_SEMANAL_prov.PROVEEDOR=VENTA_SEMANAL_prov.PROVEEDOR.str.split(" U ",expand=True)[0]

VENTA_DIARIA_prov['TIPO']='VENTA DIARIA'
VENTA_SEMANAL_prov['TIPO']='VENTA SEMANAL'

df3_prov=pd.concat([VENTA_DIARIA_prov,VENTA_SEMANAL_prov])
df3_prov['Fecha']=pd.to_datetime(df3_prov.FECHA)

## FIN DE LIBROS


# In[17]:


ALL_22_acce2=ALL_22_acce.groupby(['SUCURSAL','FECHA_ven','LINEA_NEGOCIO','PROVEEDOR']).sum()[['CANTIDAD_VENTA','TOTAL_VENTA']].reset_index()
ALL_22_acce2['FECHA_ven']=pd.to_datetime(ALL_22_acce2.FECHA_ven)
ALL_22_acce2['Año'] = ALL_22_acce2['FECHA_ven'].dt.year 
ALL_22_acce2['Mes'] = ALL_22_acce2['FECHA_ven'].dt.month 
ALL_22_acce2['Dia'] = ALL_22_acce2['FECHA_ven'].dt.day 
look_up = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May',
            6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}

ALL_22_acce2['Mes'] = ALL_22_acce2['Mes'].apply(lambda x: look_up[x])


# In[18]:


ALL_22_sub_acce2=ALL_22_sub_acce.groupby(['SUCURSAL','FECHA_ven','LINEA_NEGOCIO','PROVEEDOR']).sum()[['CANTIDAD_VENTA','TOTAL_VENTA']].reset_index()
ALL_22_sub_acce2['FECHA_ven']=pd.to_datetime(ALL_22_sub_acce2.FECHA_ven)
ALL_22_sub_acce2['Año'] = ALL_22_sub_acce2['FECHA_ven'].dt.year 
ALL_22_sub_acce2['Mes'] = ALL_22_sub_acce2['FECHA_ven'].dt.month 
ALL_22_sub_acce2['Dia'] = ALL_22_sub_acce2['FECHA_ven'].dt.day 
look_up = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May',
            6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
ALL_22_sub_acce2['Mes'] = ALL_22_sub_acce2['Mes'].apply(lambda x: look_up[x])


# In[19]:


MAPAS=pd.read_csv('Venta.csv')
CONSULTA=pd.read_csv('Consulta.csv')
CARGA=pd.read_csv('Carga.csv')


# In[20]:


MAPAS1=pd.read_csv('Venta_dia.csv')
MAPAS11=pd.read_csv('Consulta_dia.csv')
MAPAS111=pd.read_csv('Carga_dia.csv')


# In[ ]:





# In[21]:


LAT_LONG1=pd.read_csv('LUGARES_LAT_LONG_ALL.csv')
LAT_LONG2=pd.read_csv('LUGARES_LAT_LONG_ALL.csv')

LAT_LONG1['ESTADO']=LAT_LONG1['SUCURSAL']
LAT_LONG1['SUCURSAL']='TOTAL CADENA'

LAT_LONG=pd.concat([LAT_LONG1,LAT_LONG2])
LAT_LONG.COLONIA=LAT_LONG.COLONIA.str.split(",", expand = True)[0]

REF1=LAT_LONG2.groupby(['SUCURSAL','ESTADO','LUGAR']).sum()[['ENVIOS','CANTIDAD']].reset_index().sort_values(by='ENVIOS',ascending=False)
REF2=LAT_LONG2.groupby(['SUCURSAL','ESTADO','LUGAR']).sum()[['ENVIOS','CANTIDAD']].reset_index()
REF2['SUCURSAL']='TOTAL CADENA'
REF2=REF2.groupby(['SUCURSAL','ESTADO','LUGAR']).sum()[['ENVIOS','CANTIDAD']].reset_index().sort_values(by='ENVIOS',ascending=False)
REF_ALL=pd.concat([REF1,REF2])
del REF1, REF2,LAT_LONG1,LAT_LONG2


# In[22]:


LAT_LONG1=pd.read_csv('LUGARES_LAT_LONG.csv')
LAT_LONG2=pd.read_csv('LUGARES_LAT_LONG.csv')

LAT_LONG1['ESTADO']=LAT_LONG1['SUCURSAL']
LAT_LONG1['SUCURSAL']='TOTAL CADENA'

LAT_LONG=pd.concat([LAT_LONG1,LAT_LONG2])
LAT_LONG.COLONIA=LAT_LONG.COLONIA.str.split(",", expand = True)[0]

REF1=LAT_LONG2.groupby(['SUCURSAL','ESTADO','LUGAR']).sum()[['ENVIOS','CANTIDAD']].reset_index().sort_values(by='ENVIOS',ascending=False)
REF2=LAT_LONG2.groupby(['SUCURSAL','ESTADO','LUGAR']).sum()[['ENVIOS','CANTIDAD']].reset_index()
REF2['SUCURSAL']='TOTAL CADENA'
REF2=REF2.groupby(['SUCURSAL','ESTADO','LUGAR']).sum()[['ENVIOS','CANTIDAD']].reset_index().sort_values(by='ENVIOS',ascending=False)
REF=pd.concat([REF1,REF2])
del REF1, REF2,LAT_LONG1,LAT_LONG2


# In[23]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div([
    
    html.Div([
        html.H1('Comportamiento de ventas (Prueba) - CONFIDENCIAL ', style={'fontSize': 30,'font-family':'sans-serif'}),
        html.Img(src='assets/MULTICANAL.PNG')
    ],style = {}, className = 'banner'),

    html.Div([
        html.Div([
            html.P('Selecciona la Sucursal', className = 'fix_label', style={'color':'black', 'margin-top': '4px'}),
            dcc.RadioItems(id = 'items', 
                            labelStyle = {'display': 'inline-block'},
                            options = [
                                {'label' : 'TOTAL CADENA', 'value' : 'TOTAL CADENA'},
                                {'label' : 'MERCADOLIBRE', 'value' : 'MERCADOLIBRE'},
                                {'label' : 'AMAZON', 'value' : 'AMAZON'},
                                {'label' : 'INTERNET', 'value' : 'INTERNET'},

                            ], value = 'TOTAL CADENA',
                            style = {'text-aling':'center', 'color':'navy'}, className = 'dcc_compon'),
        ], className = 'create_container2 thirteen columns', style = {'margin-bottom': '10px'}),
    ], className = 'row flex-display'),
##################################################################------------------------------
    
##################################################################------------------------------
    html.Div([
        html.H1('¿A donde llegan los envios" ?', style={'fontSize': 22,'font-family':'sans-serif'})
    ],style = {}, className = 'banner2'),    
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'geomapa_graph1', figure = {})
        ], className = 'create_container1 eight columns'),
        
        html.Div([
            dcc.Graph(id = 'table_top_1', figure = {})
        ], className = 'create_container1 five columns'),

        
    ], className = 'row flex-display'),   
##################################################################------------------------------
    html.Div([
        html.H1('¿Que días y horas predomina la venta?', style={'fontSize': 22,'font-family':'sans-serif'})
    ],style = {}, className = 'banner2'),    
##################################################################------------------------------    
    
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'mapa_graph1_1', figure = {})
        ], className = 'create_container1 six columns'),
        
        html.Div([
            dcc.Graph(id = 'mapa_graph1_2', figure = {})
        ], className = 'create_container1 six columns'),
        
        html.Div([
            dcc.Graph(id = 'mapa_graph1_3', figure = {})
        ], className = 'create_container1 six columns'),
        
    ], className = 'row flex-display'),
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'mapa_graph2_1', figure = {})
        ], className = 'create_container1 six columns'),
        
        html.Div([
            dcc.Graph(id = 'mapa_graph2_2', figure = {})
        ], className = 'create_container1 six columns'),
        
        html.Div([
            dcc.Graph(id = 'mapa_graph2_3', figure = {})
        ], className = 'create_container1 six columns'),
        
    ], className = 'row flex-display'),    
    
    
##################################################################------------------------------
    html.Div([
        html.H1('Comportamiento de ventas por linea de negocio y tipo de producto', style={'fontSize': 22,'font-family':'sans-serif'})
    ],style = {}, className = 'banner2'),    
##################################################################------------------------------
    
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'area_graph1_1', figure = {})
        ], className = 'create_container1 eight columns'),
        html.Div([
            dcc.Graph(id = 'sun_graph1_1', figure = {})
        ], className = 'create_container1 five columns'),
    ], className = 'row flex-display'),
##################################################################------------------------------

    html.Div([
        html.Div([
            dcc.Graph(id = 'area_graph1_2', figure = {})
        ], className = 'create_container1 eight columns'),
        html.Div([
            dcc.Graph(id = 'sun_graph1_2', figure = {})
        ], className = 'create_container1 five columns'),
    ], className = 'row flex-display'),
##################################################################------------------------------
    html.Div([
        html.H1('PRODUCTOS - TOP 20 de '+date_inicio_top+' a '+date_fin+', subtema y proveedor', style={'fontSize': 22,'font-family':'sans-serif'})
    ],style = {}, className = 'banner3'),        
##################################################################------------------------------    
    html.Div([
        html.Div([
            dcc.Graph(id = 'line_graph2_1', figure = {})
        ], className = 'create_container1 eight columns'),
        html.Div([
            dcc.Graph(id = 'pie_graph2_1', figure = {})
        ], className = 'create_container1 five columns'),
    ], className = 'row flex-display'),    
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'line_graph2_2', figure = {})
        ], className = 'create_container1 eight columns'),
        html.Div([
            dcc.Graph(id = 'pie_graph2_2', figure = {})
        ], className = 'create_container1 five columns'),
    ], className = 'row flex-display'),    
##################################################################------------------------------
##################################################################------------------------------


], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})


# In[ ]:


##################################################################------------------------------
num=len(ALL_DATA_22.FECHA_ven.unique())

@app.callback(
    Output('sun_graph1_1', component_property='figure'),
    [Input('items', component_property='value')])
def update_graph_pie(value):
    fig1 = px.sunburst(ALL_DATA_22[ALL_DATA_22['SUCURSAL']==value], path=['Mes','LINEA_NEGOCIO','TIPO_PRODUCTO'], values='TOTAL_VENTA',
                  color='TOTAL_VENTA',color_continuous_scale='tempo')
        
    fig1.update_traces(textinfo="label+percent parent")
    fig1.update_layout(title='Participación por linea de negocio, de Enero-01 a '+date_fin,height=450)
    return (fig1)

@app.callback(
    Output('area_graph1_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.histogram(ALL_DATA_22[ALL_DATA_22['SUCURSAL']==value], x="FECHA_ven", y="TOTAL_VENTA", color="LINEA_NEGOCIO", nbins=num)
    fig2.update_layout(title='Venta diaria por linea de negocio, de Enero-01 a '+date_fin, height=450, bargap=0.1)
    
    return (fig2)

@app.callback(
    Output('sun_graph1_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig1 = px.sunburst(ALL_DATA_22[ALL_DATA_22['SUCURSAL']==value], path=['Mes','TIPO_PRODUCTO','LINEA_NEGOCIO'], values='TOTAL_VENTA',
                  color='TOTAL_VENTA',color_continuous_scale='tempo')
    fig1.update_traces(textinfo="label+percent parent")
    fig1.update_layout(title='Participación por tipo de producto, de Enero-01 a '+date_fin,height=450)
    return (fig1)

@app.callback(
    Output('area_graph1_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.histogram(ALL_DATA_22[ALL_DATA_22['SUCURSAL']==value], x="FECHA_ven", y="TOTAL_VENTA", color="TIPO_PRODUCTO", nbins=num)
    fig2.update_layout(title='Venta diaria por tipo de producto, de Enero-01 a '+date_fin, height=450, bargap=0.1)
    return (fig2)


@app.callback(
    Output('bar_graph1_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig3 = px.histogram(ALL_DATA_22[(ALL_DATA_22['SUCURSAL']==value)&(ALL_DATA_22['Mes']==mes)], x="LINEA_NEGOCIO", y="TOTAL_VENTA", color="TIPO_PRODUCTO", text_auto=True, nbins=num)
    fig3.update_layout(title='Venta diaria por tipo de producto, de Enero-01 a '+date_fin, height=450, bargap=0.1)
    return (fig3)


@app.callback(
    Output('line_graph2_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig1 = px.line(df3[(df3['SUCURSAL']==value)&(df3['TIPO']=='VENTA DIARIA')], x="FECHA", y="VENTA", color="SUBTEMA", facet_col='TIPO')
    fig1.update_layout(title='Comportamiento del top 20 ('+date_inicio_top+' a '+date_fin+')- ÁREAS', height=500)
    return (fig1)

@app.callback(
    Output('pie_graph2_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.pie(df3[(df3['SUCURSAL']==value)&(df3['FECHA']>=Fecha_inicio_top)&(df3['TIPO']=='VENTA DIARIA')], values='VENTA', names='SUBTEMA', title='TOP 20 de subtemas')
    fig2.update_layout(title='Participacion del top 20 ('+date_inicio_top+' a '+date_fin+')- ÁREAS', height=500)
    return (fig2)

@app.callback(
    Output('line_graph2_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig1 = px.line(df3_prov[(df3_prov['SUCURSAL']==value)&(df3_prov['TIPO']=='VENTA DIARIA')], x="FECHA", y="VENTA", color="PROVEEDOR", facet_col='TIPO')
    fig1.update_layout(title='Comportamiento del top 20 ('+date_inicio_top+' a '+date_fin+')- PROVEEDOR', height=500)
    return (fig1)

@app.callback(    
    
    Output('pie_graph2_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.pie(df3_prov[(df3_prov['SUCURSAL']==value)&(df3_prov['FECHA']>=Fecha_inicio_top)&(df3_prov['TIPO']=='VENTA DIARIA')], values='VENTA', names='PROVEEDOR')
    fig2.update_layout(title='Participacion del top 20 ('+date_inicio_top+' a '+date_fin+')- PROVEEDOR', height=500)
    return (fig2)


#####3r
@app.callback(
    Output('mapa_graph1_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.imshow(MAPAS[MAPAS['SUCURSAL']==value][['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo']]*100, text_auto=".1f", color_continuous_scale='tempo', aspect="auto")
    fig2.update_layout(title='Horarios de venta', height=450, bargap=0.1,coloraxis_showscale=False)
    
    return (fig2)

@app.callback(
    Output('mapa_graph1_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.imshow(CONSULTA[CONSULTA['SUCURSAL']==value][['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo']]*100, text_auto=".1f", color_continuous_scale='tempo', aspect="auto")
    fig2.update_layout(title='Horarios de tráfico en sitio', height=450, bargap=0.1,coloraxis_showscale=False)
    
    return (fig2)

@app.callback(
    Output('mapa_graph1_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.imshow(CARGA[CARGA['SUCURSAL']==value][['Lunes','Martes', 'MiÃ©rcoles', 'Jueves', 'Viernes', 'SÃ¡bado', 'Domingo']]*100, text_auto=".1f", color_continuous_scale='tempo', aspect="auto")
    fig2.update_layout(title='Horarios de Operación', height=450, bargap=0.1,coloraxis_showscale=False)
    
    return (fig2)
############################----------------------------
@app.callback(
    Output('mapa_graph2_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.imshow(MAPAS1[MAPAS1['SUCURSAL']==value][['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo']]*100, text_auto=".1f", color_continuous_scale='tempo', aspect="auto")
    fig2.update_layout(title='Demanda por día - Venta', height=200, bargap=0.1,coloraxis_showscale=False)
    
    return (fig2)

@app.callback(
    Output('mapa_graph2_2', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.imshow(MAPAS11[MAPAS11['SUCURSAL']==value][['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo']]*100, text_auto=".1f", color_continuous_scale='tempo', aspect="auto")
    fig2.update_layout(title='Demanda por día - Tráfico en sitio', height=200, bargap=0.1,coloraxis_showscale=False)
    return (fig2)

@app.callback(
    Output('mapa_graph2_3', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig2 = px.imshow(MAPAS111[MAPAS111['SUCURSAL']==value][['Lunes','Martes', 'MiÃ©rcoles', 'Jueves', 'Viernes', 'SÃ¡bado', 'Domingo']]*100, text_auto=".1f", color_continuous_scale='tempo', aspect="auto")
    fig2.update_layout(title='Demanda por día - Operación', height=200, bargap=0.1,coloraxis_showscale=False)
    return (fig2)

##############---------------------
##############---------------------
@app.callback(
    Output('geomapa_graph1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig = px.scatter_mapbox(LAT_LONG[LAT_LONG['SUCURSAL']==value], lat="LATITUDE", lon="LONGITUDE", hover_name="LUGAR",size='TOTAL', hover_data=['VENTA','CANTIDAD','COLONIA'],
                        color="ESTADO",color_discrete_sequence=px.colors.qualitative.G10, zoom=3.6,mapbox_style="carto-positron" ,height=500, width=1100,
                           center=dict(lat=22.6, lon=-96.25))
    return (fig)


@app.callback(    
    
    Output('table_top_1', component_property='figure'),
    [Input('items', component_property='value')])

def update_graph_pie(value):
    fig_1_df = REF[REF['SUCURSAL']==value][['ESTADO','LUGAR']].head(20)
    fig1 = go.Figure(data=[go.Table(header=dict(values=list(fig_1_df),fill_color='darkslategray',align='left',font=dict(color='white')),
                                    
        cells=dict(values=[fig_1_df.ESTADO,fig_1_df.LUGAR],line_color='darkslategray',align='left'))])    
    fig1.update_layout(autosize=True, title = "TOP 20 de destinos", height=500)
    return (fig1)


if __name__ == '__main__':
    app.run_server(debug=False)
#    app.run_server()


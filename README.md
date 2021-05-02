Herramienta para crear representación gráfica de la IA a 14 días, IA a 7 días y nuevos casos por municipios en Euskadi.


# municipios_poblacion_postal.csv

Fichero de elaboración propia con los municipios de Euskadi con Código postal y población

# download_xlsx.sh

Script que descarga de la web de https://opendata.euskadi.eus/catalogo/-/evolucion-del-coronavirus-covid-19-en-euskadi/ los xlsx que contienen las actualizaciones diarias de nuevos casos.

Se extrae la hoja 4 (3 si se cuenta desde 0) y se transforma en un CSV con nombre AÑOMESDIA.CSV

# euskadi_IA.py

Script de python que lee los csv de actualizaciones diarias de nuevos casos covid y genera 3 gráficas:

* IA14 días (calculada por acumulación de casos a 14 días / población municipio * 100000)
* IA7 días (calculada por acumulación de casos a 7 días / población municipio * 100000)
* Nuevos casos diarios

# PARA_FTP_V2

Mapas con los límites municipales de Euskadi (https://www.geo.euskadi.eus/limites-administrativos-del-pais-vasco/s69-geodir/es/)

Descargado de ftp://ftp.geo.euskadi.net/cartografia/Limites/CB_MUNICIPIOS_5000_ETRS89.zip


# Dependencias

* pandas
* pandas3
* gnumeric

* python3-geopandas
* python3-pandas

# Uso

$ python3 euskadi_IA.py AÑOMESDIA.CSV

Generará una carpeta dailymaps con las 3 imagenes mencionadas anteriormente


historic_url="https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/historico-situacion-epidemiologica.txt"
wget $historic_url -O historico_xlsx.txt
while read url; do

#url="https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/0321/29/situacion-epidemiologica.xlsx"
	day=`echo $url | awk 'BEGIN { FS = "/" } ; { print $9 }'`
	monyear=`echo $url | awk 'BEGIN { FS = "/" } ; { print $8 }'`
	month=`echo $monyear | fold -w2 | head -n1`
	year=20`echo $monyear | fold -w2 | tail -n1`

	filenamebegin=$year$month$day
	xlsxname=$filenamebegin.xlsx
	wget $url -O $xlsxname

	# Pasamos todas las hojas del xlsx a csv
	ssconvert -S $xlsxname $filenamebegin.csv

	# Sólo nos interesa la hoja 5 (IA por municipios)
	for i in `seq 0 2`
	do
		rm *.csv.$i
	done
	for i in `seq 4 8`
	do
		rm *.csv.$i
	done

	# Borrar primera línea
	sed '1d' $filenamebegin.csv.3 > tmpfile; mv tmpfile $filenamebegin.csv.3 # POSIX

	# Borrar segunda columna (Nombre municipio)
	cut --complement -f1 -d"," $filenamebegin.csv.3 > tmpfile ;  mv tmpfile $filenamebegin.csv ; rm $filenamebegin.csv.3
done <historico_xlsx.txt
rm *.xlsx

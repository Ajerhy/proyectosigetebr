#SISTEMA DE GESTION DE TERRENOS BRUNO RACUA
![Sistema de Gestion de Terrenos Bruno Racua](logo.png)
#Sigetebr
NombreView()
NombreListarView()
CrearNombreView()
NombreDetalleView()
ActualizarNombreView()


cymysql==0.9.12
Django==2.1
django-cymysql==2.1.0
Pillow==5.3.0
psycopg2==2.7.5
pytz==2018.5

COPY contrato_persona("creacion","modificacion","nombrepersona","paternopersona","maternopersona","cipersona") FROM  'C:\persona.txt' USING DELIMITERS ';'

pip freeze > requirements.txt

pip install -r requirements.txt
"""
messages.info//Azul
messages.success//Verde
messages.warning//Anaranjado
messages.error//Rojo

messages.success(request, 'Mensaje')

pip install mod-wsgi
"""
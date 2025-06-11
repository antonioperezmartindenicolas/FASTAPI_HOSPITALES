import mysql.connector 
database = mysql.connector.connect( # LLAMAMOS AL FUNCION CONNECT PARA CONECTARNOS
    host ='localhost',
    port = 3307,
    ssl_disabled = True,
    user ='root', #USUARIO QUE USAMOS NOSOTROS
    password ='antonio', #CONTRASEÑA CON LA QUE NOS CONECTAMOS
    database='hospitales'
) 
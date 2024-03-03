# srodriguev-st0263
topicos telematica - sara rodriguez

# info de la materia: ST0263 <Topicos Especiales de Telematica>
#
# Estudiante(s): Sara Rodriguez Velasquez , srodriguev@eafit.edu.co
#
# Profesor: Alvaro Ospina, aospina@eafit.edu.co
#
# RETOS 01 Y 02
#
# 1. breve descripción de la actividad
#
En esta actividad se realizó la base de un sistema peer to peer con un servidor central que funciona como directorio.

El pServer.py actúa como un nodo servidor que almacena y gestiona los archivos compartidos.
El pClient.py es el cliente que interactúa con el servidor para subir, descargar y listar archivos.
El pPeer.py es el script que representa un nodo de la red peer-to-peer.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se cumplió con la meta de tener un sistema peer 2 peer que intercambie archivos, que por ahora son archivos simbolicos a modo de cadenas de texto. 
Estas se actualizan en una carpeta local que funciona como base de datos sencilla.

Se pueden bajar y subir archivos txt y sus contenidos.

Se puede visualizar que hay en que peer o en el servidor por medio de metodos auxiliares.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

No se configuró la asignación de un peer como suplente de otro en caso de falla, en ese caso el peer que hizo la consulta puede pedirle al servidor principal que elimine el peer inalcanzable y nada mas.

No se usa una base de datos para tener mayor consistencia con los datos.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Arquitectura:
La arquitectura general sigue un modelo cliente-servidor, donde el servidor actúa como el punto central para la gestión de archivos compartidos y los clientes realizan operaciones de carga, descarga y listado de archivos.

Aunque se tiene un sistema donde el intercambio se da entre los nodos existe un servidor principal que funciona como directorio.

Patrones:
Se utiliza el patrón de diseño de Servicio (Service Pattern) para definir y gestionar las operaciones que pueden ser realizadas por los clientes en el servidor. Esto se ve reflejado en la definición de métodos como Upload, Download y ListFiles en el servidor.

También se emplea el patrón Cliente-Servidor, donde el cliente envía solicitudes al servidor y este responde con la información requerida

Mejores prácticas utilizadas:
Uso de gRPC para la comunicación entre cliente y servidor, lo que proporciona una forma eficiente y confiable de definir y gestionar servicios distribuidos.

Separación de responsabilidades entre cliente y servidor, lo que facilita el mantenimiento y la escalabilidad del sistema.

Utilización de configuraciones externas (por ejemplo, archivos .ini) para almacenar información de configuración, lo que hace que el sistema sea más flexible y configurable.


# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Lenguaje de programación: Python
Versión de Python: Python 3.10.9

Librerías y paquetes:
* gRPC: Se utiliza para la comunicación entre clientes y servidores en el sistema P2P.
* grpcio: La implementación de gRPC para Python.
* grpcio-tools: Herramientas para la generación de código gRPC en Python.
* configparser: Utilizado para leer archivos de configuración INI.
* os: Para operaciones relacionadas con el sistema operativo, como la manipulación de rutas de archivos.
* requests: Para realizar solicitudes HTTP a través del protocolo REST API.
* concurrent.futures: Para ejecutar operaciones de manera asíncrona.
* grpc-reflection: Para habilitar la reflexión del servicio gRPC.

## como se compila y ejecuta.

```command line

python3 server.py
python3 pServer.py
python3 pClient.py
```


## detalles del desarrollo.

Se fue escalando la usabilidad, comenazando por los servicios REST Api y ya luego se crearon los metodos con gRPC. Por ultimo se hicieron mejoras para cumplir con los requisitos y proporcionar mayor robustez.

## detalles técnicos




## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

Los parametros de ejecucion como puerto, direccion ip y folders de archivos se configuran en el peerConfig.init

```command line

nano peerConfig.ini
```



## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)



## opcionalmente - si quiere mostrar resultados o pantallazos 



# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

Los parametros se configuran dentro del archivo config.

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

Primero debe instalar las librerias. 

```command line

pip install grpcio grpcio-tools configparser requests grpcio-reflection

```

Luego correr el server principal

```command line

python3 server.py

```

Luego, recomendablemente en sus propias carpetas, por orden, correr los dos servicios de los peer.

```command line

python3 pServer.py & python3 pClient.py

```

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## (https://www.linkedin.com/pulse/implementing-peer-to-peer-data-exchange-inpython-luis-soares-m-sc-/) - Luis Soarez. Implementing Peer-to-Peer Data Exchange in Python
## (https://grpc.io/docs/languages/go/basics/) - Tutoriales de gRPC
## (https://grpc.io/docs/languages/python/basics/) - Tutoriales de gRPC
## (https://www.ramonmillan.com/libros/librodistribucionlibrosredesp2p/distribucionlibrosredesp2p_caracteristicasp2p.php) - caracteristicas de redes p2p
## (https://www.tutorialspoint.com/flask/index.htm) - Tutorial de Flask
## (https://www.redsauce.net/blog/es/postman-quick-guide) - Guia rapida de Postman


# flask

## ¡Hola, mundo!
```sh
mkdir microblog && cd microblog
python3 -m venv venv
source venv/bin/activate
```
Intalación de Flask

    pip install flask

Comprobar la instalación de Flask

    import flask

Crear un paquete `app` para albergar la aplicación:

    mkdir app

`app/__init__.py`: el script crear el objeto de la aplicación como una instancia de la clase
`Flask` importado del paquete flask. La variable `__name__` pasada a la clase `Flask` es una
variable predefinida de Python, que se establece en el nombre del módulo en el que se utiliza.
Flask usa la ubicación del módulo pasado aquí como punto de partida cuando necesita cargar
recursos asociados, como archivos de plantilla. A todos los efectos practicos, pasando
`__name__` casi siempre va a configurar Flask de la manera correcta. A continuación, la
aplicación importa el módulo `routes`, que aún no existe.

Otra peculiaridad es que el módulo `routes` se importa en la parte inferior y no en la parte
superior del script como siempre se hace. La importación inferior es una solución para las
importaciones circulares, un problema común con las aplicaciones de Flask. Vas a ver que
el módulo `routes` necesita importar la variable `app` definida en este script, por lo que
colocar una de las importaciones en la parte superior evita el error que resulta de las
referencias mutuas entre dos archivos.

Entonces, ¿qué pasa en el módulo `routes`? Las rutas son las diferentes URLs que implementa la
aplicación. En Flask, los controladores para las rutas de la aplicación se escriben como
funciones de python, denominadas *funciones de visualización*. Las funciones de vista se
asignan a una o más URls de ruta para que Flask sepa qué lógica ejecutar cuando un cliente
solicita una URL determinada.

`app/routes.py`: es la primera función de vista para esta aplicación.

Esta función de vista es bastante simple, solo devuelve un saludo como una cadena.
`@app.route` las dos líneas extrañas de arriba de la función son decoradores, una
característica única de Python. Los decoradores modifican la función que le sigue. Un
patrón común con los decoradores es usarlos para registrar funciones como devoluciones de
llamada para ciertos eventos. En este caso, el decorador `@app.routes` crea una
asociación entre la URL dada como argumento y la función. En este ejemplo hay dos decoradores
, que asocian las URL `/` y `/index` a esta función. Esto significa que cuando el navegador
solicite cualquiera de las dos URL, Flask invocará esta función y devolverá el valor
devuelto al navegador como respuesta.

Para completa la aplicación, debe tener una secuenia de comandos dePython en el nivel
superior que defina la instancia de la aplicación Flask. `microblog.py`: con una sola línea
que importa la instancia de la aplicación.

La instancia de la aplicación Flask se llama `app` y es miembro del paquete `app`. La
declaración `from app import app` importa la variable `app` que es miembro del paquete `app`.

Se debe indicar a Flas cómo importarlo, configurando la variable ambiental:

    export FLASK_APP=microblog.py

Para ejecitarlo:

    flask run --host=0.0.0.0

`localhost:5000/` y `localhost:5000/index`: La primera URL se asigna a `/`, mientras que el
segundo corresponde a `/index`. Ambas rutas están asociadas con una única función de vista
en la aplicación, por lo que producen el mismo resultado, que es la cadena que devuelve
la función. Si ingresa cualquier otra URL, obtendrá un error, ya que la aplicación
solo reconoce estas dos URL.

Dado que las variable no se recuerdan en las sesiones de terminal, puede que resulte
tedioso tener que configurar siempre la variable de entorno `FLASK_APP` en cada
nueva terminal. A partir de la versión `1.0`, Flask le permite registrar las variables
de entorno que desea que se importen automáticamente cuando ejecute el dominio `flask`.
Para usar esta opción, debe instalar el módulo `python-dotnenv`:

    pip install python-dotenv

Luego, puede escribir el nombre y el valor de la variable de entorno en un archivo
llamado `.flaskenv` ubicado en el directorio de nivel superior del proyecto.

## Templates
¿Qué son las plantillas?
Quiero que la página de inico de mi aplicació tenga un encabezado que de la bienvenida
al usuario. Por el momento voy a ingorar el hecho de que la aplicación aún no tiene
el concepto de usuarios (más adelante). En su lugar, usaré un usuario simulado, que
implementaré como un diccionario de Python, de la siguiente manera:
```py
print()
```

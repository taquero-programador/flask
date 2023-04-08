# Flask

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
#### ¿Qué son las plantillas?
Quiero que la página de inico de mi aplicación tenga un encabezado que de la bienvenida
al usuario. Por el momento voy a ingorar el hecho de que la aplicación aún no tiene
el concepto de usuarios (más adelante). En su lugar, usaré un usuario simulado, que
implementaré como un diccionario de Python, de la siguiente manera:
```py
user = {'username': 'Miguel'}
```
La creación de objetos simulados es una técnica útil que le permite concentrarse en
una parte de la aplicación sin tener que preocuparse por otras partes del sistema que
aún no existe.

La función de vista en la aplicación devuelve una cadena simple. Lo que quiero hacer
ahora es expandir esa cadena devuelta en una página HTML completa, tal vez algo
como esto -> `app/routes.py`.

Las plantillas ayudan a logar esta separación entre la presentación y la lógica
comercial. En Flask, las plantillas se escriben como archivos separados, amancenados
en una carpeta de plantillas que se encuentra dentro del paquete de la aplicación.
Entonces, cree el directorio donde se almacenarán las plantillas:

    mkdir app/templates

`app/templates/index.html`

Esta es una página HTML es su mayoría estándar, muy simple. Lo único interesante de
esta página es que hay un par de marcadores de posición para el contenido dinámico,
encerrados en secciones `{{ .. }}`. Estos marcadores de posición representan las
partes de la página que son variable y solo se conocerán en tiempo de ejecución.

Ahora que la presentación de la página se descargó en la plantila HTML, la función
de vista de puede simplificar -> `app/routes.py`.

La operación que convierte una plantilla es una página HTML completa se denomina
representación. Para renderizar la plantilla, tuve que importar una función que viene
con Flask llamada `render_template()`. Esta función toma un nombre de archivo de plantilla
y una lista variable de argumentos de plantilla y devuelve la misma plnatilla, pero
con todos los marcadores de posición reemplazado por valores reales.

La función `render_template()` invoca el motor de plantillas Jinga2 que viene incluido
con Flask. Jinga2 sustituyo `{{ .. }}` con los valores correspondientes, dado por los
argumentos proporcionados al llamar a `render_template()`.

#### Declaraciones condicionales
Ha visto cómo Jinga2 reemplza los marcadores de posición con valores reales durante
el renderizado, pero esta es solo una de las muchas operaciones poderosas que admite
Jinga2 en los archivos de plantilla. Por ejemplo, las plantillas también adminte
sentencias de control, dadas dentro de bloques `{% ... %}`. Agregar una declaración
condicional -> `app/templates/index.html`.

Ahora la plantilla es un poco más inteligente. Si la función de vista se olvida de pasar
un valor para la variable `title` de marcador de posición, en lugar de mostrar un título
vacío, la plantilla proporcionará uno predeterinado. Puede probar cómo funciona esta
condicional eliminando el argumento `title` en la llamada de la función 
`render_template()`. Aplica para el título en la pestaña del navegador.

#### Bucles
El usuario conetado probablemente querrá ver las publicaciones recientes de los
usuarios conectados en la página de inicio.

Crear algunos usarios falsos en `/app/routes.py`.

Para representar las publicaciones de los usuarios, estoy usando una lista, donde cada
elemento es un diccionario que tiene los campos `autho` y `body`.

Por el lado de la plantilla tengo que resolver un nuevo problema. La lista de
publicaciones puede tener cualaquier cantidad de elementos, depende de la función de
vista decidir cuántas publicaciones se presentarán en la página. La plantilla no puede
hacer supociones sobre cuántas publicaciones hay, por lo que debe estar preparada
para representar tantas publicaciones como la vista envíe de forma genérica.

Para este tipo de problemas, Jinga2 ofrece una estructura de control `for`
-> `app/templates/index.html`.

#### Herencia de plantillas
La mayoría de las aplicaciones web en estos días tienen una barra de navegación en la
parte superior de la página con algunos enlaces de uso frecuente, como un enlace para   editar un su perfil, iniciar sesióm, cerrar, sesión, etc. Puede agregar fácilmente
una barra de navegación a la plantilla `index.html` con algo más de HTML, pero a medida
que la aplicación cerza, necesitará esta misma barra de navegación en otras páginas.

Jinga2 tiene una función de herencia de plantillas. En escencia, lo que puede hacer es
mover las partes del diseño de página que son comunes a todas las plantillas a una
plnatilla base, de la cual se derivan todas las demás plantillas.

Definir una plantilla base llamada `base.html` que incluya una barra de navegación simple
y también la lógica de título implemantado anteriormente. plantilla base en
`app/templates.base.html`.

`block` declaración de control para definir el lugar donde las plantillas derivadas
pueden insertarse. Los bloques reciben un nombre único, al que las plantillas derivadas
pueden hacer referencia cuando proporcionan su contenido.

Con la plantilla base en su lugar, ahora puede simplificar `index.html` haciéndolo
heredar de `base.html`. Modificar `app/templates/index.html`.

Dado que la plantilla `base.html` ahora se encargará de la esctructura general de la
página, quite todos los elementos de `index.html` y dejé solo la parte del contenido.
La declaración `extends` establece el vínculo de herencia dentre las dos plantillas,
de modo que Jinga2 sabe que cuando se le pide que renderice `index.html` necesita
incrustarlo dentro de `base.html`. Las dos plantillas tienen la declaración
`block` con nombre `content`, así es como Jinga2 sabe combinar las dos plantillas en
una sola. Ahora, si necesita crear páginas adicionaes para la aplicación, puede
crearlas como plantillas derivadas de la misma plantilla `base.html`, y así es como
puede hacer que todas las páginas de la aplicación compartan la misma apariencia sin
duplicación.

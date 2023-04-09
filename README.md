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
, que asocian las URL `/` e `/index` a esta función. Esto significa que cuando el navegador
solicite cualquiera de las dos URL, Flask invocará esta función y devolverá el valor
devuelto al navegador como respuesta.

Para completa la aplicación, debe tener una secuenia de comandos de Python en el nivel
superior que defina la instancia de la aplicación Flask. `microblog.py`: con una sola línea
que importa la instancia de la aplicación.

La instancia de la aplicación Flask se llama `app` y es miembro del paquete `app`. La
declaración `from app import app` importa la variable `app` que es miembro del paquete `app`.

Se debe indicar a Flask cómo importarlo, configurando la variable ambiental:

    export FLASK_APP=microblog.py

Para ejecutarlo:

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
Para usar esta opción, debe instalar el módulo `python-dotenv`:

    pip install python-dotenv

Luego, puede escribir el nombre y el valor de la variable de entorno en un archivo
llamado `.flaskenv` ubicado en el directorio de nivel superior del proyecto.

## Templates
#### ¿Qué son las plantillas?
Quiero que la página de inicio de mi aplicación tenga un encabezado que de la bienvenida
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
comercial. En Flask, las plantillas se escriben como archivos separados, almancenados
en una carpeta de plantillas que se encuentra dentro del paquete de la aplicación.
Entonces, cree el directorio donde se almacenarán las plantillas:

    mkdir app/templates

`app/templates/index.html`

Esta es una página HTML en su mayoría estándar, muy simple. Lo único interesante de
esta página es que hay un par de marcadores de posición para el contenido dinámico,
encerrados en secciones `{{ .. }}`. Estos marcadores de posición representan las
partes de la página que son variable y solo se conocerán en tiempo de ejecución.

Ahora que la presentación de la página se descargó en la plantila HTML, la función
de vista se puede simplificar -> `app/routes.py`.

La operación que convierte una plantilla es una página HTML completa se denomina
representación. Para renderizar la plantilla, tuve que importar una función que viene
con Flask llamada `render_template()`. Esta función toma un nombre de archivo de plantilla
y una lista variable de argumentos de plantilla y devuelve la misma plantilla, pero
con todos los marcadores de posición reemplazado por valores reales.

La función `render_template()` invoca el motor de plantillas Jinga2 que viene incluido
con Flask. Jinga2 sustituyo `{{ .. }}` con los valores correspondientes, dado por los
argumentos proporcionados al llamar a `render_template()`.

#### Declaraciones condicionales
Ha visto cómo Jinga2 reemplaza los marcadores de posición con valores reales durante
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
El usuario conectado probablemente querrá ver las publicaciones recientes de los
usuarios conectados en la página de inicio.

Crear algunos usuarios falsos en `/app/routes.py`.

Para representar las publicaciones de los usuarios, estoy usando una lista, donde cada
elemento es un diccionario que tiene los campos `author` y `body`.

Por el lado de la plantilla tengo que resolver un nuevo problema. La lista de
publicaciones puede tener cualquier cantidad de elementos, depende de la función de
vista decidir cuántas publicaciones se presentarán en la página. La plantilla no puede
hacer supociones sobre cuántas publicaciones hay, por lo que debe estar preparada
para representar tantas publicaciones como la vista envíe de forma genérica.

Para este tipo de problemas, Jinga2 ofrece una estructura de control `for`
-> `app/templates/index.html`.

#### Herencia de plantillas
La mayoría de las aplicaciones web en estos días tienen una barra de navegación en la
parte superior de la página con algunos enlaces de uso frecuente, como un enlace para
editar un su perfil, iniciar sesión, cerrar, sesión, etc. Puede agregar fácilmente
una barra de navegación a la plantilla `index.html` con algo más de HTML, pero a medida
que la aplicación crezca, necesitará esta misma barra de navegación en otras páginas.

Jinga2 tiene una función de herencia de plantillas. En escencia, lo que puede hacer es
mover las partes del diseño de página que son comunes a todas las plantillas a una
plnatilla base, de la cual se derivan todas las demás plantillas.

Definir una plantilla base llamada `base.html` que incluya una barra de navegación simple
y también la lógica de título implemantado anteriormente. Plantilla base en
`app/templates/base.html`.

`block` declaración de control para definir el lugar donde las plantillas derivadas
pueden insertarse. Los bloques reciben un nombre único, al que las plantillas derivadas
pueden hacer referencia cuando proporcionan su contenido.

Con la plantilla base en su lugar, ahora puede simplificar `index.html` haciéndolo
heredar de `base.html`. Modificar `app/templates/index.html`.

Dado que la plantilla `base.html` ahora se encargará de la estructura general de la
página, quite todos los elementos de `index.html` y dejé solo la parte del contenido.
La declaración `extends` establece el vínculo de herencia entre las dos plantillas,
de modo que Jinga2 sabe que cuando se le pide que renderice `index.html` necesita
incrustarlo dentro de `base.html`. Las dos plantillas tienen la declaración
`block` con nombre `content`, así es como Jinga2 sabe combinar las dos plantillas en
una sola. Ahora, si necesita crear páginas adicionaes para la aplicación, puede
crearlas como plantillas derivadas de la misma plantilla `base.html`, y así es como
puede hacer que todas las páginas de la aplicación compartan la misma apariencia sin
duplicación.

## Web forms
#### Introducción a Flask-WTF
Para manejar los formularios web en esta aplicación, voy a usar la extensión Flask-WTF,
que es un envoltorio delgado alrededor del paquete WTForms que se integra muy bien
con Flask.

Las extensiones de Flask son módulos regulares de Python que se instalar con `pip`.

    pip install flask-wtf

Hay varios formatos para que la aplicación especifique las operaciones de configuración.
La solución más básica es definir sus variables como claves en `app.conf`, que
utiliza un estilo de diccionario para trabajar con variables.

Para mantener las cosas bien organizadas, voy a crear una clase de configuración
en un módulo de Python separado. A continuación puede ver la nueva clase de
configuración para esta aplicación, almacenada en un módulo `config.py` en el directorio
de nivel superior: `config.py`.

La variable `SECRET_KEY` de configuración que agregué como el único elemento de
configuración es una parte importante en la mayoría de las aplicaciones Flask.
Flask y algunas de sus extensiones utilizan el valor de la clave secreta como clave
criptográfica, útil para generar firmas y token. La extensión Flask-WTF lo usa para
proteger formularios web contra un ataque desagradable llamado Cross-Site Request
Forgery o CSRF. Como su nombre lo indica, se supone que la clave secreta es secreta,
ya que ninguna persona fuera de los mantenedores de confianza de la aplicación lo
sepan.

El valor de la clave secreta se establece como una expresión con dos términos,
unidos por el operador `or`. El primer término busca el valor de una variable de
entorno llamada `SECRET_KEY`. El segundo término es solo una cadena codificada.
Este es un patrón que se podra repetir para las variables de configuración. La
idea es que se prefiera un valor procedente de una variable de entorno, pero si
el entorno no define la variable, entonces se utiliza la cadena codificada de
forma predeterminada. Cuando está desarrollando esta aplicación, los requisitos de
seguiridad son bajos, por lo que puede ignorar esta configuración y dejar que se use
la cadena codificada, configuraré un valor único y difícil de adivinar en el entorno,
de modo que el servidor tenga una clave segura que nadie más conozca.

Ahora que tengo un archivo de configuración, necesito decirle a Flask que lo lea y
lo aplique. Eso se puede hacer justo después de crear la instancia de la aplicación
Flask usando el método `app.config.from_objet()`: `app/__init__.py`.

Se puede acceder a los elementos de configuración con una sintaxis de diccionario
desde `app.config`:
```py
from microblog import app
app.config['SECRET_KEY']
```
Una vez más, teniendo en cuenta la separación de preocupaciones, voy a usar un nuevo
módulo `app/forms.py` para almacenar mis clases de formularios web. Para comenzar,
definamos un formulario de inicio de sesión de usuario, que le pide al usuario que
ingrese un nombre de usuario y una contraseña. El formulario también incluirá una
casilla de verificación "recordarme" y un botón de envío: `app/forms.py`.

La mayoría de las extensiones de Flask usan una convención de nomeclatura `flask_<name>`
para su símbolo de importación de nivel superior. En este caso, Flask-WTF
tiene todos sus símbolos bajo `flask_wtf`. Aquí es donde la clase base `FlaskForm` se
importa desde la parte superior de `app/forms.py`.

Las cuatro clases que representan los tipos de campo que estoy usando para este
formulario se importan directamente del paquete WTForms, ya que la extenisón
Flask-WTF no proporciona versiones personalizadas. Para cada campo, se crea un
objeto como una variable de clase en la clase `LoginForm`. Cada campo recibe una
descripción o etiqueta como primer argumento.

El argumento `validators` que ve en algunos de los campos se usa para adjuntar
comportamientos de validación a los campos. El validador `DataRequired` simplemente
verifica que el campo no se envíe vacío. Hay muchos más validadores disponibles.

#### Plantillas de formulario
El siguiente paso es agregar el formulario a una plantilla HTML para que se pueda
representar en una página web. La buena noticia es que los campos que están
definidos en la clase `LoginForm` saben cómo representarse a sí mismos como HTML,
por lo que esta tarea es bastante simple. A continuación puede ver la plantilla de
inicio de sesión, se almacenará en `app/templates/login.html`.

Para esta plantilla se está reautilizando la plantilla `base.html`, a través de la
declaración `extends` de herencia de plantilla.

Esta plantilla espera un objeto de formulario instanciado desde la clase `LoginForm`
que se dará como un argumento, que puede ver referenciado como `form`. Este
argumento será enviado por la función de vista de inicio de sesión, que aún no
se ha escrito.

El elemento HTML `<form>` se utiliza como contenedor para el formulario web. El
atributo `action` del formulario se usa para decirle al navegador la URL que debe usarse
al enviar la información que el usuario ingresó en el formulario. Cuando la
acción se establece en una cadena vacía, el formulario se envía a la URL que se
encuentra actualmente en la barra de direcciones, que es la URL que represento el
formulario de la página. El atributo `method` especifica el método de solicitud HTTP
que debe usarse al enviar el formulario al servidor. El valor predeterminado es
enviarlo como una solicitud `GET`, pero en casi todos los casos, utilizando una
solicitud `POST` mejora la experiencia del usuario porque las solicitudes de este
tipo pueden enviar los datos del formulario en el cuerpo de la solicitud, mientras
que `GET` agregar los campos de los formularios en la URL, saturando la barra de
direcciones del navegador. El atributo `novalidate` se usa para decirle al navegador
que web que no que no aplique la validación a los campos de este formulario, lo
que deja esta tarea a la aplicación Flask que se ejecuta en el servidor. Usando
`novalidate` es completamente opcional, pero para este primer formulario es
importane que lo establezca porque le permitirá probar la validación del lado del
servidor.

El argumento `form.hidden_tag()` de plantilla genera un campo oculto que incluye
un token que se usa para proteger el formulario contra ataques CSFR. Todo lo que
necesita hacer para proteger el formulario es incluir este campo oculto y tener
el `SECRET_KEY` definida en la configuración de Flask. Si te encargas de estas dos
cosas, Flask-WTF hace el resto por ti.

Si ha escrito formularios web HTML en el pasado, es posible que le haya resultado
extraño que no haya campo HTML en la plantilla. Esto se debe a que los campos del
objeto de formulario saben cómo monstrarse como HTML. Todo lo que tenía que hacer
era incluir `{{ form.<field_name>.label }}` donde quería la etiqueta de campo, y
`{{ form.<field_name()> }}` donde quería el campo. Para los campos que requieren
atributos HTML adicionales, se puede pasar como argumentos. Los campos de usuario
y contrseña en esta plantilla `size` como un argumento que se añadirá al elemento
HTML `<input>` como atributo. Así es como también pueden adjuntar clases CSS o Id
a campos de formulario.

#### Vista de formulario
El paso final antes de que pueda ver este formulario en el navegador es codificar
una nueva función de vista en la aplicación que repesente la plantilla de la
sección anterior.

Nueva función de vista asignada a la URL de inicio de sesión que crea un formulario
y lo pasa a la plantilla para su procesamiento. Esta función de visualización
también puede ir en el módulo `app/routes.py`.

Lo que hice aquí es importar la clase `LoginForm` de `forms.py`, creó una instancia de
un objeto y lo envío a la plantilla. `form=form` la sintaxis puede parecer extraña,
pero simplemente está pasando el objeto `form` creado en la línea de arriba a la
plantilla con el nombre `form`.

Para facilitar el acceso al formulario de inicio de sesión, la plantilla base
puede incluir un enlace en la barra de navegación: `app/templates/base.html`.

En este punto, puede ejecutar la aplicación y ver el formulario en su navegador.
Con la aplicación en ejecución, escriba `localhost:/5000/` en la barra de direcciones
y luego haga clic en Inicar sesión para ver el nuevo formulario.

#### Recepción de datos de formulario
Si intenta presionar el botón Enviar, el navegador monstrará un error de "Método
no permitido". Esto se debe a que la función de vista de inicio de sesión de la
sección anterior hace la mitad del trabajo hasta ahora. Puede mostrar el formulario
en una página web, pero aún no tiene la lógia para procesar los datos enviados por
el usuario. Esta es otra área en la que Flask-WTF hace que el trabajo sea realmente
fácil. Aquí hay una versión actualizada de la función de vista que acepta y valida
los datos enviados por el usuario -> `app/routes.py`.

la primera novedad de esta versión es el argumento `methods` en el decoradore de rutas.
Esto le dice a Flask que esta función de vista acepta solicitudes `GET` y `POST`,
anulando el valor predeterminado, que es solo aceptar peticiones `GET`. El protocolo
HTTP que las peticiones `GET` son aquellas que devuelven información al cliente.
Todas las solicitudes en la aplicación hasta el momento son de este tipo. Las
solicitudes `POST` se utilizan normalmente cuando el navegador envía datos de formulario
al servidor. El error "Metodo no permitido" que el navegador mostró antes,
aparece porque el navegador intentó enviar una solicitud `POST` y la aplicación
no estaba configurada para aceptarla. El proporcionar el argumento `methods`, le
está diciendo a Flask qué métodos de solicitud debe aceptar.

El método `form.validate_on_submit()` hace todo el trabajo de procesamiento de
formularios. Cuando el navegador envía la solicitud `GET` para recibir la página web
con el formulario, este método va a devolver `False`, por lo que en ese caso la
función omite la instrucción `if` y va directamente a representar la plantilla en
la última línea de la función.

Cuando el navegador envía la solicitud `POST` como resultado de que el usuario
presione el botón enviar, `form.validate_on_submit()` va a recopilar todos los datos,
ejecutará todas las validaciones adjuntos a los campos y, si todo está bien,
retornará `True`, indicando que los datos son válidos y pueden ser tratados por la
aplicación. Pero si al menos un campo falla en la validación, la función devolverá
`False`, y eso hará que el formulario se devuelva al usuario, como en el caso de la
solicitud `GET`.

Cuando `form.validate_on_submit()` devuelve `True`, la función de vista de inicio de
sesión llama a dos funciones nuevas, importadas de Flask. La función `flash()` es
una forma útil de monstrar un mensaje al usuario. Muchas aplicaciones utilizan esta
técnica para informar al usuario se alguna acción ha tenido éxito o no. En este
caso, voy a usar este mecanismo como una solución temporal, por ahora monstrara un
mensaje que confirme que la aplicación recibió las credenciales.

`redirect()` esta función le indica al navegador web del cliente que vaya
automáticamente a una página diferentes, pasada como argumento. Esta función de
visualización la utiliza para redirigir al usuario a la página de `index` de la
aplicación.

Cuando llamas a la función `flash()`, Flask almacena el mensaje, pero los mensajes
flasheados no aparecerán mágicamente en las páginas web. Las plantillas de la
aplicación deben representar estos mensaje flasheados de una manera que funcione
para el diseño del sitio. Voy a agregar estos mensajes a la plantilla base, para que
todas las plantillas hereden esta funcionalidad -> `app/templates/base.html`.

Aquí estoy usando un constructor `with` para asignar el resultado de llamar a 
`get_flashed_messages()` a una variable `messages`, todo en el contexto de la
plantilla. La función `get_flashed_messages()` proviene de Flask y devuelve una lista
de todos los mensajes que se han registrado previamente con `flash()`. La condición
comprueba si `messages` tiene algún contendo. y en ese caso, un elemento <ul>
representara cada mensaje como un elemento de la lista <li>.

Una propiedad interesante de estos mensajes flasheados es que una vez que se
solicitan una vez a través de la función `get_flashed_messages()` se eliminan de
la lista de mensajes, por lo que aparecen solo una vez después de llamar a la
función `flash()`.

#### Mejorar la validación de campos
Los validadores que se adjuntar a los campos del formulario evitan que se acepten
datos no válidos en la aplicación. La forma en que la aplicación trata con la
entrada del formulario no váliada es volviendo a mostrar el formulario, para
permitir que el usuario haga las corecciones necesarias.

Si intentó enviar datps no válidos, estoy seguro de que notó que, si bien los
macanismo de validación funcionan bien. no hay ninguna indicación para el usuario
de que algo anda mal con el formulario, el usuario simplemente recupera el
formulario. La siguiente tarea es mejorar la experiencia del usuario agragando un
mensaje de error significativo junto a cada campo que falló en la validación.

De hecho, los validadores de formularios ya generan estos mensajes de error
descriptivo, por lo que todo lo que falta es alguna lógica adicional en la
plantilla para representarlos.

Plantilla de inicio de sesión con mensajes de validación de campo agregados en los
campos de nombre de usuario y contraseña -> `app/templates/login.html`.

El único cambio que he hecho es agregar bucles `for` justo después de los campos de
nombre de usuario y contraseña que representan los mensajes de error agregados
por los validadores de color rojo. Como regla general, cualquier campo que tenga
validadores adjuntos tendrá mensajes de error que resulten de la validación
agregada en `form.<field_name>.errors`. Esta va a ser una lista, porque los campos
pueden tener varios validadores adjuntos y más de uno puede proporcionar mensajes
de error para mostrar al usuario.

Si intenta enviar el formulario con un nombre de usuario y contrsela vacíos,
recibirá un mensaje de error en rojo.

#### Generando enlaces
El formulario de inicio de sesión está bastante completo ahora, pero antes de cerrar
este capítulo quería discutir la forma correcta de incluir enlaces en plantillas
y redireccionamiento.

Un problema con la escritura de enlaces directamente en plantillas y archivos
fuente es que si un día decide reorganizar sus enlaces, tendrá que buscar y
reemplazar estos enlaces en toda su aplicación.

Para tener un mejor control sobre estos enlaces, Flask proporciona una función
llamada `url_for()`, que genera direcciones URL usando un mapeo interno de direcciones
URL para ver funciones. Por ejemplo, la expresión `url_for('login')` devolverá
`/login` y `url_for('index')` devolverá `/index`. El argumento `url_for()` es el nombre
del punto final, que es el nombre de la función de vista.

Puede preguntar por qué es mejor usar los nombres de las funciones en lugar de las
URL. El hecho es que es mucho más probale que cambien las URL que ver los nombres
de las funciones, que son completamente internos. Una razón secundaria es que,
como aprenderá más adelante, algunas URL tienen componentes dinámicos, por lo que
generar esas URL a mano requeriría concaterna varios elementos, lo cual es tedioso
y propenso a errores. El `url_for()` también puede generar estas URL complejas.

Así que de ahora en adelante, voy a usar `url_for()` cada vez que necesite generar
una URL de aplicación -> `app/templates/base.html` y actualizar la función
`login()` -> `app/routes.py`.

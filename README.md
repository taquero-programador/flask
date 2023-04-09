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

## Databases
Flask no admite bases de datos de forma nativa. Pero tiene la libartad de elegir la
base de datos que mejor se adapte a su aplicación en lugar de verse obligado a
adaptarse a una.

Hay excelentes opciones para bases de datos en Python, muchas de ellas con
extensiones de Flask que hacen una mejor integración con la aplicación. Las bases
de datos se pueden separar en dos grandes grupos, las que siguen el modelo
relaciona y las que no. El último modelo a menuso se denomina NoSQL, lo que indica
que no implementa el popular lenguaje de consultas SQL. Si bien existen
excelentes productos de bases de daots en ambos grupos, las bases de dato
relacionales son una mejor combinación para las aplicaciones que tiene datos
estructurados, como listas de usuarios, pubicaciones de blog, etc., mientras que
las bases de datos NoSQL tienden a ser mejores para los datos que tienen una
estructura menos definida. Esta aplicación, como la mayoría de las demás, se puede
implementar utilizando cualquier tipo de base de datos.

Flask-SQLAlchemy es una extensión que proporciona un contenedor compatible con Flask
para el popular paquete SQLAlchemy, que es un mapaeador relacional de objetos u ORM.
Los ORM permiten que las aplicaciones administren una base de datos utilizando
entidades de alto nivel como clases, objetos y métodos en lugar de tablas y SQL.
El trabajo del ORM es traducir las operaciones de alto nivel en comandos de base de
datos.

Lo bueno de SQLAlchemy es que es un ORM no para una, sino para muchas base de
datos relaciones. SQLAlchemy admite una larga lista de motores de base de datos,
inlcuidos los populares MySQL, PostgreSQL y SQLite. Esto es extremadamente
poderoso, porque puede hacer su desarrollo utilizando una base da datos SQLite
simple que no requiere un servidor. y luego, cuando llegue el momento de
implementar la aplicación de un servidor de producción, puede elegir un servidor
MySQL o PostgreSQL más robusto, sin tener que cambiar su aplicación.

Instalar SQLAlchemy:

    pip install flask-sqlalchemy

#### Migraciones de bases de datos
Esto es difícil porque las bases de datos relacionales se centran en datos
estructurados, por lo que cuando la estructura cambia, los datos que ya están en
la base de datos deben migrarse para la estructura modificada.

Flask-Migrate es un contenedor de Flask para Alembic, un marco de migración de
base de datos para SQLAlchemy. TRabajar con Migraciones de base de datos agrega
un poco de trabajo para iniciar una base de datos, pero es un pequeño precio a
pagar por una form sólida de realiza cambios en su base de datos en el futuro.

Instalar Flask-Migrate:

    pip install flask-migrate

#### Configuración de Flask-SQLAlchemy
Las bases de datos SQLite son la opción más conveniente para el desarrollar
aplicaiones pequeñas, a veces incluso no tan pequeñas, ya que cada base de datos
se almacena en un solo archivo en el disco y no es necesario ejecutar un servidor
de base de datos.

Agregar dos nuevos elementos de configuración al archivo -> `config.py`.

La extensión Flask-SQLAlchemy toma la ubicación de la base de datos de la
aplicación de la variable `SQLALCHEMY_DATABASE_URI`. En este caso, estoy tomando
la URL de la base de datos de la variable de entorno `DATABSE_URL`, y si no está
definido, estoy configurando una base de datos llamada `app.db` ubicada en el
directorio principal de la aplicación, que se almacena en la variable `basedir`.

La opción de configuración `SQLALCHEMY_TRACK_MODIFICATIONS` está establecida en
`False` para deshabilitar una función de Flask-SQLAlchemy que no necesito, que es
enviar una señal a la aplicación cada vez que se va a relizar un cambio en la
base de datos.

La base de datos va estar representada en la aplicación por la instancia de la
base de datos. El motor de migración de base de datos también tendrá una
instancia. Estos son objetos que deben crearse después de la aplicación,
en el archivo -> `app/__init__.py`.

He realizado tres cambios en el script de `app/__init__.py`. Primero, he añadido
un objeto `db` que representa la base de datos. Luego he agregado otro objeto que
representa el motor de migración. Con surte, verá un patrón sobre como trabajar
con las extensiones de Flask. La mayoría de las extensiones se inicializan como
estas dos. Finalmente, Estoy importando un nuevo módulo llamado `models` en el
fondo. Este módulo definirá la estructura de la base de datos.

#### Modelos de base de datos
Los datos que se almacenarán en la base de datos estarán representado por una
colección de clases, generalmente denominadas *modelos de base de datos*. La capa
ORM dentro de SQLAlchemy hará las traducciones necesarias para asignar objetos
creados a partir de estas clases en filas en las tablas de base de datos
adecuadas.

Comencemos por crear un modelo que represente a los usuarios:

![users](pics/tusers.png)

El campo `id` suele estar en todos los modelos y se utiliza como clave principal.
A cada usuario de la base de dato se le asignará un valor de identifiación único,
almacenado en este campo. Las claves primarias, en la mayoría de los casos, son
asignadas automáticamente por la base de datos, por lo que solo necesito
proporcionar el campo `id` marcado como clave primaria.

Los campos `username`, `email` y `password_hash` se definen como cadenas (`VARCHAR`), y
sus longitudes máximas se especifican para que la base de datos pueda optimizar
el uso del espacio. Mientras que los campos `username` y `email` se explican por sí
mismos, el campo `password_hash` merece algo de atención. Quiero asegurame de
que la aplicación que estoy creando adopte las mejores prácticas de seguridad y,
por ese motivo, no almacenaré las contraseñas de los usuarios en la base de datos.
El problema con el almacenamiento de contraseñas es que si la base de datos
alguna vez se ve comprometida, los atacantes tendrán acceso a las contraseña y
eso podría ser devastador para los usuarios. En lugar de escribir las contraseñas
directamente, voy a escribir un hash de contraseña, lo que mejora enormemente la
seguirdad.

Entonces, ahora que sé lo que quiero para mi tabla de usuarios, puedo traducirlo en
código en el nuevo módulo -> `app/models.py`.

La clase `User` hereda de `db.Model`, una clase base para todos los modelos de
Flask.SQLAlchemy. Esta clase define varios campos como variable de clase. Los
campos se crean como instancias de la clase `db.Column`, que toma como argumento
el tipo de campo, más otros campos opcionales que, por ejemplo, permiten indeicar
qué campos son únicos e indexados, lo cual es importante para que las búsquedas
en la base de datos sea eficiente.

El método `__repr__` le dice a Python cómo imprimir objetos de la clase, lo que sera
útil para la depuración, ejemplo:
```py
from app.models import User
u = User(username='susan', email='susan@example.com')
u
```

#### Creación del repositorio de migración
La clase de modelo creado en la sección anterior define la estructura de la base
de datos inicial (*schema*) para esta aplicación. Pero a medida que la aplicación
continúa creciendo, es probable que deba realizar cambios en esa estructura,
como agregar cosas nuevas y, a veces, modificar o eiminar elementos. Alembic
realizará estos cambios de esquema de una manera que no requiera que la base de
datos se vuelva a crear desde cero cada vez que se deba realizar un cambio.

Para logar esta tarea aparentemente fácil, Alembic mantiene un repositorio de
migración, que es un directorio en el que almacena sus scripts de migración. Cada
vez que se reliza un cambio en el esquema de la base de datos, se agrega un script
de migración al repositorio con los detalles de los cambios. Para aplicar las
migraciones a una base de datos, estos scripts de migración se ejecutan en la
secuencia en que se crearon.

Flask-Migrate expone sus comandos a través del dominio `flask`. `flask db` Flask-Migrate
agrega un subcomando para administrar todo lo relacioando con las migraciones de
base de datos. Crear el repositorio de migración para microblog:

    flask db init

Después de ejecutar este comando, encontrará un nuevo directorio de migraciones,
con algunos archivos y un subdirectorio de versiones dentro. Todos estos archivos
deben tratarse como parte de su proyecto a partir de ahora y, en particular, deben
agregarse al control de código de fuente junto con el código de la aplicación.

#### La primera migración de base de datos
Con el repositorio de migración en su lugar, es hora de crear la primera migración
de base de datos, que incluirá la tabla de usuarios que se asigna al modelo
`User` de la base de datos. Hay dos formas de crear una migración de base de datos:
manual o automáticamente. Para generar una migración automáticamente, Alembic
compara el esquema de la base de datos definido por los modelos de la base de datos
real que se usa actualmente en la base de datos. Luego, completa el script de
migración con los cambios necesarios para que el esquema de la base de datos
coincida con los modelos de la aplicación. En este caso, dado que no existe una
base de datos anterior, la migración automática agregará todo el modelo `User`
al script de migración. El subcomando `flask db migrate` genera estas migraciones
automáticas:

    flask db migrate -m "users table"

La salida del comando le da una idea de lo que Alembic incluyó en la migración. Las
dos primeras líneas son informativas y, por lo general, se pueden ignorar. Luego
dice que ecnotró una tabla de usuarios y dos índices. Luego te dice dónde escribió
el script de migración. El código `e517276bb1c2` es un código único generado
automáticamente para la migración. El comentario dado con la opción `-m` es opcional,
agrega un breve texto descriptivo a la migración.

El script de migración generado ahora es parte de su proyecto y debe incorporase
al control de código. La función `upgrade()` aplica la migración y la función
`downgrade()`. Esto le permite a Alembic migrar la base de datos a cualquier punto
del historial, incluso a versiones anteriores, utilizando la ruta de degreadación.

El coamndo `flask db migrate` no reliza ningún cambio en la base de datos, solo genera
el script de migración. Para aplicar los cambios a la base de datos, debe usar el
comando `flask db upgrade`:

    flask db upgrade

Debido a que esta aplicación una SQLite, el comando `upgrade` detectará que una base
de datos no existe y la creará (`app.db`). Cuando trabaje con sevidores de base de
datos, como MySQL y PostgreSQL, debe crear la base de datos en el servidor
antes de ejecutar `upgrade`.

Tenga en cuenta que Flask-SQLAlchemy usa una convención de nomeclatura "snake case"
para las tablas de la base de datos de forma predeterminada. Para el modelo
anterior `User`, la tabla correspondiente en la base de datos se llamará `user`.
Para la clase de modelo `AdreesAndPhone`, la tabla se llamaría `address_and_phone`.
Si prefiere elegir sus propios nombre de tablas, puede agregar un atributo llamado
`__tablename__` a la clase de modelo, establezca el nombre desea como una cadena.

#### Flujo de trabajo de actualización y degradación de la base de datos
La aplicación está en su infancia en este momento. Imagine que tiene su aplicación
en su máquina de desarrollo y también tiene una copia implementada en su servidor
de producción que está en línea y en uso.

Digamos que para la próxima versión de su aplicación debe introducir un cambio
en sus modelos, por ejemplo, se debe agregar una nueva tabla. Sin migraciones,
necesitaría descrubir cómo cambiar el esquema de su base de datos, tanto en su
máquina de desarrollo como en su servidor, y esto podría ser mucho trabajo.

Pero con el soporte de migración de base de datos, después de modificar los
modelos en su aplicación, genera un nuevo script de migración (`flask db migrate`),
probablemente lo revise para asegurarse de que la generación automática hizo lo
correcto y luego aplique los cambios a su base de datos de desarrollo
(`flask db upgrade`). Agregará el script de migración al control de código de
fuente y lo confirmará.

Cuando esté listo para lanzar la nueva versión de la aplicación a su servidor de
producción, todo lo que necesita hacer es obtener la versión actualizada de au
aplicación, que incluirá el nuevo script de migración y ejecutar `flask db upgrade`.
Alembic, detectará que la base de datos de producción no está actualizada a la
última revisión del esquema y ejecutará todos los nuevos scripts de la migración
que se crearon después de la versión anterior.

También tiene un comando `flask db downgrade`, que deshace la última migración. Si
bien es poco probable que necesite esta opción en su sistema de producción, puede
resultare muy úitl durante el desarrollo. Es posible que haya generado un script
de migración y lo haya aplicado, solo para descubrir que los cambios que
realizó no son exactamente lo que necesita. En este caso, puede degradar la base
de datos, eliminar el script de migración y luego generar uno nuevo para
reemplazarlo.

#### Las bases de datos
Las bases de datos relacionales son buenas para almacenar relaciones entre
elementos de datos. Considere el caso de un usuario que escribe una publicación
de blog. El usuario tendrá un registro de la tabla `users`, y la publicación
tendrá un registro en la tabla `posts`. La forma más eficiente de registrar quién
escribió una publicación determinada es vincular los dos registros relacionados.

Una vez que establece un vinculo entre un usuario y una publicación, la base de
datos puede responder consultas sobre este vínculo. El más trivial es cuando
tienes una publicación de un blog y necesitar saber qué usuario lo escribió.
Una consulta más compleja es la inversa de esta. Si tiene un usuario, es posible
que desee concer todas las publicaciones que este usuario escribió. Flask-SQLAlchemy
ayudará con ambos tipos de consultas.

Expandamos la base de datos para almacenar publicaciones de blog y ver las
relaciones en acción. Esquema para una nueva tabla `posts`:

![posts](pics/tposts.png)

La tabla `posts` tendrá el `id` requerido, un campo `body` y un `timestamp`. Pero además
de estos campos separados, tendrá un campo `user_id`, que vincula la publicación
con su autor. Todos los usuarios tienen una clave `id` princila que es única. La
forma de vincular una publicación de blog con el usuario que lo creó es agregar
una referencia al `id`, eso es exactamente lo que el campo `user_id` es. Este campo
`user_id` se llava clave foránea. El diagrama de las bases de datos anterior
muestra las claves foráneas como un enlace entre el campo y el campo `id` de la
tabla que se refiere. Este tipo de ralación se llama uno a muchos, porque "un"
usuario escribe muchas "publicaciones". Modificar -> `app/models.py`.

La nueva clase `Post` representará publicaciones de blog escritas por usuarios. El
campo `timestamp` se indexará, lo cual es útl si desea recuperar publicaciones en
order cronológico. También he añadido un argumento `default`, y pasó la función
`datetime.utcnow`. Cuando pasa una función como predeterminada, SQLAlchemy
establecerá el campo en el valor al llamar a esa función. En general querrá
trabajar con fechas y horas UTC en una aplicación de servidor. Esto garantiza que
está utilizando marcas de tiempo uniforme independientemente de dónde se encuentren
los usuarios. Estas marcas de timpo se convertirán a la hora local del usuario
cuando se muestren.

El campo `user_id` se inicializó como una clave externa para `user.id`, lo que
significa que hace referencia a un valor `id` de la tabla de usuarios. En esta
referencia el campo `user` es el nombre de la tabla de la base de datos para el
modelo. Es una desafortunada inconsistencia que en algunos casos, como en una
llamada a `db.relationship()`, el modelo es referenciado por la clase del model, que
normalmente comienza con un carácter en mayúscula, mienstras que en otros casos
como esta declaración `db.ForeignKey()`, un modelo viene dado por su nombre de tabla
de base de datos, para el cual SQLAlchemy usa automáticamente caracteres en minúsculas
y, para nombres de modelos de varias palabras, mayúscula y minúsculas.

La clase `User` tiene un nuevo campo `posts`, que se inicializa con `db.relationship`.
Este no es un campo de base de datos real, sino una bista de alto nivel de la
relación entre usuarios y las publicaciones, y por esa razón no está en el
diagrama de la base de datos. Para una relación de uno a muchos `db.relationship`.
El campo normalmente se define en el lado "uno" y se usa como una forma
conveniente de obtener acceso a los "muchos". Entonces, por ejemplo, si tengo
tengo un usuario almacenado en `u`, la expresión `u.posts` ejecutará una consulta
de base de datos que devuelve todas la publicaciones escritar por ese usuario. El
primer argumento `db.relationship` es la clase modelo que representa el lado "varios"
de la relación. Este argumento se puede proporcionar como una cadena con el nombre
de la clase si el modelo se define más adelante en el módulo. El argumento
`backref` define el nombre de un campo que se agregará a los objetos de la clase
"varios" que apunta al objeto "uno". Esto agregará una expresión `post.author` que
devolverá al usuario una publicación dada. El agumento `lazy` define cómo se emitirá
la consulta de la base de datos para la relación.

Dado que tengo actualizaciones de los modelos de la aplicación, es necesario
generar una nueva migración de la base de datos:

    flask db migrate -m "posts table"

Y aplicar la migración a la base de datos:

    flask db upgrade

#### Jugando con la base de datos
Dado que la aplicación aún no tiene ninguna lógica de base de datos, juguemos con
la base de datos en el intérprete de Python para familiarizarnos con ella.
```py
from app import app, db
from app.models import User, Post
```
Para que Flask y sus extensiones tengan acceso a la aplicación Flask sin tener que
que pasar `app` como argumento en cada función, un contexto de aplicación se debe
crear y enviar.
```py
app.app_context().push()
```
A continuación, cree un nuevo usuario:
```py
u = User(username='john', email='john@example.com')
db.session.add(u)
db.session.commit()
```
Los cambios en una base de datos se realizan en el contexto de una sesión de base
de datos, a la que se puede acceder como `db.session`. Se pueden acumular múltiples
cambios en una sesión y una vez registrados todos los cambios se puede emitir un
solo `db.session.commit()`, que escribe todos los cambios. Si en cualquier momento
mientras se trabaja en una sesión hay un error, una llamada a `db.session.rollback()`
cancelará la sesión y eliminará los cambios almacenado en ella. Lo importante a
recordar es que los cambios solo se escriben en la base de datos cuando se emite
una confirmación con `db.session.commit()`. Las sesiones garantizan que la base de
datos nunca quedará en un estado inconsistente.

El contexto de la aplicación que se envió anteriormente permite que Flask-SQLAlchemy
acceda a la instancia de la aplicación Flask `app` sin tener que recibirlo como un
argumento. La extensión busca en el diccionario `app.config` la entrada
`SQLALCHEMY_DATABASE_URI`, que contiene la URL de la base de datos.

Agregar otro usuario:
```py
u = User(username='susan', email='susan@example.com')
db.session.add(u)
db.session.commit()
```
La base de datos puede responder una consulta que devuelve todos los usuarios:
```py
users = User.query.all()
users
...
for u in users:
    print(u.id, u.username)
```
Todos los modelos tienen un atributo `query` que es el punto de entrada para ejecutar
consultas de base de datos. la consulta más básica es aquella que devuelve todos los
elementos de esa clase, que se denomina `all()`. Tenga en cuenta que los campos `id`
se establecieron automáticamente en `1` y `2` cuando se agregaron los usuarios.

Aquí hay otra forma de hacer consultas. Si conoces el `id` de un usuario, puede
recuperarse ese usuario usando lo siguiente:
```py
u = User.query.get(1)
# or
print(User.query.get(1))
```
Ahora agregar una publicación de blog:
```py
u = User.query.get(1)
p = Post(body='test post', author=u)
db.session.add(p)
db.session.commit()
```
No necesita establecer un valor para `timestamp` porque ese campo tiene un valor
predeterminado, que puede ver en la definición del modelo. ¿Y qué paso con el campo
`user_id`? Recuerda el `db.relationship` que creé en la clase `User` agregando un
atributo `posts` a los usuarios, y también un atributo `author` a las publicaciones.
Asigno un autor a una publicación usando el campo virtual `author` en lugar de tener
que lidiar con el ID de usuario. SQLAlchemy es excelente en ese sentido, ya que
proporciona una abstracción de alto nivel sobre las relaciones y las claves externas.

Algunas consultas a la base de datos:
```py
u = user.query.get(1)
u
...
posts = u.posts.all()
posts
...

# usuario sin posts
u = User.query.get(2)
u
...
u.posts.all()
...

# print post author and body for all posts
for p in Post.query.all():
    print(p.id, p.author.username, p.body)

# get all users in reverse order
User,qyer.order_by(User.username.desc()).all()
```
Borrar los registros de la tabla `User` y `Post`:
```py
for u in User.query.all():
    db.sessiopn.delete(u)

for p in Post.query.all():
    db.session.delete(p)

# confirmar
db.session.commit()
```

#### Contexto de shell
```py
from app import app, db
from app.models import User, Post
app.app_context().push()
```
Mientras trabaja con su aplicación, necesitara probar cosas en una shell de Python
con mucha frecuencia, por lo que tener que repetir las declaraciones anteriores
cada vez se volcerá tedioso. 

El commando `flask shell` es otra herramienta muy útil en `flask`. El comando `shel` es
el segundo comando "básico" implementado por Flask, después de `run`. El
propósito de este comando es iniciar un interprete de Python en el contexto de la
aplicación. Ejemplo:
```py
python
>>> app
# error

flask shell
>>> app
print(User.query.all()) # works fine!
```
Con una sesión regular, el símbolo `ap` no se conoce a menos que se import explícitamente,
pero cuando se usa `flask shell`, el comando import previamente la instancia de la
aplicación, lo bueno de `flask shell` no es solo que preimporta `app`, sino también
puede configurar un "contexto de shell".

La siguiente función en `microblog.py` crea un contexto de shell que agrega la
instancia de la base de datos y los modelos a la sesión de shell.

Si se obtiene error al acceder a `db`, `User` y `Post`, es probable que se deba a que
no se a registrado la variable de entorno `FLASK_APP=microblog.py`. Se resuelve añadiendo
la variable en una archivo `.flaskenv` o con `export FLASK_APP=microblog.py`.

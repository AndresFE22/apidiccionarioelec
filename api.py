from flask import Flask, jsonify, request, Response
import mysql.connector
from flask_cors import CORS
import base64
import imghdr
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'mi_clave_secreta'

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)

app.json_encoder = CustomJSONEncoder


db = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$default"
)

if db.is_connected():
    print("La conexión a la base de datos se estableció correctamente")
else:
    print("La conexión a la base de datos no se pudo establecer")

@app.route('/')
def inicio():
    return 'servidor escuchando'

@app.route('/api/comunas/<comuna>/palabras', methods=['GET'])
def obtener_palabras(comuna):
    db = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$default"
)
    cursor = db.cursor()
    query = "SELECT palabras FROM palabras"

    if comuna.lower() == 'monteria':
        query = "SELECT DISTINCT palabras FROM palabras"
        cursor.execute(query)
    else:
        query = "SELECT palabras FROM palabras WHERE comuna = %s"
        cursor.execute(query, (comuna,))

    palabras = [row[0] for row in cursor.fetchall()]  # Convertir a lista
    cursor.close()
    print(palabras)
    return jsonify(palabras)

@app.route('/api/palabras', methods=['POST'])
def guardar_palabras():
    db = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$default")

    data = request.json
    termino = data.get('nuevoTermino')
    comunas = data.get('comunasSeleccionadas')
    print(termino, comunas)
    if comunas and isinstance(comunas, list):
        cursor = db.cursor()

        for comuna in comunas:
            insert_query = "INSERT INTO palabras (palabras, comuna) VALUES (%s, %s)"
            values = (termino, comuna)
            cursor.execute(insert_query, values)

        db.commit()
        cursor.close()

        return jsonify({'message': 'Palabras agregadas correctamente'})

    return jsonify({'error': 'No se proporcionaron comunas seleccionadas'}), 400


@app.route('/api/terminos', methods=['GET'])
def obtener_terminos():
    db = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$default"
)
    cursor = db.cursor()
    query = "SELECT * FROM palabras"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    # Crear un diccionario anidado para almacenar los términos y sus comunas asociadas
    terminos_dict = {}

    for row in rows:
        palabra = row[2]
        comuna = row[1]

        # Si el término ya existe en el diccionario, agregar la comuna a la lista de comunas
        if palabra in terminos_dict:
            terminos_dict[palabra].append(comuna)
        else:
            # Si el término no existe en el diccionario, crear una nueva entrada con la comuna en una lista
            terminos_dict[palabra] = [comuna]

    return jsonify(terminos_dict)

@app.route('/api/palabras/editar', methods=['POST'])
def editar_palabras():
    db = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$default"
)
    data = request.json
    termino = data.get('palabraEditada')
    comunas = data.get('comunasSeleccionadas')
    print(termino, comunas)
    if comunas and isinstance(comunas, list):
        cursor = db.cursor()

        for comuna in comunas:
            insert_query = "INSERT INTO palabras (palabras, comuna) VALUES (%s, %s)"
            values = (termino, comuna)
            cursor.execute(insert_query, values)

        db.commit()
        cursor.close()

        return jsonify({'message': 'Palabras editada correctamente'})

    return jsonify({'error': 'No se proporcionaron comunas seleccionadas'}), 400

@app.route('/api/palabras/eliminar', methods=['POST'])
def eliminar_palabras():
    db = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$default"
)
    data = request.json
    termino = data.get('palabraEditada')
    comunas = data.get('comunasSeleccionadas')
    print(termino, comunas)

    if termino and comunas and isinstance(comunas, list):
        cursor = db.cursor()

        for comuna in comunas:
            delete_query = "DELETE FROM palabras WHERE palabras = %s AND comuna = %s"
            values = (termino, comuna)
            cursor.execute(delete_query, values)

        db.commit()
        cursor.close()

        return jsonify({'message': 'Palabras eliminadas correctamente'})

    return jsonify({'error': 'No se proporcionaron datos válidos'}), 400













    #RUTAS PARA EL DICCIONARIO KOGUI
bd = mysql.connector.connect (

    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$kogui"
)

if bd.is_connected():
    print("La conexión a la base de datos se estableció correctamente")
else:
    print("La conexión a la base de datos no se pudo establecer")


# Rutas para guardar informacion
@app.route('/apik/guardarpalabras', methods=['POST'])
def crear_palabra():
    palabra = request.form.get('palabra')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(palabra, significado, imagen)

    cursor = bd.cursor()
    query = "INSERT INTO palabras (palabra, significado, imagen) VALUES (%s, %s, %s)"
    values = (palabra, significado, imagendata)
    cursor.execute(query, values)
    bd.commit()
    cursor.close()


    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})

@app.route('/apik/guardarinfo', methods=['POST'])
def crear_info():
    informacion = request.form.get('informacion')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(informacion, significado, imagen)
    bd.reconnect()
    cursor = bd.cursor()
    query = "INSERT INTO informacion (informacion, significado, imagen) VALUES (%s, %s, %s)"
    values = (informacion, significado, imagendata)
    cursor.execute(query, values)
    bd.commit()
    cursor.close()


    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})

@app.route('/apik/guardaroracion', methods=['POST'])
def crear_oracion():
    oracion = request.form.get('oracion')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(oracion, significado, imagen)

    bd.reconnect()
    cursor = bd.cursor()
    query = "INSERT INTO oraciones (oracion, significado, imagen) VALUES (%s, %s, %s)"
    values = (oracion, significado, imagendata)
    cursor.execute(query, values)
    bd.commit()
    cursor.close()


    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})



# Ruta para enviar la informacion
@app.route('/apik/palabras', methods=['GET'])
def obtenerPalabras():
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT palabra, significado, imagen FROM palabras"
    cursor.execute(query)
    palabras = cursor.fetchall()
    cursor.close()
    resultado = []
    for palabra, significado, imagen in palabras:
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        formato_imagen = imghdr.what(None, imagen)
        resultado.append({ 'palabra': palabra, 'significado': significado, 'imagen': imagen_base64, 'formato': formato_imagen})
    print(resultado)
    response = jsonify(resultado)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    return response

@app.route('/apik/oraciones', methods=['GET'])
def obtenerOraciones():
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT oracion, significado, imagen FROM oraciones"
    cursor.execute(query)
    oraciones = cursor.fetchall()
    cursor.close()
    resultado = []
    for oracion, significado, imagen in oraciones:
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        formato_imagen = imghdr.what(None, imagen)
        resultado.append({ 'oracion': oracion, 'significado': significado, 'imagen': imagen_base64, 'formato': formato_imagen})
    print(resultado)
    response = jsonify(resultado)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    return response

@app.route('/apik/info', methods=['GET'])
def obtenerInformacion():
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT informacion, significado, imagen FROM informacion"
    cursor.execute(query)
    informacion = cursor.fetchall()
    cursor.close()
    resultado = []
    for info, significado, imagen in informacion:
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        formato_imagen = imghdr.what(None, imagen)
        resultado.append({ 'info': info, 'significado': significado, 'imagen': imagen_base64, 'formato': formato_imagen})
    print(resultado)
    response = jsonify(resultado)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    return response


#Rutas para editar la informacion

#imprimirpalabras
@app.route('/apik/showtable', methods=['GET'])
def showpalabras():
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT id, palabra, significado FROM palabras"
    cursor.execute(query)
    palabras = cursor.fetchall()
    cursor.close()
    print(palabras)
    json_data = json.dumps(palabras, cls=CustomJSONEncoder)
    response = Response(json_data, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    print(response)
    return response

if __name__ == '__main__':
    app.run(port=8080)

#eliminar palabras
@app.route('/apik/palabras/<int:id>', methods=['DELETE'])
def eliminar_palabra(id):
    bd.reconnect()
    cursor = bd.cursor()
    query = "DELETE FROM palabras WHERE id = %s"
    cursor.execute(query, (id,))
    bd.commit()
    cursor.close()

    return jsonify({'message': 'Palabra eliminada correctamente'})

#editar palabras
@app.route('/apik/palabras/<int:id>', methods=['PUT'])
def editar_palabra(id):

    nueva_palabra = request.json.get('palabra')
    nuevo_significado = request.json.get('significado')
    print(nueva_palabra, nuevo_significado)

    bd.reconnect()
    cursor = bd.cursor()
    query = "UPDATE palabras SET palabra = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_palabra, nuevo_significado, id,))
    bd.commit()
    cursor.close()

    return jsonify({'message': 'Palabra editada correctamente'})

#mandar imagen de palabras
@app.route('/apik/palabras/<int:id>/image', methods=['GET'])
def imagen_palabras(id):
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT imagen FROM palabras WHERE id = %s"
    cursor.execute(query, (id,))
    imagen = cursor.fetchone()[0]
    cursor.close()
    imagen_base64 = base64.b64encode(imagen).decode('utf-8')
    formato_imagen = imghdr.what(None, imagen)
    response = jsonify({
        'imagen_base64': imagen_base64,
        'formato_imagen': formato_imagen
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#imprimiroraciones
@app.route('/apik/showtableo', methods=['GET'])
def showoraciones():
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT id, oracion, significado FROM oraciones"
    cursor.execute(query)
    oraciones = cursor.fetchall()
    cursor.close()
    print(oraciones)
    json_data = json.dumps(oraciones, cls=CustomJSONEncoder)
    response = Response(json_data, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    print(response)
    return response

if __name__ == '__main__':
    app.run(port=8080)

#eliminar oraciones
@app.route('/apik/oraciones/<int:id>', methods=['DELETE'])
def eliminar_oracion(id):
    bd.reconnect()
    cursor = bd.cursor()
    query = "DELETE FROM oraciones WHERE id = %s"
    cursor.execute(query, (id,))
    bd.commit()
    cursor.close()

    return jsonify({'message': 'oracion eliminada correctamente'})

#editar oraciones
@app.route('/apik/oraciones/<int:id>', methods=['PUT'])
def editar_oracion(id):

    nueva_oracion = request.json.get('oracion')
    nuevo_significado = request.json.get('significado')
    print(nueva_oracion, nuevo_significado)

    bd.reconnect()
    cursor = bd.cursor()
    query = "UPDATE oraciones SET oracion = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_oracion, nuevo_significado, id,))
    bd.commit()
    cursor.close()

    return jsonify({'message': 'oracion editada correctamente'})

#mandar imagen de oraciones
@app.route('/apik/oraciones/<int:id>/image', methods=['GET'])
def imagen_oracion(id):
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT imagen FROM oraciones WHERE id = %s"
    cursor.execute(query, (id,))
    imagen = cursor.fetchone()[0]
    cursor.close()
    imagen_base64 = base64.b64encode(imagen).decode('utf-8')
    formato_imagen = imghdr.what(None, imagen)
    response = jsonify({
        'imagen_base64': imagen_base64,
        'formato_imagen': formato_imagen
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#imprimir informacion
@app.route('/apik/showtablei', methods=['GET'])
def showoinfo():
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT id, informacion, significado FROM informacion"
    cursor.execute(query)
    informacion = cursor.fetchall()
    cursor.close()
    print(informacion)
    json_data = json.dumps(informacion, cls=CustomJSONEncoder)
    response = Response(json_data, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    print(response)
    return response

if __name__ == '__main__':
    app.run(port=8080)

#eliminar informacion
@app.route('/apik/info/<int:id>', methods=['DELETE'])
def eliminar_informacion(id):
    bd.reconnect()
    cursor = bd.cursor()
    query = "DELETE FROM informacion WHERE id = %s"
    cursor.execute(query, (id,))
    bd.commit()
    cursor.close()

    return jsonify({'message': 'información eliminada correctamente'})

#editar oraciones
@app.route('/apik/info/<int:id>', methods=['PUT'])
def editar_informacion(id):

    nueva_info = request.json.get('informacion')
    nuevo_significado = request.json.get('significado')
    print(nueva_info, nuevo_significado)

    bd.reconnect()
    cursor = bd.cursor()
    query = "UPDATE informacion SET informacion = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_info, nuevo_significado, id,))
    bd.commit()
    cursor.close()

    return jsonify({'message': 'información editada correctamente'})

#mandar imagen de oraciones
@app.route('/apik/info/<int:id>/image', methods=['GET'])
def imagen_informacion(id):
    bd.reconnect()
    cursor = bd.cursor()
    query = "SELECT imagen FROM informacion WHERE id = %s"
    cursor.execute(query, (id,))
    imagen = cursor.fetchone()[0]
    cursor.close()
    imagen_base64 = base64.b64encode(imagen).decode('utf-8')
    formato_imagen = imghdr.what(None, imagen)
    response = jsonify({
        'imagen_base64': imagen_base64,
        'formato_imagen': formato_imagen
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response












#RUTAS DICCIONARIO ELECTRONICO

from flask import Flask, jsonify, request, session, render_template, Response
from flask_cors import CORS
import mysql.connector
import base64
import imghdr
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'mi_clave_secreta'

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

c = mysql.connector.connect (
    host="cuentaapi.mysql.pythonanywhere-services.com",
    user="cuentaapi",
    password="Andres22*",
    database="cuentaapi$electronico"
)

if c.is_connected():
    print("La conexión a la base de datos se estableció correctamente")
else:
    print("La conexión a la base de datos no se pudo establecer")



# Rutas para guardar informacion
@app.route('/apie/guardarpalabras', methods=['POST'])
def crear_palabrae():
    palabra = request.form.get('palabra')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(palabra, significado, imagen)

    cursor = c.cursor()
    query = "INSERT INTO palabras (palabras, significado, imagen) VALUES (%s, %s, %s)"
    values = (palabra, significado, imagendata)
    cursor.execute(query, values)
    c.commit()
    cursor.close()


    return jsonify({'message': 'palabra creada exitosamente'})

@app.route('/apie/guardarfrase', methods=['POST'])
def crear_frase():
    frase = request.form.get('frases')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(frase, significado, imagen)
    c.reconnect()
    cursor = c.cursor()
    query = "INSERT INTO frases (frases, significado, imagen) VALUES (%s, %s, %s)"
    values = (frase, significado, imagendata)
    cursor.execute(query, values)
    c.commit()
    cursor.close()


    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})

@app.route('/apie/guardarrefran', methods=['POST'])
def crear_refran():
    refran = request.form.get('refran')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(refran, significado, imagen)

    c.reconnect()
    cursor = c.cursor()
    query = "INSERT INTO refranes (refranes, significado, imagen) VALUES (%s, %s, %s)"
    values = (refran, significado, imagendata)
    cursor.execute(query, values)
    c.commit()
    cursor.close()


    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})



# Ruta para enviar la informacion
@app.route('/apie/palabras', methods=['GET'])
def obtenerPalabrase():
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT palabras, significado, imagen FROM palabras"
    cursor.execute(query)
    palabras = cursor.fetchall()
    cursor.close()
    resultado = []
    for palabra, significado, imagen in palabras:
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        formato_imagen = imghdr.what(None, imagen)
        resultado.append({ 'palabra': palabra, 'significado': significado, 'imagen': imagen_base64, 'formato': formato_imagen})
    print(resultado)
    response = jsonify(resultado)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    return response

@app.route('/apie/refranes', methods=['GET'])
def obtenerrefranes():
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT refranes, significado, imagen FROM refranes"
    cursor.execute(query)
    refranes = cursor.fetchall()
    cursor.close()
    resultado = []
    for refran, significado, imagen in refranes:
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        formato_imagen = imghdr.what(None, imagen)
        resultado.append({ 'refran': refran, 'significado': significado, 'imagen': imagen_base64, 'formato': formato_imagen})
    print(resultado)
    response = jsonify(resultado)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    return response

@app.route('/apie/frases', methods=['GET'])
def obtenerFrases():
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT frases, significado, imagen FROM frases"
    cursor.execute(query)
    frases = cursor.fetchall()
    cursor.close()
    resultado = []
    for frase, significado, imagen in frases:
        imagen_base64 = base64.b64encode(imagen).decode('utf-8')
        formato_imagen = imghdr.what(None, imagen)
        resultado.append({ 'frase': frase, 'significado': significado, 'imagen': imagen_base64, 'formato': formato_imagen})
    print(resultado)
    response = jsonify(resultado)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    return response


#Rutas para editar la informacion

#imprimirpalabras
@app.route('/apie/showtable', methods=['GET'])
def showpalabrase():
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT id, palabras, significado FROM palabras"
    cursor.execute(query)
    palabras = cursor.fetchall()
    cursor.close()
    print(palabras)
    json_data = json.dumps(palabras, cls=CustomJSONEncoder)
    response = Response(json_data, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    print(response)
    return response

if __name__ == '__main__':
    app.run(port=8080)

#eliminar palabras
@app.route('/apie/palabras/<int:id>', methods=['DELETE'])
def eliminar_palabrae(id):
    c.reconnect()
    cursor = c.cursor()
    query = "DELETE FROM palabras WHERE id = %s"
    cursor.execute(query, (id,))
    c.commit()
    cursor.close()

    return jsonify({'message': 'Palabra eliminada correctamente'})

#editar palabras
@app.route('/apie/palabras/<int:id>', methods=['PUT'])
def editar_palabrae(id):

    nueva_palabra = request.json.get('palabra')
    nuevo_significado = request.json.get('significado')
    print(nueva_palabra, nuevo_significado)

    c.reconnect()
    cursor = c.cursor()
    query = "UPDATE palabras SET palabras = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_palabra, nuevo_significado, id,))
    c.commit()
    cursor.close()

    return jsonify({'message': 'Palabra editada correctamente'})

#mandar imagen de palabras
@app.route('/apie/palabras/<int:id>/image', methods=['GET'])
def imagen_palabrase(id):
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT imagen FROM palabras WHERE id = %s"
    cursor.execute(query, (id,))
    imagen = cursor.fetchone()[0]
    cursor.close()
    imagen_base64 = base64.b64encode(imagen).decode('utf-8')
    formato_imagen = imghdr.what(None, imagen)
    response = jsonify({
        'imagen_base64': imagen_base64,
        'formato_imagen': formato_imagen
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#imprimirrefranes
@app.route('/apie/showtabler', methods=['GET'])
def showorefranes():
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT id, refranes, significado FROM refranes"
    cursor.execute(query)
    refranes = cursor.fetchall()
    cursor.close()
    print(refranes)
    json_data = json.dumps(refranes, cls=CustomJSONEncoder)
    response = Response(json_data, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    print(response)
    return response

if __name__ == '__main__':
    app.run(port=8080)

#eliminar refranes
@app.route('/apie/refranes/<int:id>', methods=['DELETE'])
def eliminar_refran(id):
    c.reconnect()
    cursor = c.cursor()
    query = "DELETE FROM refranes WHERE id = %s"
    cursor.execute(query, (id,))
    c.commit()
    cursor.close()

    return jsonify({'message': 'refran eliminado correctamente'})

#editar refranes
@app.route('/apie/refranes/<int:id>', methods=['PUT'])
def editar_refran(id):

    nuevo_refran = request.json.get('oracion')
    nuevo_significado = request.json.get('significado')
    print(nuevo_refran, nuevo_significado)

    c.reconnect()
    cursor = c.cursor()
    query = "UPDATE refranes SET refranes = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nuevo_refran, nuevo_significado, id,))
    c.commit()
    cursor.close()

    return jsonify({'message': 'refran editado correctamente'})

#mandar imagen de refran
@app.route('/apie/refranes/<int:id>/image', methods=['GET'])
def imagen_refran(id):
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT imagen FROM refranes WHERE id = %s"
    cursor.execute(query, (id,))
    imagen = cursor.fetchone()[0]
    cursor.close()
    imagen_base64 = base64.b64encode(imagen).decode('utf-8')
    formato_imagen = imghdr.what(None, imagen)
    response = jsonify({
        'imagen_base64': imagen_base64,
        'formato_imagen': formato_imagen
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#imprimir frases
@app.route('/apie/showtablef', methods=['GET'])
def showofrases():
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT id, frases, significado FROM frases"
    cursor.execute(query)
    frases = cursor.fetchall()
    cursor.close()
    print(frases)
    json_data = json.dumps(frases, cls=CustomJSONEncoder)
    response = Response(json_data, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Agregar el encabezado
    print(response)
    return response

if __name__ == '__main__':
    app.run(port=8080)

#eliminar frases
@app.route('/apie/frases/<int:id>', methods=['DELETE'])
def eliminar_frases(id):
    c.reconnect()
    cursor = c.cursor()
    query = "DELETE FROM frases WHERE id = %s"
    cursor.execute(query, (id,))
    c.commit()
    cursor.close()

    return jsonify({'message': 'frase eliminada correctamente'})

#editar frase
@app.route('/apie/frases/<int:id>', methods=['PUT'])
def editar_frase(id):

    nueva_frase = request.json.get('frase')
    nuevo_significado = request.json.get('significado')
    print(nueva_frase, nuevo_significado)

    c.reconnect()
    cursor = c.cursor()
    query = "UPDATE frases SET frases = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_frase, nuevo_significado, id,))
    c.commit()
    cursor.close()

    return jsonify({'message': 'frase editada correctamente'})

#mandar imagen de frase
@app.route('/apie/frases/<int:id>/image', methods=['GET'])
def imagen_frase(id):
    c.reconnect()
    cursor = c.cursor()
    query = "SELECT imagen FROM frases WHERE id = %s"
    cursor.execute(query, (id,))
    imagen = cursor.fetchone()[0]
    cursor.close()
    imagen_base64 = base64.b64encode(imagen).decode('utf-8')
    formato_imagen = imghdr.what(None, imagen)
    response = jsonify({
        'imagen_base64': imagen_base64,
        'formato_imagen': formato_imagen
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
















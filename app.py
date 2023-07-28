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

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="diccionarioelectronico"
)

if db.is_connected():
    print("La conexión a la base de datos se estableció correctamente")
else:    
    print("La conexión a la base de datos no se pudo establecer")

@app.route('/')
def inicio():
    return 'Servidor escuchando'


# Rutas para guardar informacion
@app.route('/api/guardarpalabras', methods=['POST'])
def crear_palabra():
    palabra = request.form.get('palabra')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(palabra, significado, imagen)

    cursor = db.cursor()
    query = "INSERT INTO palabras (palabras, significado, imagen) VALUES (%s, %s, %s)"
    values = (palabra, significado, imagendata)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    
    return jsonify({'message': 'palabra creada exitosamente'})

@app.route('/api/guardarfrase', methods=['POST'])
def crear_frase():
    frase = request.form.get('frases')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(frase, significado, imagen)
    db.reconnect()
    cursor = db.cursor()
    query = "INSERT INTO frases (frases, significado, imagen) VALUES (%s, %s, %s)"
    values = (frase, significado, imagendata)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

        
    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})

@app.route('/api/guardarrefran', methods=['POST'])
def crear_refran():
    refran = request.form.get('refran')
    significado = request.form.get('significado')
    imagen = request.files['imagen']
    imagendata = imagen.read()

    print(refran, significado, imagen)

    db.reconnect()
    cursor = db.cursor()
    query = "INSERT INTO refranes (refranes, significado, imagen) VALUES (%s, %s, %s)"
    values = (refran, significado, imagendata)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

        
    # Aquí puedes realizar la lógica para guardar el nuevo dato en una base de datos, por ejemplo
    return jsonify({'message': 'Dato creado exitosamente'})



# Ruta para enviar la informacion
@app.route('/api/palabras', methods=['GET'])
def obtenerPalabras():
    db.reconnect()
    cursor = db.cursor()
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

@app.route('/api/refranes', methods=['GET'])
def obtenerrefranes():
    db.reconnect()
    cursor = db.cursor()
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

@app.route('/api/frases', methods=['GET'])
def obtenerFrases():
    db.reconnect()
    cursor = db.cursor()
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
@app.route('/api/showtable', methods=['GET'])
def showpalabras():
    db.reconnect()
    cursor = db.cursor()
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
@app.route('/api/palabras/<int:id>', methods=['DELETE'])
def eliminar_palabra(id):
    db.reconnect()
    cursor = db.cursor()
    query = "DELETE FROM palabras WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'Palabra eliminada correctamente'})

#editar palabras
@app.route('/api/palabras/<int:id>', methods=['PUT'])
def editar_palabra(id):

    nueva_palabra = request.json.get('palabra')
    nuevo_significado = request.json.get('significado')
    print(nueva_palabra, nuevo_significado)

    db.reconnect()
    cursor = db.cursor()
    query = "UPDATE palabras SET palabras = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_palabra, nuevo_significado, id,))
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'Palabra editada correctamente'})

#mandar imagen de palabras
@app.route('/api/palabras/<int:id>/image', methods=['GET'])
def imagen_palabras(id):
    db.reconnect()
    cursor = db.cursor()
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
@app.route('/api/showtabler', methods=['GET'])
def showorefranes():
    db.reconnect()
    cursor = db.cursor()
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
@app.route('/api/refranes/<int:id>', methods=['DELETE'])
def eliminar_refran(id):
    db.reconnect()
    cursor = db.cursor()
    query = "DELETE FROM refranes WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'refran eliminado correctamente'})

#editar refranes
@app.route('/api/refranes/<int:id>', methods=['PUT'])
def editar_refran(id):

    nuevo_refran = request.json.get('oracion')
    nuevo_significado = request.json.get('significado')
    print(nuevo_refran, nuevo_significado)

    db.reconnect()
    cursor = db.cursor()
    query = "UPDATE refranes SET refranes = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nuevo_refran, nuevo_significado, id,))
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'refran editado correctamente'})

#mandar imagen de refran
@app.route('/api/refranes/<int:id>/image', methods=['GET'])
def imagen_refran(id):
    db.reconnect()
    cursor = db.cursor()
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
@app.route('/api/showtablef', methods=['GET'])
def showofrases():
    db.reconnect()
    cursor = db.cursor()
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
@app.route('/api/frases/<int:id>', methods=['DELETE'])
def eliminar_frases(id):
    db.reconnect()
    cursor = db.cursor()
    query = "DELETE FROM frases WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'frase eliminada correctamente'})

#editar frase
@app.route('/api/frases/<int:id>', methods=['PUT'])
def editar_frase(id):

    nueva_frase = request.json.get('frase')
    nuevo_significado = request.json.get('significado')
    print(nueva_frase, nuevo_significado)

    db.reconnect()
    cursor = db.cursor()
    query = "UPDATE frases SET frases = %s, significado = %s WHERE id = %s"
    cursor.execute(query, (nueva_frase, nuevo_significado, id,))
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'frase editada correctamente'})

#mandar imagen de frase
@app.route('/api/frases/<int:id>/image', methods=['GET'])
def imagen_frase(id):
    db.reconnect()
    cursor = db.cursor()
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
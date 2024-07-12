from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, "source", "templates")

app = Flask(__name__, template_folder= template_dir)

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    myresultado = cursor.fetchall()
    #Convertir los datos a diccionario
    insertarObjeto = []
    columnaNombres = [columna[0] for columna in cursor.description]
    for registros in myresultado:
        insertarObjeto.append(dict(zip(columnaNombres, registros)))
    cursor.close()
    return render_template('index.html', data=insertarObjeto)

@app.route('/usuarios', methods=['POST'])  #'/usuarios<string:id>', method=['POST']
def agregarUsuarios():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    edad = request.form['edad']
    email = request.form['email']

    if nombre and apellido and edad and email:
        cursor = db.database.cursor()
        sql = "INSERT INTO usuarios (nombre, apellido, edad, email) VALUES (%s, %s, %s, %s)"
        data = (nombre,apellido, edad, email)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/eliminar/<string:id>') #delete/<string:id>', method=['POST']
def eliminar(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/editar/<string:id>', methods=['POST'])
def editar(id):
    nombre=request.form['nombre']
    apellido=request.form['apellido']
    edad=request.form['edad']
    email=request.form['email']

    if nombre and apellido and edad and email:
        cursor = db.database.cursor()
        sql = "UPDATE usuarios SET  nombre=%s, apellido=%s, edad=%s, email=%s WHERE id=%s"
        data = (nombre, apellido, edad, email, id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
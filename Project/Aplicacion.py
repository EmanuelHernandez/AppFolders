#importar funciones de Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL




def action(consulta):
    cursor = mysql.connection.cursor()
    cursor.execute (consulta)
    mysql.connection.commit()
    return cursor

def action2(consulta,parametro):
    cursor = mysql.connection.cursor()
    cursor.execute (consulta,parametro)
    mysql.connection.commit()
    return cursor

app = Flask(__name__)

#Conexion SQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'proyecto'

mysql = MySQL(app)



#Inicializar sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cursor = mysql.connect.cursor()
    cursor.execute('SHOW FULL TABLES')
    datos = cursor.fetchall()

    return render_template('index.html', items = datos)


@app.route('/view_items/<string:Tables_in_proyecto>')
def view_items(Tables_in_proyecto):
    cursor = action("SELECT * FROM "+Tables_in_proyecto)
    datos = cursor.fetchall()


    return render_template('view_items.html', items = datos, nametable = Tables_in_proyecto)



@app.route('/add_item/<nametable>', methods=['POST'])
def add_items(nametable):
    if request.method == 'POST':
        fullname = request.form['fullname']
        action2("INSERT INTO "+ nametable +" (nombre) VALUES (%s)",[fullname])


        flash('Item agregado correctamente')
        return redirect('/view_items/'+nametable)
        

@app.route('/edit/<Tables_in_proyecto>/<id>')
def obtener_data(Tables_in_proyecto, id):
    cursor = action("SELECT * FROM "+ Tables_in_proyecto +" where id = {0}".format (id))
    datos = cursor.fetchall()


    return render_template('editar-items.html', items = datos[0], nametable = Tables_in_proyecto)

@app.route('/modificar/<nametable>/<id>', methods=['POST'])
def modificar_items(nametable,id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        
        cursor = mysql.connection.cursor()
        cursor.execute ("""
        UPDATE """+nametable+"""
            SET nombre = %s
        WHERE id = %s
        
        """,[fullname, id])
        mysql.connection.commit()
        flash('Items modificado correctamente')


    return redirect('/view_items/'+nametable)


@app.route('/delete/<nametable>/<id>')
def delete(nametable,id):
    action("DELETE FROM "+nametable+" WHERE id = {0}".format (id))


    flash('Item eliminado correctamente')
    return redirect('/view_items/'+nametable)

    
@app.route('/delete/<folder>')
def delete_folder(folder):
    action("DROP TABLE "+folder)


    flash('Folder eliminado correctamente')
    return redirect(url_for('index'))



@app.route('/add_folder' ,methods = ['POST'])
def add_folder():
    if request.method == 'POST':
        fullname = request.form['fullname']
        cursor = mysql.connection.cursor()
        cursor.execute ("""CREATE TABLE """+fullname+""" (
                ID int NOT NULL AUTO_INCREMENT,
                nombre varchar(150) NOT NULL,
                PRIMARY KEY (id)
                );""")
        mysql.connection.commit()


        flash('Folder creada correctamente')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
from re import U
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app= Flask(__name__,template_folder='./templates',static_folder='./templates/static')

#configure DB settings

USER_DB='postgres'
PASS_DB='postgres'
URL_DB='localhost'
NAME_DB='dap_flask_db'
FULL_URL_DB= f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#initialized sql alchemy objects
db=SQLAlchemy(app)

#configure flask-migrate
migrate= Migrate()
migrate.init_app(app, db)

class Persona(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(250))
    apellido=db.Column(db.String(250))
    email=db.Column(db.String(250))

    def __str__(self):
        return (
            f'id: {self.id}, '
            f'nombre: {self.nombre}, '
            f'apellido: {self.nombre}, '
            f'email: {self.nombre}, '
                )


@app.before_request
def before_request():
    print('Antes de la peticion')

@app.after_request
def after_request(response):
    print('Despues de la peticion')
    return response

@app.route('/')
def index ():

    personas = Persona.query.all()
    total_personas= Persona.query.count()

    cursos =['Python', 'Java', 'C++', 'Html', 'Css']
    data = {
        'titulo':'Bienvenido a la API',
        'home':'Inicio',
        'cursos': cursos,
        'nroCursos':len(cursos)
    }
    app.logger.debug(f'Listado de personas {personas}')
    app.logger.debug(f'Cantidad de personas {total_personas}')
    return render_template('index.html', data= data, personas= personas, total_personas= total_personas )

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre,edad):
    data ={
        'titulo':'contacto',
        'nombre':nombre,
        'edad':edad
    }
    return render_template('contacto.html', data= data)

def query_string(): 
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return 'Ok'

def pagina_no_encontrada(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True, port=5000)
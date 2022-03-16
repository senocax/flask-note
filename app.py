from crypt import methods
from re import U
from wsgiref.validate import validator
from xml.dom.minidom import Identified
from flask import Flask, redirect, render_template, request, request_started, url_for
from flask_migrate import Migrate
from forms import PersonaForm

from models import *
from database import *


app= Flask(__name__,template_folder='./templates',static_folder='./templates/static')

#configure DB settings

USER_DB='postgres'
PASS_DB='postgres'
URL_DB='localhost'
NAME_DB='dap_flask_db'
FULL_URL_DB= f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

#configure flask-migrate
migrate= Migrate()
migrate.init_app(app, db)

#configure flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'


@app.before_request
def before_request():
    print('Antes de la peticion')

@app.after_request
def after_request(response):

    print('Despues de la peticion')
    return response

@app.route('/')
def index ():

    personas = Persona.query.order_by('id')
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

@app.route('/contacto/<int:id>')
def contacto(id):
    persona = Persona.query.get(id)
    app.logger.debug(f"la persona es {persona.id}")
    return render_template('contacto.html', persona= persona)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj = persona)
    if (request.method == "POST") :
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f"Se insertara en la Db {persona}")
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for("index"))

    return render_template('agregar.html', forma = personaForm )
@app.route('/editar/<int:id>', methods=['GET' , 'POST'])
def editar(id):
    persona = Persona.query.get(id)
    personaForma= PersonaForm(obj=persona)
    if(request.method == 'POST'):
        if personaForma.validate_on_submit():
            personaForma.populate_obj(persona)
            app.logger.debug(f"Se edatara en la Db {persona}")
            db.session.commit()
            return redirect(url_for("index"))

    return render_template('editar.html',persona = persona, forma = personaForma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get(id)
    app.logger.debug(f"Se eliminara en la Db {persona}")
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for("index"))


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
from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def index ():

    cursos =['Python', 'Java', 'C++', 'Html', 'Css']
    data = {
        'titulo':'Bienvenido a la API',
        'home':'Inicio',
        'cursos': cursos,
        'nroCursos':len(cursos)
    }

    return render_template('index.html', data= data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import Usuario, Cultivo, Solicitud, Solicitud_detalle, Reporte
from dao import UsuarioDao, CultivoDao, SolicitudDao, Solicitud_detalleDao
# , ReporteDao

app = Flask(__name__)
app.secret_key = 'ucom'

conn = psycopg2.connect(dbname='sys_riego', user='postgres',
                        password='postgres', host='localhost', port=5432)

cur = conn.cursor()

usuario_dao = UsuarioDao(conn)
cultivo_dao = CultivoDao(conn)
solicitud_dao = SolicitudDao(conn)
solicitud_detalle_dao = Solicitud_detalleDao(conn)
#reporte_dao = ReporteDao(conn)


@app.route('/')
def home():
    return render_template('home.html', titulo='')


@app.route('/new_user')
def newUser():
    return render_template('newUser.html', titulo='Registrar usuario')


@app.route('/save_user', methods=['POST', ])
def saveUser():
    nombre = request.form['name']
    email = request.form['email']
    usuario = request.form['username']
    senha = request.form['password']
    usuario = Usuario('0', nombre, email, '', '',
                      '', '', '', '', usuario, senha)
    usuario_dao.salvar(usuario)
    return render_template('login.html', titulo='Login')


@app.route('/listar_cultivos')
def listar_cultivos():
    listar_cultivos = cultivo_dao.listar()
    return render_template('listar_cultivo.html', titulo='Lista de cultivos', cultivos=listar_cultivos)


@app.route('/nuevo_cultivo')
def adicionar_cultivo():
    # if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
    # return redirect(url_for('login', proxima=url_for('adicionar_cultivo')))
    return render_template('adicionar_cultivo.html', titulo='Adicionar cultivo')


@app.route('/crear_cultivo', methods=['POST', ])
def crear_cultivo():
    nombre_cultivo = request.form['nombre_cultivo']
    descripcion_cultivo = request.form['descripcion_cultivo']
    necesidad_agua = request.form['necesidad_agua']
    cultivo = Cultivo(nombre_cultivo, descripcion_cultivo, necesidad_agua)
    cultivo_dao.salvar(cultivo)
    return redirect(url_for('listar_cultivos'))


@app.route('/remover_cultivo/<int:id>')
def remover_cultivo(id):
    cultivo_dao.deletar(id)
    flash('El cultivo fue eliminado')
    return redirect(url_for('listar_cultivos'))


@app.route('/editar_cultivo/<int:id>')
def editar_cultivo(id):
    # if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
    # return redirect(url_for('login', proxima=url_for('editar_cultivo', id=id)))

    cultivo_editar = cultivo_dao.busca_por_id(id)
    return render_template('editar_cultivo.html', titulo='Editando cultivo', cultivo=cultivo_editar)


@app.route('/actualizar_cultivo', methods=['POST', ])
def actualizar_cultivo():
    id = request.form['id']
    nombre_cultivo = request.form['nombre_cultivo']
    descripcion_cultivo = request.form['descripcion_cultivo']
    necesidad_agua = request.form['necesidad_agua']
    cultivo_actual = Cultivo(
        nombre_cultivo, descripcion_cultivo, necesidad_agua, id)
    cultivo_dao.salvar(cultivo_actual)
    return redirect(url_for('listar_cultivos'))


@app.route('/listar_solicitudes')
def listar_solicitudes():
    listar_solicitudes = solicitud_dao.listar_solicitudes_productores
    return render_template('listar_solicitud.html', titulo='Lista de solicitudes', pedidos=listar_solicitudes)


@app.route('/nueva_solicitud')
def adicionar_solicitud():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('adicionar_solicitud')))
    usuarios = usuario_dao.listar()
    cultivos = cultivo_dao.listar()
    return render_template('adicionar_solicitud.html', titulo='Adicionar solicitud', usuarios=usuarios, cultivos=cultivos)


@app.route('/crear_solicitud', methods=['POST', ])
def crear_solicitud():
    id_usuario = request.form['id_usuario']
    solicitud = Solicitud(id_usuario, 0, 0, 0, 0, 0)
    solicitud_dao.salvar(solicitud)
    # salvar detalles
    cultivos = cultivo_dao.listar()
    for cultivo in cultivos:
        if(request.form.get('cultivoId_' + str(cultivo.id), None) is None):
            continue
        else:
            cultivoId = request.form['cultivoId_' + str(cultivo.id)]
            cantidad_plantas = request.form['cantidad_plantas_' +
                                            str(cultivo.id)]

            print(cultivoId + ' cantidad_plantas ' + cantidad_plantas)
            solicitud_detalle = Solicitud_detalle(
                solicitud.id, solicitud.id, cultivo.id, cantidad_plantas)
            solicitud_detalle_dao.salvar(solicitud_detalle)

    return redirect(url_for('listar_solicitudes'))


@app.route('/detalle_pedido/<int:id>')
def detalle_solicitud(id):
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('detalle_solicitud')))
    solicitud = solicitud_dao.busca_por_id(id)
    usuario = usuario_dao.busca_por_id(solicitud.id_usuario)
    detalles = solicitud_detalle_dao.listar(solicitud.id)
    return render_template('detalle_solicitud.html', titulo='Detalle solicitud', solicitud=solicitud, usuario=usuario, detalles=detalles)


# auth
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.busca_por_usuario(request.form['usuario'])
    if usuario is not None and usuario.senha == request.form['senha']:
        session['usuario_conectado'] = usuario.id
        session['usuario_usuario'] = usuario.usuario
        flash(usuario.nombre + ' conectado con éxito!')
        proxima = request.form['proxima']
        return redirect(proxima)
    else:
        flash('No conectado intente de nuevo')
        return redirect(url_for('login'))

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_conectado'] = None
    flash('Ningún usuario conectado!')
    return redirect(url_for('home'))
    
@app.route('/listCropType')
def listCropType():
    listCropType = cultivo_dao.listar()
    return render_template('listCropType.html', titulo='Tipos de cultivos', cropTypes=listCropType)


if __name__ == '__main__':
    app.run(debug=True)

from unittest.mock import create_autospec
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
# reporte_dao = ReporteDao(conn)


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


@app.route('/edit_user')
def editUser():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('editUser')))

    id = session['usuario_id']
    usuario = usuario_dao.busca_por_id(id)
    return render_template('editUser.html', titulo='Editar usuario', usuario=usuario)


@app.route('/update_user', methods=['POST', ])
def updateUser():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('editUser')))

    id = session['usuario_id']
    nombre = request.form['name']
    email = request.form['email']
    ciruc = request.form['ciruc']
    celular = request.form['celular']
    direccion = request.form['direccion']
    ciudad = request.form['ciudad']
    departamento = request.form['departamento']
    has = request.form['has']
    usuario = Usuario(ciruc, nombre, email, celular, direccion,
                      ciudad, departamento, has, '', '', '', id)
    usuario_dao.salvar(usuario)
    return render_template('home.html', titulo='Home')


@app.route('/edit_password')
def editPass():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('editPass')))

    id = session['usuario_id']
    usuario = usuario_dao.busca_por_id(id)
    return render_template('editPass.html', titulo='Editar password', usuario=usuario)


@app.route('/update_password', methods=['POST', ])
def updatePass():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('editPass')))

    id = session['usuario_id']
    senha = request.form['senha']

    usuario_dao.salvar_senha(id, senha)
    return render_template('home.html', titulo='Home')


@app.route('/listar_solicitudes')
def listar_solicitudes():
    listar_solicitudes = solicitud_dao.listar_solicitudes_productores
    return render_template('listar_solicitud.html', titulo='Lista de solicitudes', pedidos=listar_solicitudes)


@app.route('/new_calculation')
def newCalculation():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('newCalculation')))

    usuario = usuario_dao.busca_por_id(id=session['usuario_id'])
    cultivos = cultivo_dao.listar()
    return render_template('newCalculation.html', titulo='Cancular', usuarios=usuario, cultivos=cultivos)


@app.route('/save_calculation', methods=['POST', ])
def saveCalculation():
    id_usuario = session['usuario_id']
    has_cultivadas = request.form['has_cultivadas']
    agua_disponible = request.form['agua_disponible']
    horas_riego = request.form['horas_riego']
    hora_inicio = request.form['hora_inicio']

    solicitud = Solicitud(id_usuario, has_cultivadas,
                          agua_disponible, horas_riego, 0, hora_inicio)
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
                solicitud.id, cultivo.id, cantidad_plantas)
            solicitud_detalle_dao.salvar(solicitud_detalle)

    # Calculo GEKKO

    return redirect(url_for('show_report'))


@app.route('/detalle_solicitud/<int:id>')
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
        session['usuario_conectado'] = True
        session['usuario_id'] = usuario.id
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


@app.route('/newCropType')
def newCropType():
    # if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
    # return redirect(url_for('login', proxima=url_for('adicionar_cultivo')))
    return render_template('newCropType.html', titulo='Agregar nuevo tipo de cultivo')


@app.route('/saveNewCropType', methods=['POST', ])
def saveNewCropType():
    nombre_cultivo = request.form['nombre_cultivo']
    descripcion_cultivo = request.form['descripcion_cultivo']
    necesidad_agua = request.form['necesidad_agua']
    cultivo = Cultivo(nombre_cultivo, descripcion_cultivo, necesidad_agua)
    cultivo_dao.salvar(cultivo)
    return redirect(url_for('listCropType'))


@app.route('/updateCropType/<int:id>')
def updateCropType(id):
    # if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
    # return redirect(url_for('login', proxima=url_for('editar_cultivo', id=id)))

    updateCropType = cultivo_dao.busca_por_id(id)
    return render_template('updateCropType.html', titulo='Editar cultivo', cropType=updateCropType)


@app.route('/saveCropTypeUpdated', methods=['POST', ])
def saveCropTypeUpdated():
    id = request.form['id']
    nombre_cultivo = request.form['nombre_cultivo']
    descripcion_cultivo = request.form['descripcion_cultivo']
    necesidad_agua = request.form['necesidad_agua']
    cultivo_actual = Cultivo(
        nombre_cultivo, descripcion_cultivo, necesidad_agua, id)
    cultivo_dao.salvar(cultivo_actual)
    return redirect(url_for('listCropType'))


@app.route('/removeCropType/<int:id>')
def removeCropType(id):
    cultivo_dao.deletar(id)
    flash('El tipo de cultivo fue eliminado')
    return redirect(url_for('listCropType'))


@app.route('/newCalc')
def newCalc():
    # if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
    # return redirect(url_for('login', proxima=url_for('adicionar_cultivo')))
    listCropType = cultivo_dao.listar()
    return render_template('newCalc.html', titulo='Solicitar nuevo calculo de riego', cropTypes=listCropType)


@app.route('/saveNewCalc', methods=['POST', ])
def saveNewCalc():
    id_usuario = 5
    has_cultivadas = 5
    agua_disponible = request.form['agua_disponible']
    horas_riego = request.form['horas_riego']
    hora_inicio = request.form['hora_inicio']

    solicitud = Solicitud(id_usuario, has_cultivadas,
                          agua_disponible, horas_riego, 0, hora_inicio)
    solicitud_dao.salvar(solicitud)
    # salvar detalles
    crops = request.form.getlist('cultivoId[]')
    plantsQ = request.form.getlist('cantidad_plantas[]')

    for crop_id, crop_value in enumerate(crops):
        solicitud_detalle = Solicitud_detalle(
            solicitud.id, crop_value, plantsQ[crop_id])
        solicitud_detalle_dao.salvar(solicitud_detalle)

    return redirect(url_for('showCalcResult', requestId=solicitud.id))

    # Calculo GEKKO

    # return redirect(url_for('show_report'))

@app.route('/showCalcResult/<int:requestId>')
def showCalcResult(requestId):
    # if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
    # return redirect(url_for('login', proxima=url_for('adicionar_cultivo')))
   # listCropType = cultivo_dao.listar()
    return render_template('showCalcResult.html', titulo='Calculo de riego')

@app.route('/newCalcdd')
def newCasslc():
    if 'usuario_conectado' not in session or session['usuario_conectado'] == None:
        return redirect(url_for('login', proxima=url_for('newCalc')))
    id = session['usuario_id']

    usuario = usuario_dao.busca_por_id(id=session['usuario_id'])
    cultivos = cultivo_dao.listar()
    return render_template('newCalc.html', titulo='Calcular', usuarios=usuario, cultivos=cultivos)


if __name__ == '__main__':
    app.run(debug=True)

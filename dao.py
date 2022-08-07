from models import Usuario, Cultivo, Solicitud, Solicitud_detalle, Reporte

SQL_USUARIO_POR_ID = 'SELECT id, ciruc, nombre, email,  celular, direccion, ciudad, departamento, has, obs, usuario, senha FROM usuario WHERE id = %s'
SQL_USUARIO_POR_USUARIO = 'SELECT id, ciruc, nombre,  email, celular, direccion, ciudad, departamento, has, obs, usuario, senha FROM usuario WHERE usuario = %s'
SQL_BUSCA_USUARIOS = 'SELECT id, ciruc, nombre, email, celular, direccion, ciudad, departamento, has, obs, usuario, senha FROM usuario'
SQL_ACTUALIZA_USUARIO = 'UPDATE usuario SET  ciruc = %s, nombre = %s, email = %s, celular = %s, direccion = %s, ciudad = %s, departamento = %s, has = %s, obs = %s WHERE id = %s'
SQL_CREA_USUARIO = 'INSERT INTO usuario (nombre, email, usuario, senha) VALUES ( %s, %s, %s, %s)'

SQL_DELETE_CULTIVO = 'DELETE FROM cultivo WHERE id = %s'
SQL_CULTIVO_POR_ID = 'SELECT id, nombre_cultivo, descripcion_cultivo, necesidad_agua FROM cultivo WHERE id = %s'
SQL_ACTUALIZA_CULTIVO = 'UPDATE cultivo SET nombre_cultivo = %s, descripcion_cultivo = %s, necesidad_agua = %s WHERE id = %s'
SQL_BUSCA_CULTIVOS = 'SELECT * FROM cultivo'
SQL_CREA_CULTIVO = 'INSERT INTO cultivo (nombre_cultivo, descripcion_cultivo, necesidad_agua) VALUES ( %s, %s, %s)'

SQL_CREA_SOLICITUD = 'INSERT INTO solicitud(id_usuario, has_cultivadas, agua_disponible, horas_riego, lineas_riego, hora_inicio) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id'
SQL_ACTUALIZA_SOLICITUD = 'UPDATE solicitud SET id_usuario = %s, has_cultivadas = %s, agua_disponible = %s, horas_riego = %s, lineas_riego = %s, hora_inicio = %s WHERE id = %s'
SQL_SOLICITUD_POR_ID = 'SELECT id, id_usuario, has_cultivadas, agua_disponible, horas_riego, lineas_riego, hora_inicio  FROM solicitud WHERE id = %s'
SQL_BUSCA_SOLICITUDES = 'SELECT id, id_usuario, has_cultivadas, agua_disponible, horas_riego, lineas_riego, hora_inicio FROM solicitud'
SQL_BUSCA_SOLICITUDES_USUARIOS = 'SELECT id, id_usuario, has_cultivadas, agua_disponible, horas_riego, lineas_riego, hora_inicio FROM solicitud'

SQL_CREA_SOLICITUD_DETALLE = 'INSERT INTO solicitud_detalle (id_solicitud, id_cultivo, cantidad_plantas) VALUES (%s, %s, %s)'
SQL_ACTUALIZA_SOLICITUD_DETALLE = 'UPDATE solicitud_detalle SET id_solicitud = %s, id_cultivo = %s, cantidad_plantas = %s  WHERE id = %s'
SQL_SOLICITUD_DETALLES_POR_ID = 'SELECT id, id_solicitud, id_cultivo, cantidad_plantas  WHERE id = %s'

SQL_CREA_REPORTE = 'INSERT INTO reporte (id_solicitud,id_solicitud_detalle, id_cultivo, nombre_cultivo, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, registro_reporte) VALUES ( %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)'


# idPedido, idCombo, nombre, descripcion, precio, cantidad, subtotal, id=None
SQL_BUSCA_SOLICITUD_DETALLES_CULTIVOS = 'SELECT sd.id, sd.id_solicitud, sd.id_cultivo, c.nombre_cultivo, c.descripcion_cultivo, pd.precio, pd.cantidad, pd.subtotal FROM solicitud_detalle as sd JOIN cultivo as c ON sd.id_cultivo = c.id WHERE sd.id_cultivo = %s'


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, usuario):
        cursor = self.__db.cursor()

        if(usuario.id):
            cursor.execute(SQL_ACTUALIZA_USUARIO, (usuario.ciruc, usuario.nombre, usuario.email, usuario.celular,
                           usuario.direccion, usuario.ciudad, usuario.departamento, usuario.has, usuario.obs, usuario.id))
        else:
            cursor.execute(SQL_CREA_USUARIO, (usuario.nombre,
                           usuario.email, usuario.usuario, usuario.senha))
            usuario.id = cursor.lastrowid
        self.__db.commit()
        return usuario

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_USUARIOS)
        usuarios = traduce_usuarios(cursor.fetchall())
        return usuarios

    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], tupla[11], id=tupla[0])

    def busca_por_usuario(self, usuario):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_USUARIO, (usuario,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], tupla[11], id=tupla[0])


class CultivoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, cultivo):
        cursor = self.__db.cursor()

        if(cultivo.id):
            cursor.execute(SQL_ACTUALIZA_CULTIVO, (cultivo.nombre_cultivo,
                           cultivo.descripcion_cultivo, cultivo.necesidad_agua, cultivo.id))
        else:
            cursor.execute(SQL_CREA_CULTIVO, (cultivo.nombre_cultivo,
                           cultivo.descripcion_cultivo, cultivo.necesidad_agua))
            cultivo.id = cursor.lastrowid
        self.__db.commit()
        return cultivo

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_CULTIVOS)
        cultivos = traduce_cultivos(cursor.fetchall())
        return cultivos

    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_CULTIVO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Cultivo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.cursor().execute(SQL_DELETE_CULTIVO, (id,))
        self.__db.commit


class SolicitudDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, solicitud):
        cursor = self.__db.cursor()
        if (solicitud.id):
            cursor.execute(SQL_ACTUALIZA_SOLICITUD, (solicitud.id_usuario, solicitud.has_cultivadas, solicitud.agua_disponible,
                           solicitud.horas_riego, solicitud.lineas_riego, solicitud.hora_inicio, solicitud.id))
        else:
            cursor.execute(SQL_CREA_SOLICITUD,  (solicitud.id_usuario, solicitud.has_cultivadas,
                           solicitud.agua_disponible, solicitud.horas_riego, solicitud.lineas_riego, solicitud.hora_inicio))
            solicitud.id = cursor.fetchone()[0]
        self.__db.commit()
        return solicitud

    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_SOLICITUDES)
        solicitudes = traduce_solicitudes(cursor.fetchall())
        return solicitudes

    def listar_solicitudes_usuarios(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_SOLICITUDES_USUARIOS)
        solicitudes_usuarios = traduce_solicitudes_usuarios(cursor.fetchall())
        return solicitudes_usuarios

    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SOLICITUD_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Solicitud(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], id=tupla[0])


class Solicitud_detalleDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, solicitud_detalle):
        cursor = self.__db.cursor()
        if (solicitud_detalle.id):
            cursor.execute(SQL_ACTUALIZA_SOLICITUD_DETALLE, (solicitud_detalle.id_solicitud,
                           solicitud_detalle.id_cultivo, solicitud_detalle.cantidad_plantas, solicitud_detalle.id))
        else:
            cursor.execute(SQL_CREA_SOLICITUD_DETALLE,  (solicitud_detalle.id_solicitud,
                           solicitud_detalle.id_cultivo, solicitud_detalle.cantidad_plantas))
            solicitud_detalle.id = cursor.lastrowid
        self.__db.commit()
        return solicitud_detalle

    def listar(self, id_cultivo):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_SOLICITUD_DETALLES_CULTIVOS, (id_cultivo,))
        solicitud_detalle = traduce_solicitud_detalle(cursor.fetchall())
        return solicitud_detalle

    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SOLICITUD_DETALLES_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Solicitud(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], id=tupla[0])


def traduce_usuarios(usuarios):
    def crea_usuario_con_tupla(tupla):
        return Usuario(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], id=tupla[0])
    return list(map(crea_usuario_con_tupla, usuarios))


def traduce_cultivos(cultivos):
    def crea_cultivo_con_tupla(tupla):
        return Cultivo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(crea_cultivo_con_tupla, cultivos))


def traduce_solicitudes(solicitudes):
    def crea_solicitud_con_tupla(tupla):
        return Solicitud(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], id=tupla[0])
    return list(map(crea_solicitud_con_tupla, solicitudes))


def traduce_solicitudes_usuarios(solicitudes_usuarios):
    def crea_solicitud_usuario_con_tupla(tupla):
        return Solicitud(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], id=tupla[0])
    return list(map(crea_solicitud_usuario_con_tupla, solicitudes_usuarios))


def traduce_solicitud_detalle(solicitud_detalles):
    def crea_solicitud_detalle_con_tupla(tupla):
        return Solicitud_detalle(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(crea_solicitud_detalle_con_tupla, solicitud_detalles))

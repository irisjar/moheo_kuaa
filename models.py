
class Usuario:
    def __init__(self, ciruc, nombre,  celular, direccion, ciudad, departamento, has, obs, usuario, senha, id=None):
        self.id = id
        self.ciruc = ciruc
        self.nombre = nombre
        self.celular = celular
        self.direccion = direccion
        self.ciudad = ciudad
        self.departamento = departamento
        self.has = has
        self.obs = obs
        self.usuario = usuario
        self.senha = senha

class Cultivo:
    def __init__(self, nombre_cultivo, descripcion_cultivo, necesidad_agua, id=None):
        self.id = id
        self.nombre_cultivo = nombre_cultivo
        self.descripcion_cultivo = descripcion_cultivo
        self.necesidad_agua = necesidad_agua


class Solicitud:
    def __init__(self, id_productor, has_cultivadas, agua_disponible, horas_riego, lineas_riego, hora_inicio, id=None):
        self.id = id
        self.id_productor = id_productor
        self.has_cultivadas = has_cultivadas
        self.agua_disponible = agua_disponible
        self.horas_riego = horas_riego
        self.lineas_riego = lineas_riego
        self.hora_inicio = hora_inicio


class Solicitud_detalle:
    def __init__(self, id_solicitud, id_cultivo, cantidad_plantas, id=None):
        self.id = id
        self.id_solicitud = id_solicitud
        self.id_cultivo = id_cultivo
        self.cantidad_plantas = cantidad_plantas


class Reporte:
    def __init__(self, id_solicitud_detalle, nombre_cultivo, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14,
                 h15, h16, h17, h18, h19, h20, h21, h22, h23, registro_reporte, id=None):
        self.id = id
        self.id_solicitud_detalle = id_solicitud_detalle
        self.nombre_cultivo = nombre_cultivo
        self.h0 = h0
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.h6 = h6
        self.h7 = h7
        self.h8 = h8
        self.h9 = h9
        self.h10 = h10
        self.h11 = h11
        self.h12 = h12
        self.h13 = h13
        self.h14 = h14
        self.h15 = h15
        self.h16 = h16
        self.h17 = h17
        self.h18 = h18
        self.h19 = h19
        self.h20 = h20
        self.h21 = h21
        self.h22 = h22
        self.h23 = h23
        self.registro_reporte = registro_reporte

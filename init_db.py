import psycopg2
print('Conectando...')
conn = psycopg2.connect(dbname='sys_riego', user='postgres',
                        password='postgres', host='localhost', port=5432)


crear_tablas = '''
CREATE TABLE usuario(
    id serial NOT NULL,
    ciruc character varying(30) NOT NULL,
    nombre_productor character varying(100) NOT NULL,
    celular character varying(20),
    direccion character varying(200),
    ciudad character varying(50),
    departamento character varying(50),
    has real,
    obs text,
    nombre varchar(20) NOT NULL,
    senha varchar(8) NOT NULL,
    CONSTRAINT productor_pk PRIMARY KEY (id)
    );



CREATE TABLE cultivo(
    id serial NOT NULL,
    nombre_cultivo character varying(150) NOT NULL,
    descripcion_cultivo character varying(200),
    necesidad_agua real,
    CONSTRAINT cultivo_pk PRIMARY KEY (id)
);

CREATE TABLE solicitud(
    id serial NOT NULL,
    id_productor integer NOT NULL,  
    has_cultivadas real,
    agua_disponible real,
    horas_riego integer,
    lineas_riego integer,
    hora_inicio integer,
    hora_fin integer,
    CONSTRAINT solicitud_pk PRIMARY KEY (id),
    CONSTRAINT fk_detalle_productor FOREIGN KEY (id_productor)
        REFERENCES productor (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE public.solicitud_detalle
(
    id serial NOT NULL,
    id_solicitud integer NOT NULL,
    id_cultivo integer NOT NULL,
    cantidad_plantas integer,
    CONSTRAINT detalle_pk PRIMARY KEY (id),
    CONSTRAINT fk_detalle_solicitud FOREIGN KEY (id_solicitud)
        REFERENCES solicitud (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_detalle_cultivo FOREIGN KEY (id_cultivo)
        REFERENCES cultivo (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);


CREATE TABLE reporte(
    id serial NOT NULL,
    id_solicitud_detalle integer NOT NULL,
    nombre_cultivo  character varying(150),  
    h0 real,
    h1 real,
    h2 real,
    h3 real,
    h4 real,
    h5 real,
    h6 real,
    h7 real,
    h8 real,
    h9 real,
    h10 real,
    h11 real,
    h12 real,
    h13 real,
    h14 real,
    h15 real,
    h16 real,
    h17 real,
    h18 real,
    h19 real,
    h20 real,
    h21 real,
    h22 real,
    h23 real,
    registro_reporte date,
    CONSTRAINT reporte_pk PRIMARY KEY (id),
    CONSTRAINT fk_reporte_detalle FOREIGN KEY (id_solicitud_detalle)
        REFERENCES solicitud_detalle (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);'''


# conn.cursor().execute(crear_tablas)

# insertando usuarios
cursor = conn.cursor()

cursor.execute('select * from usuario')
print(' -------------  Usuarios:  -------------')
for user in cursor.fetchall():
    print(user[1])

conn.commit()
cursor.close()

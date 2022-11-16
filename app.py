import pymysql
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


username = 'root'
password = 'misiontic'
server = 'localhost'
database = '/restaurante'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sxd3I36ubucy3YUMXLz7@containers-us-west-85.railway.app:7295/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Data(db.Model):  # type: ignore
    __tablename__ = 'activosfijos'
    
    idregistro = db.Column(db.Integer, primary_key = True)
    codco = db.Column(db.String(50), index=True)
    codigo = db.Column(db.String(50), index=True)
    descripcion = db.Column(db.String(200), index=True)
    tipo = db.Column(db.String(200), index=True)
    caracteristicas = db.Column(db.String(200), index=True)
    ubicacion = db.Column(db.String(50), index=True)
    centrodecosto = db.Column(db.String(50), index=True)
    cantidad = db.Column(db.String(64), index=True)
    valor = db.Column(db.String(100))
    iva = db.Column(db.String(100))
    adcimejoras = db.Column(db.String(100))
    aipi = db.Column(db.String(100))
    depreciacion = db.Column(db.String(100))
    aipidepreciacion = db.Column(db.String(100))
    total = db.Column(db.String(100))
    valorizacion = db.Column(db.String(100))
    fechaad = db.Column(db.String(100), index=True)
    proveedor = db.Column(db.String(100), index=True)
    factura = db.Column(db.String(50), index=True)

    def to_dict(self):
        return {
            'idregistro':       self.idregistro,
            'codco':            self.codco,
            'codigo':           self.codigo,
            'descripcion':      self.descripcion,
            'tipo':             self.tipo,
            'caracteristicas':  self.caracteristicas,
            'ubicacion':        self.ubicacion,
            'centrodecosto':    self.centrodecosto,
            'cantidad':         self.cantidad,
            'valor':            self.valor,
            'iva':              self.iva,
            'adcimejoras':      self.adcimejoras,
            'aipi':             self.aipi,
            'depreciacion':     self.depreciacion,
            'aipidepreciacion': self.aipidepreciacion,
            'total':            self.total,
            'valorizacion':     self.valorizacion,
            'fechaad':          self.fechaad,
            'proveedor':        self.proveedor,
            'factura':          self.factura      
        }

with app.app_context():
    db.create_all()

@app.route('/api/data')  # type: ignore
def data():

    query = Data.query

    #search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Data.codco.like(f'%{search}%'),
            Data.descripcion.like(f'%{search}%'),
            Data.centrodecosto.like(f'%{search}%'),
            Data.tipo.like(f'%{search}%')  
        ))
    total_filtered = query.count()

    #sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['codco', 'descripcion', 'centrodecosto', 'tipo']:
            col_name = 'codco'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Data, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)
    
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [data.to_dict() for data in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Data.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/add_data', methods = ["POST"])  # type: ignore
def add_data():
    codco = request.form['codco']
    descripcion = request.form['descripcion']
    centrodecosto = request.form['centrodecosto']
    tipo = request.form['tipo']
    
    new_row = Data(
        codco = codco,
        descripcion = descripcion,
        centrodecosto = centrodecosto,
        tipo = tipo,      
    )

    db.session.add(new_row)
    db.session.commit()

    print("data added")

    return redirect(url_for('index'))

@app.route('/db_test')
def testdb():
    try:
        db.engine.execute(text("SELECT 1"))
        return '<h1>It works.</h1>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'

@app.route("/")
def index():
    return render_template('index.html', title='Relacion de Activos')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
#Imports
from flask import Flask , request,jsonify
from flask_sqlalchemy import SQLAlchemy 
import psycopg2
from werkzeug.utils import cached_property
from flask_marshmallow import Marshmallow 
from flask_restplus import Api, fields , Resource 

#Conexões
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///postgres:mx72015@localhost:5432/Imoveis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
app.config['SECRET_KEY']=True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)

#Tabelas
class cliente(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome= db.Column(db.String)
    cpf = db.Column(db.Integer)
    estado_civil = db.Column(db.String)
    data_nascimento = db.Column(db.Integer)
    profissao = db.Column(db.String)
    rg = db.Column(db.Integer)
    nº = db.Column(db.Integer)
    rua = db.Column(db.String)
    endereco = db.Column(db.String)
    cep = db.Column(db.Integer)
    andar = db.Column(db.Integer)
    bloco = db.Column(db.String)
    cidade = db.Column(db.String)
    uf = db.Column(db.String)

class clienteSchema(ma.Schema):
    class Meta:
        fields = ('nome','cpf','estado_civil','data_nascimento', 
'profissão', 'rg', 'nº', 'rua', 'endereço', 'cep', 'andar', 'bloco','cidade', 'uf')


model = api.model('Dados',{
    'nome':fields.String('Digite o seu Nome'),
    'cpf':fields.String('Digite o seu CPF'),
    'estado_civil':fields.String('Digite o seu Estado_Civil'),
    'data_nascimento':fields.String('Entre com a Data_Nascimento'),
    'profissão':fields.String('Qual a sua Profissão'),
    'rg':fields.String('Digite o seu RG'),
    'n°':fields.String('Digite o seu Nº'),
    'rua':fields.String('Digite o nome da rua'),
    'endereço':fields.String('Digite o seu enderço'),
    'cep':fields.String('Digite o CEP'),
    'andar':fields.String('Digite o Andar'),
    'bloco':fields.String('Digite o Bloco'),
    'cidade':fields.String('Digite o nome de sua cidade'),
    'uf':fields.String('Digite a UF')
})

cliente_schema = clienteSchema()
clientes_schema = clienteSchema(many=True)

#Rotas
@api.route('/get')
class getdata(Resource):
    def get(self):
        return jsonify(clientes_schema.dump(cliente.query.all()))

@api.route('/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        cliente = cliente(nome=request.json['nome'],cpf=request.json['cpf'],estado_civil=request.json['estado_civil'],
data_nascimento=request.json['data_nascimento'], profissao=request.json['profissão'], rg=request.json['RG'], nº=request.json['Nº'],
rua=request.json['Rua'],endereco=request.json['Endereço'],cep=request.json['CEP'],andar=request.json['Andar'],
bloco=request.json['Bloco'],cidade=request.json['Cidade'],uf=request.json['UF'] )
        
        db.session.add(cliente)
        db.session.commit()
        return {'Mensagem':'Dado adicionado ao Banco de Dados'}

@api.route('/put/<int:id>')
class putdata(Resource):
    @api.expect(model)
    def put(self,id):
        cliente = cliente.query.get(id)
        cliente.nome = request.json['Nome']
        cliente.cpf = request.json['CPF']
        cliente.estado_civil = request.json['Estado_civil']
        cliente.data_nascimento = request.json['Data_nascimento']
        cliente.profissao = request.json['Profissão']
        cliente.rg = request.json['RG']
        cliente.nº = request.json['Nº']
        cliente.rua = request.json['Rua']
        cliente.endereco = request.json['Endereço']
        cliente.cep = request.json['CEP']
        cliente.andar = request.json['Andar']
        cliente.bloco = request.json['Bloco']
        cliente.cidade = request.json['Cidade']
        cliente.uf = request.json['UF']
        db.session.commit()
        return {'Mensagem':'Dado Atualizado com sucesso!'}

@api.route('/delete/<int:id>')
class deletedata(Resource):
    def delete(self,id):
        cliente = cliente.query.get(id)
        db.session.delete(cliente)
        db.session.commit()
        return {'Mensagem':'Dado deletado com sucesso!'}
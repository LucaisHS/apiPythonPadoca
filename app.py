from flask import Flask
from flask_cors import CORS

from db.db import db
from controllers.UsuarioController import usuario_bp  # Importa o blueprint
from controllers.EnderecoController import endereco_bp
from controllers.PedidoController import pedido_bp
from controllers.OpcoesController import opcoes_bp
from controllers.ProdutoController import produto_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})



# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/padariaSimplesApi'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/padariaSimplesApi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com a aplicação Flask
db.init_app(app)

# Registra o blueprint
app.register_blueprint(usuario_bp)
app.register_blueprint(endereco_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(opcoes_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

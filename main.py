from functools import wraps

from flask import Flask, request, jsonify #pip install flask
from flask_bcrypt import Bcrypt #pip install flask-bcrypt
import jwt #pip install PyJWT -> Nome completo: Json Web Token

from core.data.Faturamento import Faturamento
from core.data.Usuario import Usuarios

app = Flask(__name__)
bcrypt = Bcrypt(app)


def roles(_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get("Authorization")
            user_data = jwt.decode(token, "super-secret-key", algorithms=["HS256"])
            if len(list(filter(lambda item: item == user_data["role"], _roles))) > 0:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Não autorizado"), 401

        return decorator

    return wrapper


def token_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get("Authorization")

            if token is None or token == "":
                return jsonify(message="Token inválido"), 403
            else:
                try:
                    user_data = jwt.decode(token, "super-secret-key", algorithms=["HS256"])
                    kwargs["user_data"] = user_data

                    return fn(*args, **kwargs)
                except Exception as e:
                    return jsonify(message="Token inválido"), 403

        return decorator

    return wrapper


@app.route("/encryptpass/<password>", methods=["GET"])
def encryptpass(password):
    return {"encrypt": bcrypt.generate_password_hash(password).decode("utf-8")}


@app.route("/api/auth", methods=["POST"])
def auth():
    bodyData = request.get_json()
    if bodyData is not None:
        usuario = Usuarios(bcrypt)
        token = usuario.autenticarUsuario(bodyData["login"], bodyData["password"])

        if token is None:
            return {"status": 401, "message": "Usuário ou senha inválidos"}
        else:
            return {"status": 200, "token": token}
    else:
        return {"status": 401, "message": "Dados de autenticação obrigatórios"}


#Verbo GET: Serve para ler dados
@app.route("/api/faturamento", methods=["GET"])
@token_required()
@roles(["admin"])
def getFaturamentos(*args, **kwargs):
    faturamento = Faturamento()
    return jsonify(faturamentos=faturamento.lerFaturamentos())


@app.route("/api/faturamento/<id>", methods=["GET"])
@token_required()
@roles(["admin", "financeiro"])
def getFaturamento(id, *args, **kwargs):
    faturamento = Faturamento()
    return jsonify(faturamento=faturamento.lerFaturamento(id))


#Verbo POST: Serve para incluir novos registros
@app.route("/api/faturamento", methods=["POST"])
@token_required()
@roles(["admin", "financeiro"])
def postFaturamento(*args, **kwargs):
    bodyData = request.get_json() #bodyData é um DICTIONARY
    if bodyData is not None:
        faturamento = Faturamento()
        faturamento.Data = bodyData["Data"]
        faturamento.CodOrcamento = bodyData["CodOrcamento"]
        faturamento.CodProjeto = bodyData["CodProjeto"]
        faturamento.Faturamento = bodyData["Faturamento"]
        faturamento.incluirFaturamento()
        return {"status": 200, "message": "Faturamento incluído com sucesso!"}
    else:
        return {"status": 500, "message": "Dados para inclusão do faturamento obrigatórios"}


#Verbo PUT: Serve para atualizar dados
@app.route("/api/faturamento/<id>", methods=["PUT"])
@token_required()
def putFaturamento(id, *args, **kwargs):
    bodyData = request.get_json() #bodyData é um DICTIONARY
    if bodyData is not None:
        faturamento = Faturamento()
        faturamento.Data = bodyData["Data"]
        faturamento.CodOrcamento = bodyData["CodOrcamento"]
        faturamento.CodProjeto = bodyData["CodProjeto"]
        faturamento.Faturamento = bodyData["Faturamento"]
        faturamento.atualizarFaturamento(id)
        return {"status": 200, "message": "Registro atualizado com sucesso"}
    else:
        return {"status": 500,
                "message": "Não é possível atualizar registro sem "
                           "dados no corpo da requisição"}


#Verbo DELETE: Serve para remover dados
@app.route("/api/faturamento/<id>", methods=["DELETE"])
@token_required()
def deleteFaturamento(id, *args, **kwargs):
    faturamento = Faturamento()
    faturamento.apagarFaturamento(id)
    return {"status": 200, "message": "faturamento apagado com sucesso"}


if __name__ == "__main__":
    app.run()
import pyodbc #pip install pyodbc
import jwt #pip install PyJWT -> Nome completo: Json Web Token

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LOCALHOST;'
                      'Database=FATURAMENTO;'
                      'UID=sa;'
                      'PWD=sa;')

cursor = conn.cursor()


class Usuarios(object):

    def __init__(self, _bcrypt):
        self.bcrypt = _bcrypt

    def autenticarUsuario(self, login, password):
        cursor.execute("SELECT ID, ROLE, SENHA FROM USUARIO WHERE LOGIN = ?",
                       login)

        for user in cursor.fetchall():
            if self.bcrypt.check_password_hash(str(user[2]), password):
                encoded_jwt = jwt.encode({"user_id": str(user[0]), "role": str(user[1])}, "super-secret-key", algorithm="HS256") #Geração de token
                return encoded_jwt

        return None
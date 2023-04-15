'''
Criado 14/02 por Victor C.
Classe DAO responsável pelas operação CRUD e autênticação com o BD de autênticação

Metódos testados: create, get, delete, update
O restante precisa da definição de como serão gerados os tokens

'''
from datetime import datetime

class AuthDAO:

    def __init__(self, bdAuth):
        self.conexao = bdAuth.conectar()



    def create_user(self, email, password):
        cursor = self.conexao.cursor()
        cursor.execute(
            'INSERT INTO auth.users (email, password) VALUES (%s, %s) RETURNING id',
            (email, password)
        )
        user_id = cursor.fetchone()[0]
        self.conexao.commit()
        cursor.close()
        return user_id

    def get_user(self, user_id):
        cursor = self.conexao.cursor()
        cursor.execute(
            'SELECT email, criado_em FROM auth.users WHERE id = %s',
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return {'id': user_id, 'email': row[0], 'criado_em': row[1]}
        else:
            return None

    def update_user(self, user_id, email, senha):
        cursor = self.conexao.cursor()
        cursor.execute(
            'UPDATE auth.users SET email = %s, password = %s WHERE id = %s',
            (email, senha, user_id)
        )
        self.conexao.commit()
        cursor.close()

    def delete_user(self, user_id):
        cursor = self.conexao.cursor()
        cursor.execute(
            'DELETE FROM auth.users WHERE id = %s',
            (user_id,)
        )
        self.conexao.commit()
        cursor.close()

    def create_token(self, user_id, token_acesso, atualiza_token, expira_em):
        cursor = self.conexao.cursor()
        cursor.execute(
            'INSERT INTO auth.tokens (user_id, token_acesso, atualiza_token, expira_em) VALUES (%s, %s, %s, %s)',
            (user_id, token_acesso, atualiza_token, expira_em)
        )
        self.conexao.commit()
        cursor.close()

    def get_token(self, token_acesso):
        cursor = self.conexao.cursor()
        cursor.execute(
            'SELECT user_id, expira_em FROM auth.tokens WHERE token_acesso = %s',
            (token_acesso,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return {'user_id': row[0], 'expira_em': row[1]}
        else:
            return None

    def revoca_token(self, token_acesso):
        cursor = self.conexao.cursor()
        cursor.execute(
            'DELETE FROM auth.tokens WHERE token_acesso = %s',
            (token_acesso,)
        )
        self.conexao.commit()
        cursor.close()

    def limpa_tokens_expirados(self):
        cursor = self.conexao.cursor()
        cursor.execute(
            'DELETE FROM auth.tokens WHERE expira_em < %s',
            (datetime.now(),)
        )
        self.conexao.commit()
        cursor.close()
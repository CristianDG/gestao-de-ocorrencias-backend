'''
Criado 14/02 por Victor C.
Classe DAO responsável pelas operação CRUD de usuários

Metódos testados: create, get, delete, update

'''


class UsuarioDAO:

    def __init__(self, db):
        self.conexao = db.conectar()

    def create_user(self, email, password):
        cursor = self.conexao.cursor()
        cursor.execute(
            'INSERT INTO auth.users (email, password) VALUES (%s, %s) RETURNING id;',
            (email, password)
        )
        user_id = cursor.fetchone()[0]
        self.conexao.commit()
        cursor.close()
        return user_id

    def get_user(self, user_id):
        cursor = self.conexao.cursor()
        cursor.execute(
            'SELECT email, criado_em FROM auth.users WHERE id = %s;',
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
            'UPDATE auth.users SET email = %s, password = %s WHERE id = %s;',
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

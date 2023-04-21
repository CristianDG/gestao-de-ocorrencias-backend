'''
Criado 14/02 por Victor C.
Classe DAO responsável pelas operação CRUD de usuários

Metódos testados: create, get, delete, update


modificado dia 21/04
Alterei os bancos, de modo a relacionar um id do banco de autênticação com um id no banco de prod referente ao usuário

deste modo, destinei está DAO para fazer o controle das duas bases de dados ao mesmo tempo (é o certo? não, mas fiz)

'''


class UsuarioDAO:

    def __init__(self, dbAuth, dbProd):
        self.conexaoAuth = dbAuth.conectar()
        self.conexaoProd = dbProd.conectar()

    def commit(self):
        self.conexaoProd.commit()
        self.conexaoAuth.commit()

    def create_user(self, email, senha, nome, sobrenome, status):
        cursorAuth = self.conexaoAuth.cursor()
        # cria o usuário na base de dados de autênticação e retorna o seu id para ser usado abaixo
        cursorAuth.execute(
            'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id;',
            (email, senha)
        )
        usuario_auth_id = cursorAuth.fetchone()[0]
        cursorAuth.close()

        # cria o usuário na base de dados de produção retornando seu ID
        cursorProd = self.conexaoProd.conectar()
        cursorProd.executa_query(
            "INSERT INTO usuario (nome, sobrenome, email, status) VALUES (%s, %s, %s, %s) RETURNING id;",
            (nome, sobrenome, email, status)
        )
        usuario_prod_id = cursorProd.fetchone()[0]

        # utiliza os ids retornados anteriormente para relacionar na tabela que mapeia a BD de autênticação com a de prod
        cursorProd.executa_query(
            "INSERT INTO usuario_auth_map (id_auth, id_usuario) VALUES (%s, %s);",
            (usuario_auth_id, usuario_prod_id)
        )
        cursorProd.close()

        self.commit()

        return {'prod_id': usuario_prod_id, 'auth_id': usuario_auth_id}



    def get_user_auth(self, user_id):
        cursor = self.conexaoAuth.cursor()
        cursor.execute(
            'SELECT email, criado_em FROM users WHERE id = %s;',
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return {'id': user_id, 'email': row[0], 'criado_em': row[1]}
        else:
            return None

    def get_user_prod(self, id):
        cursor = self.conexaoProd.cursor()
        cursor.execute(
            "SELECT id , nome, email, matricula, status, setor FROM (SELECT u.id, u.nome, u.email, u.matricula, "
            "u.status, go.setor_atuacao as setor FROM gestor_ocorrencia as go RIGHT JOIN usuario as u on go.id = u.id "
            "WHERE u.id = %s) as dados_gestor",
            (id,)
        )

        linha = cursor.fetchone()
        cursor.close()
        if linha:
            return {'id': linha[0], 'nome': linha[1], 'email': linha[2], 'matricula': linha[3], 'status': linha[4], 'setor': linha[5]}


    def update_user_auth(self, user_id, email, senha):
        cursor = self.conexaoAuth.cursor()
        cursor.execute(
            'UPDATE users SET email = %s, password = %s WHERE id = %s;',
            (email, senha, user_id)
        )
        self.conexaoAuth.commit()
        cursor.close()

    def update_user_prod(self, id, nome, sobrenome, matricula, email, status):
        cursor = self.conexaoProd.cursor()
        cursor.execute(
            'UPDATE usuario SET nome = %s, sobrenome = %s, matricula = %s, email = %s, status = %s WHERE id = %s;',
            (nome, sobrenome, None, email, status, id)
        )
        self.conexaoProd.commit()
        cursor.close()

    def delete_user(self, user_id):
        cursor = self.conexaoAuth.cursor()
        cursor.execute(
            'DELETE FROM users WHERE id = %s',
            (user_id,)
        )
        self.conexaoAuth.commit()
        cursor.close()

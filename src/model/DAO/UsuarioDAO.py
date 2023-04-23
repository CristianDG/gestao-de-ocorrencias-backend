'''
Criado 14/02 por Victor C.
Classe DAO responsável pelas operação CRUD de usuários

Metódos testados: create, get, delete, update


modificado dia 21/04
Alterei os bancos, de modo a relacionar um id do banco de autênticação com um id no banco de prod referente ao usuário

deste modo, destinei está DAO para fazer o controle das duas bases de dados ao mesmo tempo (é o certo? não, mas fiz)

'''

from tipos import Usuario

class UsuarioDAO:

    def __init__(self, dbAuth, dbProd):
        self.conexaoAuth = dbAuth
        self.conexaoProd = dbProd

    def commit(self):
        self.conexaoProd.commit()
        self.conexaoAuth.commit()

    @staticmethod
    def formarUsuario(usuario):
        return Usuario(
            id_auth=usuario[0],
            id_prod=usuario[1],
            email=usuario[2],
            nome=usuario[3],
            status=usuario[4],
            cargo=usuario[5],
            senha=usuario[6],

        )

    def create_user(self,usuario):
        # cria o usuário na base de dados de autênticação e retorna o seu id para ser usado abaixo
        cursorAuth = self.conexaoAuth.executa_query(
            'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id;',
            (usuario.email, usuario.senha)
        )

        usuario_auth_id = cursorAuth.fetchone()[0]
        cursorAuth.close()

        # cria o usuário na base de dados de produção retornando seu ID
        cursorProd = self.conexaoProd.executa_query(
            "INSERT INTO usuario (nome, sobrenome, email, status) VALUES (%s, %s, %s, %s) RETURNING id;",
            (usuario.nome, usuario.sobrenome, usuario.email, usuario.status)
        )
        usuario_prod_id = cursorProd.fetchone()[0]

        # utiliza os ids retornados anteriormente para relacionar na tabela que mapeia a BD de autênticação com a de prod
        cursorProd.executa_query(
            "INSERT INTO usuario_auth_map (id_auth, id_usuario) VALUES (%s, %s);",
            (usuario_auth_id, usuario_prod_id)
        )
        cursorProd.close()


        return usuario_prod_id



    #retorna o id do banco de autênticação de um usuário do banco de produção
    def get_user_prod_map_auth(self, id):
        cursor = self.conexaoProd.executa_query(
            'SELECT id_auth FROM usuario_auth_map WHERE id_usuario =%s',
            (id,)
        )
        id_auth = cursor.fetchone()[0]
        cursor.close()

        return id_auth

    #retorna o id do banco de produção de um usuário do banco de autênticação
    def get_user_auth_map_prod(self, id):
        cursor = self.conexaoProd.executa_query(
            'SELECT id_usuario FROM usuario_auth_map WHERE id_auth=%s',
            (id,)
        )

        id_prod = cursor.fetchone()[0]
        cursor.close()

        return id_prod

    def get_user_prod(self, id):
        cursor = self.conexaoProd.executa_query(
            "SELECT id , nome, email, matricula, status FROM (SELECT u.id, u.nome, u.email, u.matricula, "
            "u.status, go.setor_atuacao as setor FROM gestor_ocorrencia as go RIGHT JOIN usuario as u on go.id = u.id "
            "WHERE u.id = %s) as dados_gestor",
            (id,)
        )

        linha = cursor.fetchone()
        cursor.close()
        if linha:
            return self.formarUsuario(linha)

    def get_user_auth(self, user_id):
        cursor = self.conexaoAuth.executa_query(
            'SELECT email FROM users WHERE id = %s;',
            (user_id,)
        )

        row = cursor.fetchone()
        cursor.close()
        if row:
            return {'id': user_id, 'email': row[0]}
        else:
            return None


    def update_user(self, usuario):
        self.update_user_auth(usuario.id_auth, usuario.email, usuario.senha)
        self.update_user_prod(usuario.id_prod, usuario.nome, usuario.sobrenome, None, usuario.email, usuario.status)

    def update_user_auth(self, user_id, email, senha):
        cursor = self.conexaoAuth.executa_query(
            'UPDATE users SET email = %s, password = %s WHERE id = %s;',
            (email, senha, user_id)
        )
        cursor.close()

    def update_user_prod(self, id, nome, sobrenome, matricula, email, status):
        cursor = self.conexaoProd.executa_query(
            'UPDATE usuario SET nome = %s, sobrenome = %s, matricula = %s, email = %s, status = %s WHERE id = %s;',
            (nome, sobrenome, None, email, status, id)
        )

        cursor.close()

    def delete_user(self, id_prod):
        cursorAuth = self.conexaoAuth.executa_query(
            'DELETE FROM usuario WHERE id = %s',
            (id_prod,)
        )
        cursorAuth.close()

        cursorProd = self.conexaoProd.executa_query(

        )

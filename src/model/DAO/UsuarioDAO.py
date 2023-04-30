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

    def fechar_conexao(self):
        self.conexaoAuth.fecha_conexao()
        self.conexaoProd.fechar_conexao()

    @staticmethod
    def formarUsuario(usuario):
        return Usuario(**usuario)

    def create_usuario(self, usuario):
        # cria o usuário na base de dados de autênticação e retorna o seu id para ser usado abaixo
        cursorAuth = self.conexaoAuth.executa_query(
            'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id;',
            (usuario.email, usuario.senha)
        )

        usuario_auth_id = cursorAuth.fetchone()['id']
        cursorAuth.close()

        # cria o usuário na base de dados de produção retornando seu ID
        cursorProd = self.conexaoProd.executa_query(
            "INSERT INTO usuario (nome, sobrenome, email, status) VALUES (%s, %s, %s, %s) RETURNING id;",
            (usuario.nome, usuario.sobrenome, usuario.email, usuario.status)
        )
        usuario_prod_id = cursorProd.fetchone()['id']
        cursorProd.close()

        # utiliza os ids retornados anteriormente para relacionar na tabela que mapeia a BD de autênticação com a de prod
        cursorProd = self.conexaoProd.executa_query(
            "INSERT INTO usuario_auth_map (id_auth, id_usuario) VALUES (%s, %s);",
            (usuario_auth_id, usuario_prod_id)
        )
        cursorProd.close()


        return usuario_prod_id




    def get_usuario_prod_map_auth(self, id):#retorna o id do banco de autênticação de um usuário do banco de produção
        cursor = self.conexaoProd.executa_query(
            'SELECT id_auth FROM usuario_auth_map WHERE id_usuario =%s',
            (id,)
        )
        id_auth = cursor.fetchone()['id_auth']
        cursor.close()
        if not id_auth:
            return False

        return id_auth


    def get_usuario_auth_map_prod(self, id):#retorna o id do banco de produção de um usuário do banco de autênticação
        cursor = self.conexaoProd.executa_query(
            'SELECT id_usuario FROM usuario_auth_map WHERE id_auth=%s',
            (id,)
        )

        id_prod = cursor.fetchone()['id_usuario']
        cursor.close()
        if not id_prod:
            return False

        return id_prod

    def get_user_prod(self, id):#retorna um usuário do banco de produção
        cursor = self.conexaoProd.executa_query(
            "SELECT id , nome, sobrenome, email, matricula, status "
            "FROM (SELECT u.id, u.nome, u.sobrenome, u.email, u.matricula, u.status, go.setor_atuacao as setor FROM gestor_ocorrencia as go RIGHT JOIN usuario as u on go.id = u.id "
            "WHERE u.id = %s) as dados_gestor",
            (id,)
        )

        linha = cursor.fetchone()
        cursor.close()
        if not linha:
            return False
        return linha

    def get_user_auth(self, user_id):#retorna um usuário do banco de autênticação
        cursor = self.conexaoAuth.executa_query(
            'SELECT cargo FROM users WHERE id = %s;',
            (user_id,)
        )

        row = cursor.fetchone()
        cursor.close()
        if row:
            return {'id_auth': user_id, 'cargo': row['cargo']} #id_auth, email e cargo respectivamento
        else:
            return None

    def autentica_user(self, email, senha):
        query = """
                SELECT id FROM users
                WHERE email = %s AND password = %s;
                """
        cursor = self.conexaoAuth.executa_query(query, (email, senha))
        result = cursor.fetchone()
        if result:
            user_id = result['id']
            return user_id
        else:
            return None

    def get_user(self, id_prod):#retorna um objeto do tipo usuário que contém as informações dos dois bancos de dados com exceção da senha
        usuario = self.get_user_prod(id_prod)
        usuario_auth = self.get_user_auth(self.get_usuario_prod_map_auth(id_prod))
        if usuario is None or usuario_auth is None:
            return False

        id = usuario['id']
        nome = usuario['nome']
        sobrenome = usuario['sobrenome']
        email = usuario['email']
        status = usuario['status']
        id_auth = usuario_auth['id_auth']
        cargo = usuario_auth['cargo']

        usuario_final = {'id': id, 'nome': nome, 'email': email, 'status': status, 'id_auth': id_auth, 'cargo': cargo, 'sobrenome': sobrenome}

        return self.formarUsuario(usuario_final)

    def update_user_auth(self, usuario):#atualiza os dados de um usuário do banco de autênticação
        cursor = self.conexaoAuth.executa_query(
            'UPDATE users SET email = %s, password = %s WHERE id = %s;',
            (usuario.email, usuario.senha, usuario.id_auth)
        )
        cursor.close()

    def update_user_prod(self, usuario):#atualiza os dados de um usuário do banco de regra de negócio
        cursor = self.conexaoProd.executa_query(
            'UPDATE usuario SET nome = %s, sobrenome = %s, email = %s, status = %s WHERE id = %s RETURNING id;',
            (usuario.nome, usuario.sobrenome, usuario.email, usuario.status, usuario.id_prod)
        )
        id_alterado = cursor.fetchone()['id']
        cursor.close()
        if not id_alterado:
            return False
        return id_alterado

    def update_user(self, usuario):#atualiza os dados de um usuário das duas bases de dados
        id_alterado = self.update_user_prod(usuario)
        if not id_alterado:
            return False
        self.update_user_auth(usuario)

        return id_alterado

    def delete_user(self, id_prod):#deleta um usuário com base no id do banco de produção, deletando das duas bases de dados.
        id_Auth = self.get_usuario_prod_map_auth(id_prod)

        cursorProd = self.conexaoProd.executa_query(
            'DELETE FROM usuario WHERE id =%s',
            (id_Auth,)
        )
        cursorProd.close()

        cursorAuth = self.conexaoAuth.executa_query(
            'DELETE FROM users WHERE id = %s',
            (id_Auth,)
        )
        cursorAuth.close()

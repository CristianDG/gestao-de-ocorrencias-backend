'''
Criado por Victor C 21/4

Classe DAO para manipulação dos gestores
'''


class GestorDAO:

    def __init__(self, dbProd, usuarioDAO):
        self.conexaoProd = dbProd
        self.usuarioDAO = usuarioDAO


    #cria primeiro os dados no banco de autênticação e depois cria no de produção
    #e logo após cria a linha na tabela de gestores
    def create_gestor(self, usuario):

        try:
            id_usuario = self.usuarioDAO.create_usuario(usuario)
        except:
            return False

        cursor = self.conexaoProd.executa_query(
            'INSERT INTO gestor_ocorrencia (id, setor_atuacao) VALUES (%s, %s) RETURNING id;',
            (id_usuario, usuario.setor,)
        )

        id_criado = cursor.fetchone()['id']
        cursor.close()
        if id_criado is None:
            return False
        else:
            return id_criado

    #atualiza os dados do usuário em todas as bases
    def update_gestor(self, id_auth, id_usuario,email, senha, nome, sobrenome, status, setor):
        id_usuario_auth = self.usuarioDAO.update_user_auth(id_auth, email, senha)
        id_usuario_prod = self.usuarioDAO.update_user_prod(id_usuario, nome, sobrenome, None, email, status)

        cursor = self.conexaoProd.executa_query(
            'UPDATE gestor_ocorrencia SET setor_atuacao = %s WHERE id = %s RETURNING id',
            (setor, id_usuario_prod,)
        )

        id_att = cursor.fetchone()['id']
        cursor.close()
        if id_att is None:
            return False
        else:
            return id_att

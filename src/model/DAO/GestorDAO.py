'''
Criado por Victor C 21/4

Classe DAO para manipulação dos gestores
'''

from ...tipos import Usuario

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
    def update_gestor(self, usuario):
        id_usuario_auth = self.usuarioDAO.update_user_auth(usuario.id_auth, usuario.email, usuario.senha)
        id_usuario_prod = self.usuarioDAO.update_user_prod(usuario.id, usuario.nome, usuario.sobrenome, usuario.matricula, usuario.email, usuario.status)

        cursor = self.conexaoProd.executa_query(
            'UPDATE gestor_ocorrencia SET setor_atuacao = %s WHERE id = %s RETURNING id',
            (usuario.setor, id_usuario_prod,)
        )

        id_att = cursor.fetchone()['id']
        cursor.close()
        if id_att is None:
            return False
        else:
            return id_att


    def get_gestores(self):
        cursor = self.conexaoProd.executa_query(
            "SELECT id , nome, sobrenome, email, matricula, status, setor_atuacao as setor"
            "FROM (SELECT u.id, u.nome, u.sobrenome, u.email, u.matricula, u.status, go.setor_atuacao as setor FROM gestor_ocorrencia as go RIGHT JOIN usuario as u on go.id = u.id "
            ") as dados_gestor"
        )

        resultado = cursor.fetchall()
        cursor.close()
        gestores = []

        if not resultado:
            return False

        for gestor in resultado:
            gestores.append(self.usuarioDAO.formarUsuario(gestor))
        return gestores
'''
Criado por Victor C 21/04
Classe destinada para manipular os setor

'''

from tipos import Setor


class SetorDAO:
    def __init__(self, dbProd):
        self.conexaoProd = dbProd

    def fechar_conexao(self):
        self.conexaoProd.fechar_conexao()

    @staticmethod
    def formar_setor(setor):
        print(setor)
        return Setor(
            id=setor['id'],
            nome=setor['nome'],
            descricao=setor['desc_responsabilidades'],
            status=setor['status'],
        )

    def create_setor(self, setor):
        cursor = self.conexaoProd.executa_query(
            'INSERT INTO setor (nome, desc_responsabilidades, status) VALUES (%s, %s, %s) RETURNING id;',
            (setor.nome, setor.descricao, setor.status,)
        )

        id_setor = cursor.fetchone()[0]
        cursor.close()
        return id_setor

    def update_setor(self, setor):
        cursor = self.conexaoProd.executa_query(
            'UPDATE setor SET nome=%s, desc_responsabilidades=%s, status=%s WHERE id=%s RETURNING id',
            (setor.nome, setor.descricao, setor.status, setor.id,)
        )

        id_setor = cursor.fetchone()[0]
        cursor.close()

        return id_setor

    def get_setores(self):
        cursor = self.conexaoProd.executa_query(
            'SELECT * FROM setor;', ()
        )

        setores = []

        resultado_query = cursor.fetchall()

        for setor in resultado_query:
            setores.append(self.formar_setor(setor))
        cursor.close()
        return setores

    def get_setor_por_id(self, id):
        cursor = self.conexaoProd.executa_query(
            'SELECT * FROM setor WHERE id=%s;', (id,))

        setor = self.formar_setor(cursor.fetchone())
        cursor.close()

        return setor

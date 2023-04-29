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
        return Setor(**setor)

    def create_setor(self, setor):
        cursor = self.conexaoProd.executa_query(
            'INSERT INTO setor (nome, desc_responsabilidades, status) VALUES (%s, %s, %s) RETURNING id;',
            (setor.nome, setor.desc_responsabilidades, setor.status,)
        )

        id_setor = cursor.fetchone()['id']
        cursor.close()
        return id_setor

    def update_setor(self, setor):
        cursor = self.conexaoProd.executa_query(
            'UPDATE setor SET nome=%s, desc_responsabilidades=%s, status=%s WHERE id=%s RETURNING id',
            (setor.nome, setor.desc_responsabilidades, setor.status, setor.id,)
        )

        id_setor = cursor.fetchone()['id']
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

    def get_id_setor(self, id_problema):
        cursor = self.conexaoProd.executa_query(
            'SELECT id_setor FROM problema WHERE id=%s',
            (id_problema,)
        )

        id_setor = cursor.fetchone()['id_setor']
        cursor.close()
        return id_setor

    def get_id_problemas(self, id_setor):
        cursor = self.conexaoProd.executa_query(
            'SELECT id_problema FROM problema WHERE id_setor=%s',
            (id_setor,)
        )
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def get_problemas(self):
        cursor = self.conexaoProd.executa_query('SELECT id, nome FROM problema')
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

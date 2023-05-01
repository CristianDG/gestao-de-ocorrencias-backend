'''
Criado por Victor C 21/04
Classe destinada para manipular os setor

'''

from tipos import Setor, Problema


class SetorDAO:
    def __init__(self, dbProd):
        self.conexaoProd = dbProd

    def fechar_conexao(self):
        self.conexaoProd.fechar_conexao()

    @staticmethod
    def formar_setor(setor):
        return Setor(**setor)

    @staticmethod
    def formar_problema(problema):
        return Problema(**problema)

    def create_setor(self, setor):
        cursor = self.conexaoProd.executa_query(
            'INSERT INTO setor (nome, desc_responsabilidades, status) VALUES (%s, %s, %s) RETURNING id;',
            (setor.nome, setor.desc_responsabilidades, setor.status,)
        )

        id_setor = cursor.fetchone()['id']
        cursor.close()
        if id_setor is None:
            return False
        return id_setor

    def update_setor(self, setor):
        cursor = self.conexaoProd.executa_query(
            'UPDATE setor SET nome=%s, desc_responsabilidades=%s, status=%s WHERE id=%s RETURNING id',
            (setor.nome, setor.desc_responsabilidades, setor.status, setor.id,)
        )

        id_setor = cursor.fetchone()['id']
        cursor.close()
        if id_setor is None:
            return False
        return id_setor

    def get_setores(self):
        cursor = self.conexaoProd.executa_query(
            'SELECT * FROM setor;', ()
        )

        setores = []

        resultado_query = cursor.fetchall()
        if resultado_query is None:
            return False

        for setor in resultado_query:
            setores.append(self.formar_setor(setor))
        cursor.close()
        return setores

    def get_setor_por_id(self, id):
        cursor = self.conexaoProd.executa_query(
            'SELECT * FROM setor WHERE id=%s;', (id,))

        setor = self.formar_setor(cursor.fetchone())
        cursor.close()
        if setor is None:
            return False

        return setor

    def get_id_setor(self, id_problema):
        cursor = self.conexaoProd.executa_query(
            'SELECT id_setor FROM problema WHERE id=%s',
            (id_problema,)
        )

        id_setor = cursor.fetchone()['id_setor']
        cursor.close()
        if id_setor is None:
            return False
        return id_setor

    def create_problema(self, problema):
        cursor = self.conexaoProd.executa_query(
            'INSERT INTO problema (nome, id_setor) VALUES (%s, %s) RETURNING id',
            (problema.nome, problema.id_setor,)
        )
        id_problema_criado = cursor.fetchone()['id']
        cursor.close()
        if not id_problema_criado:
            return False
        else:
            return id_problema_criado


    def update_problema(self, problema):
        cursor = self.conexaoProd.executa_query(
            'UPDATE problema SET nome=%s, id_setor =%s WHERE id=%s',
            (problema.nome, problema.id_setor, problema.id)
        )
        return problema.id


    def get_id_problemas(self, id_setor):
        cursor = self.conexaoProd.executa_query(
            'SELECT id, nome, id_setor from problema WHERE id_setor = %s',
            (id_setor,)
        )
        resultados = cursor.fetchall()
        cursor.close()

        if resultados is None:
            return False

        problemas = []
        for problema in resultados:
            problemas.append(self.formar_problema(problema))
        return problemas

    def get_problemas(self):
        cursor = self.conexaoProd.executa_query("SELECT * FROM problema WHERE nome != ''")
        resultado = cursor.fetchall()
        cursor.close()
        problemas = []
        if resultado is None:
            return False
        for problema in resultado:
            problemas.append(self.formar_problema(problema))

        return problemas

'''
Criado por Victor C 21/04
Classe destinada para manipular os setor

'''

class SetorDAO:
    def __init__(self, dbProd):
        self.conexaoProd = dbProd


    def create_setor(self, nome, descricao, status):
        cursor = self.conexaoProd.executa_query(
            'INSERT INTO setor (nome, desc_responsabilidades, status) VALUES (%s, %s, %s) RETURNING id;',
            (nome, descricao, status,)
        )

        id_setor = cursor.fetchone()[0]
        cursor.close()
        return id_setor

    def update_setor(self, id, nome, descricao, status):
        print(status)
        cursor = self.conexaoProd.executa_query(
            'UPDATE setor SET nome=%s, desc_responsabilidades=%s, status=%s WHERE id=%s RETURNING id',
            (nome, descricao, status, id,)
        )

        id_setor = cursor.fetchone()[0]
        cursor.close()

        return id_setor

    def get_setores(self):
        cursor = self.conexaoProd.executa_query(
            'SELECT * FROM setor;', ()
        )

        setores = cursor.fetchall()
        cursor.close()
        return setores

    def get_setor_by_id(self, id):
        cursor = self.conexaoProd.executa_query(
            'SELECT * FROM setor WHERE id=%s;', (id,)
        )

        setores = cursor.fetchone()
        cursor.close()
        return setores

'''
Feito por Victor c.

Classe responsável por adquirir os dados necessários para a montagem do dashboard utilizada na aplicação
'''

class DashboardDAO:

    def __init__(self, conexaoProd):
        self.conexao = conexaoProd


    def get_ocorrencias_criadas_hoje(self):
        cursor = self.conexao.executa_query(
            """SELECT COUNT(*) AS num_ocorrencias_cadastradas_hoje
            FROM reportify.ocorrencia
            WHERE date_trunc('day', data_criacao) = date_trunc('day', CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo');
            """, ())

        resultado = cursor.fetchone()['num_ocorrencias_cadastradas_hoje']
        cursor.close()
        if resultado is None:
            return False
        return resultado

    # retorna a quantidade total de ocorrências resolvidas e invalidas
    # o objeto de retorno é um dicionário do tipo {'num_ocorerncias_invalidadas': int, 'num_ocorerncias_resolvidas': int}
    def get_ocorrencias_validas_invalidas(self):
        cursor = self.conexao.executa_query("""
            SELECT
              COUNT(*) FILTER (WHERE status = 'invalida') AS num_ocorrencias_invalidadas,
              COUNT(*) FILTER (WHERE status = 'solucionada') AS num_ocorrencias_resolvidas
            FROM ocorrencia;
        """, ())

        resultado = cursor.fetchone()
        cursor.close()
        if not resultado:
            return False
        return resultado


    '''
    Retorna a quantidade de ocorrencias registradas nos ultimos 12
    os objetos de retorno são dicionários no modelo {'mes': timestamp, 'num_ocorrencias_cadastradas': int}
    '''
    def get_ocorrencias_cadastradas_12meses(self):
        cursor = self.conexao.executa_query("""
            SELECT
                DATE_TRUNC('month', data_criacao) AS mes,
                COUNT(*) AS num_ocorrencias_cadastradas
            FROM reportify.ocorrencia
            WHERE data_criacao >= date_trunc('month', CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo') - INTERVAL '12 months'
            GROUP BY DATE_TRUNC('month', data_criacao)
            ORDER BY DATE_TRUNC('month', data_criacao);
        """,
            ()
        )

        resultado = cursor.fetchall()
        cursor.close()
        if not resultado:
            return False
        return resultado

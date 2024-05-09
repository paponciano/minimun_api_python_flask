import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LOCALHOST;'
                      'Database=FATURAMENTO;'
                      'UID=sa;'
                      'PWD=sa;')

cursor = conn.cursor()


class Faturamento(object):
    def lerFaturamentos(self):
        listaDadosFaturamento = []

        cursor.execute("SELECT TOP 100 ID, DATA, COD_ORCAMENTO, COD_PROJETO, FATURAMENTO FROM DADOS_FATURAMENTO")

        for item in cursor.fetchall():
            dic = {"ID": str(item[0]), "DATA": str(item[1]), "COD_ORCAMENTO": str(item[2]),
                   "COD_PROJETO": str(item[3]), "FATURAMENTO": str(item[4])}

            listaDadosFaturamento.append(dic)

        return listaDadosFaturamento

    def lerFaturamento(self, id):
        listaDadosFaturamento = []

        cursor.execute("SELECT ID, DATA, COD_ORCAMENTO, COD_PROJETO, FATURAMENTO FROM DADOS_FATURAMENTO WHERE ID = ?", id)

        for item in cursor.fetchall():
            dic = {"ID": str(item[0]), "DATA": str(item[1]), "COD_ORCAMENTO": str(item[2]),
                   "COD_PROJETO": str(item[3]), "FATURAMENTO": str(item[4])}

            listaDadosFaturamento.append(dic)

        return listaDadosFaturamento

    def incluirFaturamento(self):
        cursor.execute("INSERT INTO DADOS_FATURAMENTO VALUES (?, ?, ?, ?)",
                       self.Data, self.CodOrcamento,
                       self.CodProjeto, self.Faturamento)

        conn.commit()

    def atualizarFaturamento(self, id):
        cursor.execute("UPDATE DADOS_FATURAMENTO SET DATA = ?, COD_ORCAMENTO = ?, COD_PROJETO = ?, FATURAMENTO = ? WHERE ID = ?",
                       self.Data, self.CodOrcamento,
                       self.CodProjeto, self.Faturamento, id)

        conn.commit()

    def apagarFaturamento(self, id):
        cursor.execute("DELETE FROM DADOS_FATURAMENTO WHERE ID = ?", id)

        conn.commit()

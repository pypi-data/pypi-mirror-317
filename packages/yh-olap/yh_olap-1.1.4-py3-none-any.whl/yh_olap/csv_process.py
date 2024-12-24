import os
import pandas as pd


class Csv:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.csv_file_name = os.path.basename(self.csv_file)
        self.csv_file_name_without_ext = os.path.splitext(self.csv_file_name)[0]
        self.cols = []
        self.df = pd.read_csv(self.csv_file, dtype=str)
        self.cols = self.df.columns.values

    def get_create_table_sql(self, table_name=None, dorp_table=True):
        if not table_name:
            table_name = self.csv_file_name_without_ext
        sql = ''
        drop_sql = 'drop table if exists %s;\n' % table_name
        if dorp_table:
            sql = sql + drop_sql
        col_sql = ','.join([i + ' string' for i in self.cols])
        create_sql = "CREATE table if not exists %s \n(%s);\n" % (
            table_name, col_sql)
        sql = sql + create_sql
        return sql

    def get_insert_sql(self, table_name=None, truncate=True, code_len=60000):
        if not table_name:
            table_name = self.csv_file_name_without_ext
        sql = ''
        truncate_sql = 'truncate table %s;\n' % table_name
        if truncate:
            sql = sql + truncate_sql
        insert_sql = "insert into %s values" % table_name
        insert_sql_code_len = len(insert_sql.encode())
        insert_values = []
        for row in self.df.iterrows():
            vals = "'" + "','".join([str(i) for i in row[1].values]) + "'"
            insert_values.append("(%s)\n" % vals)
        para_code_len = insert_sql_code_len
        para = []
        for i in insert_values:
            row_code_len = len(i.encode()) + 1
            para_code_len = para_code_len + row_code_len
            if para_code_len >= code_len:
                para_sql = insert_sql + ','.join(para) + ";"
                sql = sql + para_sql
                para = [i]
                para_code_len = insert_sql_code_len + row_code_len
            else:
                para.append(i)
        if para:
            para_sql = insert_sql + ','.join(para) + ";"
            sql = sql + para_sql
        return sql

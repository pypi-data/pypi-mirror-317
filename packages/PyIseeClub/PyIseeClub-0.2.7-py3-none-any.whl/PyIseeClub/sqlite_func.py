# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, text


def insert_(sqlite_path, df, table_name):
    try:
        if not df.empty:
            # Create SQLAlchemy engine
            engine = create_engine(f'sqlite:///{sqlite_path}', echo=True)
            # Use pandas to_sql method to insert data
            df.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=1000, method='multi')
            return 'Data inserted successfully'
        else:
            return f"{table_name} is None"
    except Exception as e:
        return f"Error inserting data: {e}"


def delete_(sqlite_path, table_name, condition=None):
    try:
        # Create SQLAlchemy engine
        engine = create_engine(f'sqlite:///{sqlite_path}', echo=True)

        with engine.connect() as connection:
            # 如果提供了条件，则构建删除语句
            if condition:
                delete_statement = text(f"DELETE FROM {table_name} WHERE {condition}")
            else:
                delete_statement = text(f"DELETE FROM {table_name}")

            # 执行删除语句
            result = connection.execute(delete_statement)

        return f"{result.rowcount} rows deleted successfully"
    except Exception as e:
        return f"Error deleting data: {e}"

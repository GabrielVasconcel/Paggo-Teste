from datetime import datetime
import os
import pandas as pd
import httpx
import numpy as np
from sqlalchemy import create_engine

# alterar depois para pegar do docker-compose
API_URL = os.getenv("API_URL", "http://api_fonte:8000/data/")
DATABASE_URL_ALVO = os.getenv("DATABASE_URL", "postgresql://user:password@db_alvo:5432/alvo")


def run_etl(data_consulta, colunas):
    data_consulta = datetime.strptime(data_consulta, "%d-%m-%Y")
    data_inicio = data_consulta.replace(hour=0, minute=0, second=0)
    data_fim = data_consulta.replace(hour=23, minute=59, second=59)

    params = [
        ("inicio", data_inicio.isoformat()),
        ("fim", data_fim.isoformat())
    ] + [("colunas", col) for col in colunas]


    response = httpx.get(url=API_URL, params=params)
    response.raise_for_status()  
    dados = response.json() # retorna os dados para o dia, e colunas informadas

    dados = pd.DataFrame(dados) # converte para dataframe
    dados["timestamp"] = pd.to_datetime(dados["timestamp"]) # converte a coluna timestamp para datetime

    dados.set_index("timestamp", inplace=True) # define a coluna timestamp como index
    resultado = []

    for coluna in colunas:
        # agrega em grupos de 10 minutos 
        agregados = dados[[coluna]].resample("10min").agg(["mean", "min", "max", "std"])
        agregados.columns = [f"{agg[0]}_{agg[1]}" for agg in agregados.columns]
        agregados["data"] = agregados.index.date
        agregados["timestamp"] = agregados.index.time

        agregados_long = pd.melt(agregados, id_vars=["data", "timestamp"], var_name="name", value_name="value")
        resultado.append(agregados_long)

    resultado = pd.concat(resultado, ignore_index=True) # concatena os dataframes em um 
    # criando o signal_id para name
    signal_map = {}
    idx = 0
    for name in ["wind_speed", "power", "ambient_temperature"]:
        for agregador in ["mean", "min", "max", "std"]:
            signal_map[f"{name}_{agregador}"] = idx
            idx += 1 
    resultado["signal_id"] = resultado["name"].map(signal_map)
    resultado["signal_id"] = resultado["signal_id"].astype("Int64") 

    engine = create_engine(DATABASE_URL_ALVO) # cria a engine para conectar ao banco de dados alvo
    resultado.to_sql("signal", engine, if_exists="append", index=False) # insere os dados no banco de dados



if __name__ == "__main__":
    import sys
    dia = sys.argv[1]
    colunas = sys.argv[2:]
    run_etl(dia, colunas)
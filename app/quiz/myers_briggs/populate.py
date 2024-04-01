import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2


def __get_cxn():
    load_dotenv()
    env = os.environ
    cnxn = psycopg2.connect(
        dbname=env.get("DB_NAME"),
        user=env.get("DB_USER"),
        password=env.get("DB_PASS"),
        host=env.get("DB_HOST"),
        port=env.get("DB_PORT")
    )

    return cnxn


def load_personaTypes():
    cnxn = __get_cxn()
    data = pd.read_csv("16_types.csv")
    for row in data.itertuples():
        cursor = cnxn.cursor()
        query = (f"INSERT INTO public.quiz_personalitytype (combo, name, describe) "
                 f"VALUES('{row.combo}', '{row.name}', '{row.describe}');")
        cursor.execute(query)
        cnxn.commit()
        cursor.close()
    cnxn.close()

    return True


def load_persona():
    cnxn = __get_cxn()
    data = pd.read_csv("personalities.csv")
    for row in data.itertuples():
        cursor = cnxn.cursor()
        query = (f"INSERT INTO public.quiz_personality (name, abbrv, dichotomy, describe) "
                 f"VALUES('{row.name}', '{row.abbrv}', '{row.dichotomy}', '{row.describe}');")
        cursor.execute(query)
        cnxn.commit()
        cursor.close()
    cnxn.close()

    return True


def load_question():
    cnxn = __get_cxn()
    data = pd.read_csv("questions.csv")
    for row in data.itertuples():
        cursor = cnxn.cursor()
        query = (f"INSERT INTO public.quiz_question (count, dichotomy, text) "
                 f"VALUES({int(row.count)}, '{row.dichotomy}', '{row.text}');")
        cursor.execute(query)
        cnxn.commit()
        cursor.close()
    cnxn.close()

    return True


if __name__ == "__main__":
    if load_persona() and load_personaTypes() and load_question():
        print("The Myers-Briggs information has been successfully loaded.")

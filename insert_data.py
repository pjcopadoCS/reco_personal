import pandas as pd
from flask import Flask
from models import Food, Grape, Wine, User, db, Compras
from constants import translation_dict
from werkzeug.security import generate_password_hash, check_password_hash

df = pd.read_excel('wines_dataset.xlsx')
purchases = pd.read_excel('purchases_dataset.xlsx')
users = pd.read_excel('users_dataset.xlsx')

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

def clean(text):
    cleaned_text = text.replace('\xa0', ' ')
    return cleaned_text

def translate_to_catalan(original_name):
    return translation_dict.get(original_name, original_name)

def delete_all(table):
    with app.app_context():
        db.session.query(table).delete()
        db.session.commit()
        print(f'All {table} objects deleted from database')

def create_wine(row, grapes, foods):
    code = row['code']
    name = row['title']
    category = row['category']
    category = translate_to_catalan(category)
    taste = row['type'] if not pd.isna(row['type']) else None
    taste = translate_to_catalan(taste) 
    country = row['country']
    country = translate_to_catalan(country)
    region = row['winery_region'] if not pd.isna(row['winery_region']) else None
    den_origin = row['denomination_of_origin'] if not pd.isna(row['denomination_of_origin']) else None
    year = row['seniority'] if not pd.isna(row['seniority']) else None
    alcohol = row['percentage_of_alcohol']
    price =  round(row['price'], 2)
    fruity_spicy = row['afrutado_especiado'] if not pd.isna(row['afrutado_especiado']) else None
    young_barrel = row['joven_crianza'] if not pd.isna(row['joven_crianza']) else None
    light_body = row['ligero_corpulento'] if not pd.isna(row['ligero_corpulento']) else None

    return Wine(
        code=code, name=name, category=category, year=year, 
        country=country, region=region, den_origin=den_origin,
        taste=taste, alcohol=alcohol, price=price,
        fruity_spicy=fruity_spicy, young_barrel=young_barrel,
        light_body=light_body, 
        grapes=grapes, foods=foods,
    )

def get_food_list(row, translation_cache, food_cache):
    foods = row['general_pairings'].split(', ')
    food_list = []
    for food_name in foods:
        if food_name in translation_cache:
            translated_food = translation_cache[food_name]
        else:
            translated_food = translate_to_catalan(food_name)
            translation_cache[food_name] = translated_food
        
        if translated_food != 'nan':
            if translated_food in food_cache:
                food = food_cache[translated_food]
            else:
                food = Food.query.filter_by(name=translated_food).first()
                if not food:
                    food = Food(name=translated_food)
                food_cache[translated_food] = food
            food_list.append(food)
    return food_list

def get_grape_list(row, grape_cache):
    grapes = row['variety'].split(', ')
    grape_list = []
    for grape_name in grapes:
        if grape_name != 'nan':
            if grape_name in grape_cache:
                grape = grape_cache[grape_name]
            else:
                grape = Grape.query.filter_by(name=grape_name).first()
                if not grape:
                    grape = Grape(name=grape_name)
                grape_cache[grape_name] = grape
            grape_list.append(grape)
    return grape_list

def insert_wines():
    df['variety'] = df['variety'].astype(str)
    df['variety'] = df['variety'].apply(clean)
    df['general_pairings'] = df['general_pairings'].astype(str)
    df['general_pairings'] = df['general_pairings'].apply(clean)

    translation_cache = {}
    food_cache = {}
    grape_cache = {}

    with app.app_context():
        for index, row in df.iterrows():
            grapes = get_grape_list(row, grape_cache)
            foods = get_food_list(row, translation_cache, food_cache)
                
            wine = create_wine(row, grapes, foods)
            db.session.add(wine)

            if (index + 1) % 100 == 0:  # Commit after every 100 rows
                db.session.commit()

            progress = round(index / len(df) * 100)
            if progress % 5 == 0:
                print(f'{progress}%')
        
        db.session.commit()  # Final commit for remaining rows


def print_values(column_name):
    unique_values = df[column_name].unique()
    print(f"Valors únics de la columna '{column_name}':")
    for value in unique_values:
        print(value)


def print_info():
    # Mostra un resum concís del DataFrame, incloent informació sobre índex, columnes, tipus de dades 
    # i memòria utilitzada.
    print(df.info()) 
    # Comprobar els tipus de dades de cada columna del DataFrame.
    print(df.dtypes) 
    # Mostra les primeres files del DataFrame per proporcionar una vista prèvia dels seus continguts.
    print(df.head())  
    # Proporciona estadístiques descriptives per a les columnes numèriques del DataFrame, com la mitjana, 
    # la desviació estàndard, el valor mínim, els quartils i el valor màxim.
    print(df.describe())

def create_user(row):
    return User(username=row['username'],
                password=generate_password_hash(row['password']),
                has_answered=bool(row['has_answered']))

def insert_users():
    # introduce users into the database
    with app.app_context():
        for index, row in users.iterrows():
            user = create_user(row)
            db.session.add(user)
        db.session.commit()


# class Purchases(db.Model):
#     __tablename__ = 'purchasess'
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
#     wine_id = Column(Integer, ForeignKey('wines.id', ondelete='CASCADE'), primary_key=True)

def create_purchase(row):
    user = db.session.query(User).filter(User.username == row['username']).first()
    wine = db.session.query(Wine).filter(Wine.code == row['code']).first()
    return Compras(user_id=user.id,
                   o_user_id=user.id,
                   code = wine.code,
                   wine_id=wine.id,
                   o_wine_id=wine.id,
                   username=user.username)
    #return purchase(user_id=row['user_id'], wine_id=row['wine_id'])

def insert_purchases():
    # introduce purchases into the database
    with app.app_context():
        for index, row in purchases.iterrows():
            Compra = create_purchase(row)
            db.session.add(Compra)

        db.session.commit()


if __name__ == "__main__":
    print_info()
    insert_wines()
    insert_users()
    insert_purchases()

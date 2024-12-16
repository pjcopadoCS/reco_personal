# Recomanador personalitzat de vins

## Descripció
El Recomanador personalitzat de vins és una aplicació que ajuda els usuaris a trobar vins que s'adeqüin al seu perfil fent el nombre de preguntes necessàries per obtenir tot d'informació detallada de l'usuari. Utilitzant tècniques de filtratge basat en contingut, coneixement expert amb regles específiques i una gestió avançada dels usuaris a través d'una base de dades, l'aplicació pot oferir suggeriments de vins altament personalitzats que s'ajustin als gustos i criteris específics dels usuaris.

Podeu accedir al recomanador utilitzant aquest enllaç: https://api-recomanador-personalitzat.onrender.com

## Instal·lació local

### Requisits
- Python 3.8+

### Passos
#### 1. Clona el repositori:
```bash
git clone https://github.com/pol-fradera/api_recomanador_personalitzat.git
cd api_recomanador
```

#### 2. Crea un entorn virtual:
```bash
python -m venv venv
.\venv\Scripts\activate 
```

#### 3. Instal·la les dependències:
```bash
pip install -r requirements.txt
```

## Execució local
### 1. Crea un fitxer .env i configura les variables d'entorn següents:
- SECRET_KEY = \<qualsevol valor>
- SQLALCHEMY_DATABASE_URI = \<URI de la teva base de dades>
- SQLALCHEMY_TRACK_MODIFICATIONS = \<False>

### 2. Crea les taules a la teva base de dades:
```bash
py ./create_db.py
```

### 3. Insereix les dades dels vins a la base de dades:
```bash
py ./insert_data.py
```

### 4. Executa l'aplicació:
```bash
py ./app.py
```

### 5. Obre el navegador i ves a http://localhost:5000.


## Autor
- Pol Fradera Insa - [GitHub](https://github.com/pol-fradera)


## Informació addicional

#### Actualitzar les llibreries ja instalades
```bash
pip install --upgrade -r requirements.txt
```

#### Actualizar el fitxer de depèndencies amb les llibreries instalades
```bash
pip freeze > requirements.txt
```

#### Gestionar migracions
```bash
flask --app create_db.py db init
flask --app create_db.py db migrate -m "Add gender column to users_info"
flask --app create_db.py db upgrade
```
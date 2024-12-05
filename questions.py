from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from constants import Category
from constants import Profile as ProfileEnum

from models import Profile, Grape, Food, UserInfo, Wine, db
from utils import (
    country_filter_by_profile, delete_session_info, 
    user_variety_filter,
    get_ranges, has_profile, get_options,
    price_filter_by_profile, variety_filter_by_profile,
)

questions_bp = Blueprint('questions', __name__)

QUESTION_TEMPLATE = 'checkbox_question.html'
QUESTION_1 = 'questions.recom_question1'
QUESTION_TASTE = 'questions.recom_question_taste'
QUESTION_RANGE = 'questions.recom_question_range'
QUESTION_PRICE = 'questions.recom_question_price'
QUESTION_ALCOHOL = 'questions.recom_question_alcohol'
QUESTION_COUNTRY = 'questions.recom_question_country'
QUESTION_REGION = 'questions.recom_question_region'
QUESTION_DEN_ORIGIN = 'questions.recom_question_den_origin'
QUESTION_YEAR = 'questions.recom_question_year'
QUESTION_GRAPE = 'questions.recom_question_grape'
QUESTION_FOOD = 'questions.recom_question_food'
RESULT = 'questions.result'

QUESTION_ROUTES = [
    '0',
    QUESTION_1,
    QUESTION_TASTE,
    QUESTION_RANGE,
    QUESTION_PRICE,
    QUESTION_ALCOHOL,
    QUESTION_COUNTRY,
    QUESTION_REGION,
    QUESTION_DEN_ORIGIN,
    QUESTION_YEAR,
    QUESTION_GRAPE,
    QUESTION_FOOD,
    RESULT
]


def get_next_question(current_question):
    try:
        current_index = QUESTION_ROUTES.index(current_question)
        return QUESTION_ROUTES[current_index + 1]
    except (ValueError, IndexError):
        return 'questions.result'


@questions_bp.route('/initial_questions', methods=['GET', 'POST'])
@login_required
def initial_questions():
    if current_user.has_answered:
        return redirect(url_for('home'))
    if request.method == 'POST':
        current_user.has_answered = True
        gender = request.form.get('question1')
        age = request.form.get('question2')

        profiles = request.form.getlist('question3')
        profiles_list = []
        for profile in profiles:
            profile_obj = Profile.query.filter_by(name=profile).first()
            if not profile_obj:
                profile_obj = Profile(name=profile)
            profiles_list.append(profile_obj)

        user_info = UserInfo(user_id=current_user.id, gender=gender, age=age, profiles=profiles_list)
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('initial_questions.html')


@questions_bp.route('/recom_question1', methods=['GET', 'POST'])
@login_required
def recom_question1():
    if request.method == 'GET':
        delete_session_info()
        categories = [category.value for category in Category]
        return render_template(
            QUESTION_TEMPLATE, 
            title='Pregunta 1/11',
            question='Estàs pensant en una categoria de vi específica?',
            values=categories,
        )
    elif request.method == 'POST':
        if 'skip' in request.form:
            wines = Wine.query.filter(~Wine.users.any(id=current_user.id)).all()
            session['filtered_wines'] = [wine.id for wine in wines]
            return redirect(url_for(get_next_question(QUESTION_1)))
        answer = request.form.getlist('question')
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_1))
       
        filtered_wines = (
            Wine.query.filter(~Wine.users.any(id=current_user.id))
            .filter(Wine.category.in_(answer)).all()
        )
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_1]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_1)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_taste', methods=['GET', 'POST'])
@login_required
def recom_question_taste():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        tastes = get_options('taste', filtered_wine_ids)
        
        if len(tastes) <= 1:
            return redirect(url_for(get_next_question(QUESTION_TASTE)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_TASTE)}/11',
            question="Quin tipus de vi t'agrada?",
            values=tastes
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_TASTE)))
        answer = request.form.getlist('question')
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_TASTE))
        
        filtered_wines = Wine.query.filter(Wine.id.in_(session['filtered_wines']),
                                            Wine.taste.in_(answer)).all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_TASTE]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_TASTE)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_range', methods=['GET', 'POST'])
@login_required
def recom_question_range():
    if request.method == 'GET':
        return render_template(
            'range_question.html', 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_RANGE)}/11',
            question="Defineix les característiques que més t'agraden del vi",
        )
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_RANGE)))

        aroma = int(request.form.get('Aroma'))
        ripening = int(request.form.get('Ripening'))
        body = int(request.form.get('Body'))

        target_values = {
            0: (0, 2),  # valors propers a 0
            1: (3, 7),  # valors propers a 5
            2: (8, 10)  # valors propers a 10
        }

        aroma_range = target_values[aroma]
        ripening_range = target_values[ripening]
        body_range = target_values[body]
        
        filtered_wines = Wine.query.filter(
            Wine.id.in_(session['filtered_wines']),
            Wine.fruity_spicy.between(aroma_range[0], aroma_range[1]),
            Wine.young_barrel.between(ripening_range[0], ripening_range[1]),
            Wine.light_body.between(body_range[0], body_range[1])
        ).all()

        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_RANGE]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_RANGE)))
        else:
            return redirect(url_for(RESULT))    


@questions_bp.route('/recom_question_price', methods=['GET', 'POST'])
@login_required
def recom_question_price():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        available_ranges = get_ranges('price', filtered_wine_ids)
    
        formatted_ranges = [f"{r[0]}€ - {r[1]}€" for r in available_ranges]
        if len(formatted_ranges) <= 1:
            return redirect(url_for(get_next_question(QUESTION_PRICE)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_PRICE)}/11',
            question="En quin rang de preu vols que t'ofereixi recomanació?",
            values=formatted_ranges
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_PRICE)))
        price_ranges = request.form.getlist('question')
        if not price_ranges:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_PRICE))
        
        parsed_ranges = []
        
        for r in price_ranges:
            start, end = map(int, r.replace('€', '').split(' - '))
            parsed_ranges.append((start, end))
            
        filtered_wine_ids = session.get('filtered_wines', [])

        filtered_wines_query = Wine.query.filter(Wine.id.in_(filtered_wine_ids))
        wine_conditions = [Wine.price.between(start, end) for start, end in parsed_ranges]

        if wine_conditions:
            filtered_wines_query = filtered_wines_query.filter(or_(*wine_conditions))

        filtered_wines = filtered_wines_query.all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_PRICE]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_PRICE)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_alcohol', methods=['GET', 'POST'])
@login_required
def recom_question_alcohol():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        available_ranges = available_ranges = get_ranges('alcohol', filtered_wine_ids)

        formatted_ranges = [f"{r[0]}% - {r[1]}%" for r in available_ranges]
        if len(formatted_ranges) <= 1:
            return redirect(url_for(get_next_question(QUESTION_ALCOHOL)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_ALCOHOL)}/11',
            question="Quin grau d'alcohol prefereixes?",
            values=formatted_ranges
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_ALCOHOL)))
        alcohol_ranges = request.form.getlist('question')
        if not alcohol_ranges:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_ALCOHOL))
        
        parsed_ranges = []
        for r in alcohol_ranges:
            start, end = map(int, r.replace('%', '').split(' - '))
            parsed_ranges.append((start, end))

        filtered_wine_ids = session.get('filtered_wines', [])

        filtered_wines_query = Wine.query.filter(Wine.id.in_(filtered_wine_ids))
        wine_conditions = [Wine.alcohol.between(start, end) for start, end in parsed_ranges]

        if wine_conditions:
            filtered_wines_query = filtered_wines_query.filter(or_(*wine_conditions))

        filtered_wines = filtered_wines_query.all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_ALCOHOL]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_ALCOHOL)))
        else:
            return redirect(url_for(RESULT))
        

@questions_bp.route('/recom_question_country', methods=['GET', 'POST'])
@login_required
def recom_question_country():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        countries = get_options('country', filtered_wine_ids)

        if len(countries) <= 1:
            return redirect(url_for(get_next_question(QUESTION_COUNTRY)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_COUNTRY)}/11',
            question="Tens preferència per algun país concret?",
            values=countries
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_COUNTRY)))
        answer = request.form.getlist('question')
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_COUNTRY))
        
        session['countries'] = answer
        filtered_wines = Wine.query.filter(Wine.id.in_(session['filtered_wines']),
                                            Wine.country.in_(answer)).all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_COUNTRY]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_COUNTRY)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_region', methods=['GET', 'POST'])
@login_required
def recom_question_region():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        regions = get_options('region', filtered_wine_ids)

        if len(regions) <= 1:
            return redirect(url_for(get_next_question(QUESTION_REGION)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_REGION)}/11',
            question="Tens preferència per alguna regió concreta?",
            values=regions
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_REGION)))
        answer = request.form.getlist('question')
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_REGION))
        
        filtered_wines = Wine.query.filter(Wine.id.in_(session['filtered_wines']),
                                            Wine.region.in_(answer)).all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_REGION]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_REGION)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_den_origin', methods=['GET', 'POST'])
@login_required
def recom_question_den_origin():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        dens_origin = get_options('den_origin', filtered_wine_ids)

        if len(dens_origin) <= 1:
            return redirect(url_for(get_next_question(QUESTION_DEN_ORIGIN)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_DEN_ORIGIN)}/11',
            question="Tens preferència per alguna d'aquestes denominacions d'origen?",
            values=dens_origin
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_DEN_ORIGIN)))
        answer = request.form.getlist('question')
        
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_DEN_ORIGIN))
        
        filtered_wines = Wine.query.filter(Wine.id.in_(session['filtered_wines']),
                                            Wine.den_origin.in_(answer)).all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_DEN_ORIGIN]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_DEN_ORIGIN)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_year', methods=['GET', 'POST'])
@login_required
def recom_question_year():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        years = get_options('year', filtered_wine_ids)

        if len(years) <= 1:
            return redirect(url_for(get_next_question(QUESTION_YEAR)))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_YEAR)}/11',
            question="Tens un interès especial per algun d'aquests anys?",
            values=years
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_YEAR)))
        answer = request.form.getlist('question')
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_YEAR))
        
        filtered_wines = Wine.query.filter(Wine.id.in_(session['filtered_wines']),
                                            Wine.year.in_(answer)).all()
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_YEAR]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_YEAR)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_grape', methods=['GET', 'POST'])
@login_required
def recom_question_grape():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        grapes = (
            db.session.query(Grape.name)
            .join(Grape.wines)
            .filter(Wine.id.in_(filtered_wine_ids))
            .distinct().order_by(Grape.name).all()
        )
        grapes = [grape[0] for grape in grapes]
        if len(grapes) <= 1:
            return redirect(url_for(get_next_question(QUESTION_GRAPE)))

        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_GRAPE)}/11',
            question='Quins tipus de raïm prefereixes?',
            values=grapes
        )
    
    elif request.method == 'POST':
        if 'skip' in request.form:
            return redirect(url_for(get_next_question(QUESTION_GRAPE)))
        answer = request.form.getlist('question')
        if not answer:
            flash("Has de respondre abans de continuar", 'warning')
            return redirect(url_for(QUESTION_GRAPE))
        
        filtered_wines = (
            Wine.query.join(Wine.grapes)
            .filter(Wine.id.in_(session['filtered_wines']))
            .filter(Grape.name.in_(answer)).all()
        )
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['grapes'] = answer
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_GRAPE]
        if 'next' in request.form:
            return redirect(url_for(get_next_question(QUESTION_GRAPE)))
        else:
            return redirect(url_for(RESULT))


@questions_bp.route('/recom_question_food', methods=['GET', 'POST'])
@login_required
def recom_question_food():
    if request.method == 'GET':
        filtered_wine_ids = session.get('filtered_wines', [])
        foods = (
            db.session.query(Food.name)
            .join(Food.wines)
            .filter(Wine.id.in_(filtered_wine_ids))
            .distinct().order_by(Food.name).all()
        )
        foods = [food[0] for food in foods]
        if len(foods) <= 1:
            return redirect(url_for(RESULT))
        return render_template(
            QUESTION_TEMPLATE, 
            title=f'Pregunta {QUESTION_ROUTES.index(QUESTION_FOOD)}/11',
            question='Estàs pensant acompanyar un menjar concret?',
            values=foods,
            last=True
        )
    
    elif request.method == 'POST':
        answer = request.form.getlist('question')
        if not answer:
            return redirect(url_for(RESULT))
        filtered_wines = (
            Wine.query.join(Wine.foods)
            .filter(Wine.id.in_(session['filtered_wines']))
            .filter(Food.name.in_(answer)).all()
        )
        session['filtered_wines'] = [wine.id for wine in filtered_wines]
        session['answered_questions'] = session.get('answered_questions', []) + [QUESTION_FOOD]
        return redirect(url_for(RESULT))
    

@questions_bp.route('/result', methods=['GET'])
@login_required
def result():
    filtered_wine_ids = session.get('filtered_wines', [])
    query = Wine.query.filter(Wine.id.in_(filtered_wine_ids))
    filtered_wines = query.all()
    expected_questions = [
        QUESTION_1,
        QUESTION_TASTE,
        QUESTION_RANGE,
        QUESTION_PRICE,
        QUESTION_ALCOHOL,
        QUESTION_COUNTRY,
        QUESTION_REGION,
        QUESTION_DEN_ORIGIN,
        QUESTION_YEAR,
        QUESTION_GRAPE,
        QUESTION_FOOD,
    ]
    answered_questions = session.get('answered_questions', [])
    if len(filtered_wines) < 5 or all(question in answered_questions for question in expected_questions):
        return render_template('result.html', wines=filtered_wines)
    if QUESTION_GRAPE not in answered_questions:
        if has_profile(current_user, ProfileEnum.CURIOS):
            query = variety_filter_by_profile(ProfileEnum.CURIOS, query)
        elif has_profile(current_user, ProfileEnum.EXPERT):
            query = variety_filter_by_profile(ProfileEnum.EXPERT, query)
        else:
            query = user_variety_filter(current_user, query)
    if QUESTION_COUNTRY not in answered_questions:
        # if has_profile(current_user, ProfileEnum.CURIOS):
        #     query = country_filter_by_profile(ProfileEnum.CURIOS, query)
        if has_profile(current_user, ProfileEnum.EXPERT):
            query = country_filter_by_profile(ProfileEnum.EXPERT, query)
    if QUESTION_PRICE not in answered_questions:
        if has_profile(current_user, ProfileEnum.PRAGMATIC):
            query = price_filter_by_profile(ProfileEnum.PRAGMATIC, query)
   
    filtered_wines2 = query.all()
    if filtered_wines2:
        return render_template('result.html', wines=filtered_wines2)
    
    return render_template('result.html', wines=filtered_wines)
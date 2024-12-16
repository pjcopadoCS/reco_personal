from flask import session
from sqlalchemy import func

from constants import Age, Profile, Gender, ranges_alcohol, ranges_price 
from constants import varieties_young_men, varieties_mid_men, varieties_old_men
from constants import varieties_young_women, varieties_mid_women, varieties_old_women
from constants import exotic_varieties, noble_varieties, recognized_countries, emerging_countries

from models import Grape, Wine, db

def delete_session_info():
    session.pop('answered_questions', None)
    session.pop('filtered_wines', None)
    session.pop('countries', None)
    session.pop('grapes', None)

def get_ranges(attribute, wine_ids):
    if attribute == 'alcohol':
        wine_attribute = Wine.alcohol
        ranges = ranges_alcohol
    elif attribute == 'price':
        wine_attribute = Wine.price
        ranges = ranges_price

    available_ranges = []
    for r in ranges:
        count = (
            db.session.query(func.count(Wine.id)) 
            .filter(Wine.id.in_(wine_ids))
            .filter(wine_attribute >= r[0], wine_attribute <= r[1]) 
            .scalar()
        )
        if count > 0:
            available_ranges.append(r)
    return available_ranges


def get_options(attribute, wine_ids):
    attribute_map = {
        'taste': Wine.taste,
        'country': Wine.country,
        'region': Wine.region,
        'den_origin': Wine.den_origin,
        'year': Wine.year,
    }

    wine_attribute = attribute_map.get(attribute)

    options = (
        db.session.query(wine_attribute)
        .filter(Wine.id.in_(wine_ids))
        .filter(wine_attribute.isnot(None))
        .distinct().order_by(wine_attribute).all()
    )
    options = [option[0] for option in options]
    return options


def has_profile(user, profile_name):
    for profile in user.info.profiles:
        if profile.name == profile_name:
            return True
    return False

def variety_filter_by_profile(profile_name, query):
    varieties = []
    if profile_name == Profile.CURIOS:
        varieties = exotic_varieties
    elif profile_name == Profile.EXPERT:
        varieties = noble_varieties

    return query.join(Wine.grapes).filter(Grape.name.in_(varieties))


def country_filter_by_profile(profile_name, query):
    countries = []
    if profile_name == Profile.CURIOS:
        countries = emerging_countries
    elif profile_name == Profile.EXPERT:
        countries = recognized_countries

    return query.filter(Wine.country.in_(countries))


def price_filter_by_profile(profile_name, query):
    if profile_name == Profile.PRAGMATIC:
        return query.filter(Wine.price < 25)

def user_variety_filter(user, query):
    varieties = []
    if user.info.gender == Gender.HOME:
        if user.info.age == Age.JOVE:
            varieties = varieties_young_men
        elif user.info.age == Age.MITJA:
            varieties = varieties_mid_men
        elif user.info.age == Age.GRAN:
            varieties = varieties_old_men
    elif user.info.gender == Gender.DONA:
        if user.info.age == Age.JOVE:
            varieties = varieties_young_women
        elif user.info.age == Age.MITJA:
            varieties = varieties_mid_women
        elif user.info.age == Age.GRAN:
            varieties = varieties_old_women

    return query.join(Wine.grapes).filter(Grape.name.in_(varieties))
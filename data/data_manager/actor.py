from data.db_queries import db_actors
from error_logs import logs


# ========================================================================================

class ReadingProblem(Exception):
    """ If there is problem reading data"""
    pass


# ========================================================================================

def get_all_names():
    try:
        return db_actors.fetch_all_names()
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_all_with_shows():
    try:
        return db_actors.fetch_all_with_shows()
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_by_show_id(show_id):
    try:
        return db_actors.fetch_by_show_id(show_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_details_by_movies_amount(movies_amount):
    try:
        return db_actors.fetch_details_by_movie_amount(movies_amount)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_actor_options_amount():
    try:
        return db_actors.fetch_actor_options_amount()
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def add(name, birthday, death, biography):
    try:
        return db_actors.add_to_db(name, birthday, death, biography)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem

# ========================================================================================

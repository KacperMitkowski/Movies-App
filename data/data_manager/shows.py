from data.db_queries import db_shows
from error_logs import logs


# ========================================================================================

class ReadingProblem(Exception):
    """ If there is problem reading data"""
    pass


# ========================================================================================

def get_details(page, column, order, how_many_movies_per_page):
    try:
        return db_shows.fetch_details(page, column, order, how_many_movies_per_page)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_sorted_details(page_nr, column, order, how_many_movies_per_page, genre):
    try:
        return db_shows.fetch_sorted_details(page_nr,
                                     column,
                                     order,
                                     how_many_movies_per_page,
                                     genre)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_details_by_show_id(show_id):
    try:
        return db_shows.fetch_details_by_show_id(show_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_id_by_actor_id(actor_id):
    try:
        return db_shows.fetch_id_by_actor_id(actor_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_all_with_actors():
    try:
        return db_shows.fetch_all_with_actors()
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem

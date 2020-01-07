from data.db_queries import db_genres
from error_logs import logs


# ========================================================================================

class ReadingProblem(Exception):
    """ If there is problem reading data"""
    pass


# ========================================================================================

def get_all():
    try:
        return db_genres.fetch_all()
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_by_show_id(show_id):
    try:
        return db_genres.fetch_by_show_id(show_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem

# ========================================================================================

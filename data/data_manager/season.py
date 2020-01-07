from data.db_queries import db_seasons
from error_logs import logs


# ========================================================================================

class ReadingProblem(Exception):
    """ If there is problem reading data"""
    pass


# ========================================================================================

def get_all(show_id):
    try:
        return db_seasons.fetch_all(show_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================
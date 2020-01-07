from error_logs import logs


# ========================================================================================

class JsonProblem(Exception):
    """ If there is problem reading data"""
    pass


# ========================================================================================

def check_actor_data(actor_obj):
    try:
        actor_obj['name'] and actor_obj['birthday'] and actor_obj['death'] and actor_obj['biography']
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise JsonProblem


# ========================================================================================

def biography(data):
    if len(data) == 0:
        return 'No data'
    else:
        return data


# ========================================================================================

def date(data):
    if data is None:
        return 'No data'
    else:
        return data


# ========================================================================================

def shows(all_shows, how_many_movies_per_page):
    if len(all_shows) == 0 or len(all_shows) < how_many_movies_per_page:
        return False
    else:
        return True

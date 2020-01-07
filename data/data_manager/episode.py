from data.db_queries import db_episodes
from error_logs import logs


# ========================================================================================

class ReadingProblem(Exception):
    """ If there is problem reading data"""
    pass


# ========================================================================================

def get_details_by_show_id(show_id):
    try:
        return db_episodes.fetch_details_by_show_id(show_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_max_episodes_per_season(show_id):
    try:
        return db_episodes.fetch_max_episodes_per_season(show_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def seasons_with_episodes(season_id):
    try:
        return db_episodes.fetch_seasons_with_episodes(season_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem


# ========================================================================================

def get_details_by_episode_id(episode_id):
    try:
        return db_episodes.fetch_details_by_episode_id(episode_id)
    except Exception as err:
        logs.logger.error('%s', err)
        logs.logging.exception(err)
        raise ReadingProblem

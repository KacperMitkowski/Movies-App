from data import db_connection


@db_connection.connection_handler
def fetch_details_by_show_id(cursor, show_id):
    sql_string = """
                    SELECT seasons.id AS season_id,
                           seasons.season_number AS season_number,
                           episodes.title AS episode_title,
                           episodes.id AS episode_id
                    FROM shows
                    LEFT JOIN seasons ON shows.id = seasons.show_id
                    LEFT JOIN episodes ON seasons.id = episodes.season_id
                    WHERE seasons.show_id = %(show_id)s
                    AND seasons.id = episodes.season_id;
                 """
    cursor.execute(sql_string, {'show_id': show_id})
    details = cursor.fetchall()
    return details


# ========================================================================================

@db_connection.connection_handler
def fetch_max_episodes_per_season(cursor, show_id):
    sql_string = """
                    SELECT COUNT(seasons.id)
                    FROM seasons
                    LEFT JOIN episodes ON seasons.id = episodes.season_id
                    WHERE show_id = %(show_id)s;
                 """
    cursor.execute(sql_string, {'show_id': show_id})
    records = cursor.fetchall()
    return records


# ========================================================================================

@db_connection.connection_handler
def fetch_seasons_with_episodes(cursor, season_id):
    sql_string = """
                    SELECT id AS episode_id,
                           title AS episode_title,
                           episode_number AS episode_number,
                           overview AS episode_overview
                    FROM episodes
                    WHERE season_id = %(season_id)s
                 """
    cursor.execute(sql_string, {'season_id': season_id})
    seasons_with_episodes = cursor.fetchall()
    return seasons_with_episodes


# ========================================================================================

@db_connection.connection_handler
def fetch_details_by_episode_id(cursor, episode_id):
    sql_string = """
                    SELECT id AS episode_id,
                           COALESCE(title, 'No data') AS episode_title,
                           episode_number AS episode_number,
                           overview AS episode_overview,
                           season_id AS season_id
                    FROM episodes
                    WHERE id = %(episode_id)s
                 """
    cursor.execute(sql_string, {'episode_id': episode_id})
    details = cursor.fetchall()
    return details

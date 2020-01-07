from data import db_connection


@db_connection.connection_handler
def fetch_all(cursor, show_id):
    sql_string = """
                    SELECT id AS season_id, 
                           season_number AS season_number,
                           title AS season_title,
                           overview AS season_overview,
                           show_id AS show_id
                    FROM seasons
                    WHERE show_id = %(show_id)s
                    ORDER BY season_number;
                 """
    cursor.execute(sql_string, {'show_id': show_id})
    seasons = cursor.fetchall()
    return seasons


# ========================================================================================

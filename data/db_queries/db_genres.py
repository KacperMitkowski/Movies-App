from data import db_connection


@db_connection.connection_handler
def fetch_all(cursor):
    sql_string = """
                    SELECT DISTINCT name
                    FROM genres
                    ORDER BY name;
                 """
    cursor.execute(sql_string)
    genres = cursor.fetchall()
    return genres


# ========================================================================================

@db_connection.connection_handler
def fetch_by_show_id(cursor, show_id):
    sql_string = """
                    SELECT array_agg(DISTINCT genres.name) AS name
                    FROM shows
                    LEFT JOIN show_genres ON shows.id = show_genres.show_id
                    LEFT JOIN genres ON show_genres.genre_id = genres.id
                    WHERE %(show_id)s = show_genres.show_id
                    AND show_genres.genre_id = genres.id
                 """
    cursor.execute(sql_string, {'show_id': show_id})
    genre = cursor.fetchone()['name']
    return genre

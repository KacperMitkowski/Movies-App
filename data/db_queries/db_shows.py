from data import db_connection


# ========================================================================================

@db_connection.connection_handler
def fetch_details(cursor, page, column, order, how_many_movies_per_page):
    sql_string = """
                    SELECT shows.id,
                           shows.title, 
                           shows.year, 
                           shows.runtime, 
                           shows.trailer, 
                           shows.homepage,
                           ROUND(shows.rating, 3) AS rating, 
                           array_agg(DISTINCT seasons.season_number) AS seasons, 
                           array_agg(DISTINCT genres.name) AS genre
                    FROM shows  
                    LEFT JOIN show_genres ON shows.id = show_genres.show_id
                    LEFT JOIN genres ON show_genres.genre_id = genres.id
                    LEFT JOIN seasons ON shows.id = seasons.show_id
                    GROUP BY shows.id, 
                             shows.title, 
                             shows.year, 
                             shows.runtime, 
                             shows.trailer, 
                             shows.homepage, 
                             rating
                    ORDER BY {} {}
                    OFFSET ({} * %(how_many_movies_per_page)s) - %(how_many_movies_per_page)s;
                 """
    cursor.execute(sql_string.format(column, order, page), {'how_many_movies_per_page': how_many_movies_per_page})
    shows = cursor.fetchall()
    return shows


# ========================================================================================

@db_connection.connection_handler
def fetch_sorted_details(cursor, page, column, order, how_many_movies_per_page, genre):
    sql_string = """
                    SELECT shows.id,
                           shows.title,
                           shows.year,
                           shows.runtime,
                           shows.trailer,
                           shows.homepage,
                           ROUND(shows.rating, 3) AS rating,
                           array_agg(DISTINCT seasons.season_number) AS seasons,
                           array_agg(DISTINCT genres.name) AS genre
                    FROM shows
                    LEFT JOIN show_genres ON shows.id = show_genres.show_id
                    LEFT JOIN genres ON show_genres.genre_id = genres.id
                    LEFT JOIN seasons ON shows.id = seasons.show_id
                    WHERE %(genre)s = genres.name
                    GROUP BY shows.id,
                             shows.title,
                             shows.year,
                             shows.runtime,
                             shows.trailer,
                             shows.homepage,
                             rating
                    ORDER BY {} {}
                    OFFSET ({} * %(how_many_movies_per_page)s) - %(how_many_movies_per_page)s;
                 """
    cursor.execute(sql_string.format(column, order, page), {'genre': genre,
                                                            'how_many_movies_per_page': how_many_movies_per_page})
    sorted_data = cursor.fetchall()
    return sorted_data


# ========================================================================================

@db_connection.connection_handler
def fetch_details_by_show_id(cursor, show_id):
    sql_string = """
                    SELECT title,
                           year,
                           overview,
                           trailer 
                    FROM shows
                    WHERE id=%(show_id)s;
                 """
    cursor.execute(sql_string, {'show_id': show_id})
    details = cursor.fetchone()
    return details


# ========================================================================================

@db_connection.connection_handler
def fetch_id_by_actor_id(cursor, actor_id):
    sql_string = """
                    SELECT shows.id
                    FROM shows
                    LEFT JOIN show_characters ON shows.id = show_characters.show_id
                    LEFT JOIN actors ON show_characters.actor_id = actors.id
                    WHERE actors.id = %(actor_id)s
                 """
    cursor.execute(sql_string, {'actor_id': actor_id})
    all_id = cursor.fetchall()
    return all_id


# ========================================================================================

@db_connection.connection_handler
def fetch_all_with_actors(cursor):
    sql_string = """
                    SELECT COALESCE(actors.id, '0') AS actor_id,
                           COALESCE(actors.name, 'No data') AS actor_name,
                           TO_CHAR(actors.birthday, 'dd-mon-yy') AS actor_birthday,
                           TO_CHAR(actors.death, 'dd-mon-yy') AS actor_death,
                           COALESCE(actors.biography, 'No data') AS actor_biography,
                           shows.id AS show_id,
                           shows.title AS show_title
                    FROM shows
                    LEFT JOIN show_characters ON shows.id = show_characters.show_id
                    LEFT JOIN actors ON show_characters.actor_id = actors.id
                    ORDER BY actors.name;
                 """
    cursor.execute(sql_string)
    shows_with_actors_played_in_that_shows = cursor.fetchall()
    return shows_with_actors_played_in_that_shows

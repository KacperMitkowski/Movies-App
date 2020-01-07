from data import db_connection


@db_connection.connection_handler
def fetch_all_names(cursor):
    sql_string = """
                    SELECT name 
                    FROM actors
                    ORDER BY name;
                 """
    cursor.execute(sql_string)
    actors = cursor.fetchall()

    actors_arr = []
    for actor in actors:
        actors_arr.append(actor['name'])
    return actors_arr


# ========================================================================================

@db_connection.connection_handler
def fetch_by_show_id(cursor, show_id):
    sql_string = """
                    SELECT DISTINCT actors.name AS name
                    FROM shows 
                    LEFT JOIN show_characters ON shows.id = show_characters.show_id
                    LEFT JOIN actors ON show_characters.actor_id = actors.id
                    WHERE shows.id = %(show_id)s;
                 """
    cursor.execute(sql_string, {'show_id': show_id})
    details = cursor.fetchall()

    actors_arr = []
    for single_actor in details:
        actors_arr.append(str(single_actor['name']))
    return actors_arr


# ========================================================================================

@db_connection.connection_handler
def fetch_details_by_movie_amount(cursor, movie_amount):
    sql_string = """
                    SELECT actors.name,
                           COUNT(show_characters.actor_id)
                    FROM show_characters
                    LEFT JOIN actors 
                    ON show_characters.actor_id = actors.id
                    GROUP BY actors.name
                    HAVING COUNT(show_characters.actor_id) >= {}
                    ORDER BY actors.name;
                 """
    cursor.execute(sql_string.format(movie_amount))
    details = cursor.fetchall()
    return details


# ========================================================================================

@db_connection.connection_handler
def fetch_actor_options_amount(cursor):
    sql_string = """
                    SELECT actors.name,
                           COUNT(show_characters.actor_id)
                    FROM show_characters
                    LEFT JOIN actors 
                    ON show_characters.actor_id = actors.id
                    GROUP BY actors.name;
                 """
    cursor.execute(sql_string)
    actors = cursor.fetchall()

    options_amount_arr = []
    for actor in actors:
        options_amount_arr.append(actor['count'])

    options_amount = max(options_amount_arr)
    return options_amount


# ========================================================================================

@db_connection.connection_handler
def add_to_db(cursor, name, birthday, death, biography):
    if len(birthday) == 0:
        birthday = None
    if len(death) == 0:
        death = None

    sql_string = """
                    INSERT INTO actors(id, name, birthday, death, biography)
                    VALUES ((SELECT MAX(id)
                             FROM actors) + 1, %(name)s, %(birthday)s, %(death)s, %(biography)s);
                             
                    INSERT INTO show_characters(id, show_id, actor_id, character_name)
                    VALUES ((SELECT MAX(id) 
                             FROM show_characters) + 1, NULL, (SELECT id 
                                                               FROM actors 
                                                               WHERE name=%(name)s), NULL)
                 """
    cursor.execute(sql_string, {'name': name,
                                'birthday': birthday,
                                'death': death,
                                'biography': biography})


# ========================================================================================

@db_connection.connection_handler
def fetch_all_with_shows(cursor):

    sql_string = """
                    SELECT actors.id,
                           actors.name,
                           to_char(actors.birthday, 'dd-mm-yyyy') AS birthday,
                           to_char(actors.death, 'dd-mm-yyyy') AS death,
                           actors.biography,
                           array_agg(DISTINCT shows.title) AS movie
                    FROM shows
                    LEFT JOIN show_characters ON shows.id = show_characters.show_id
                    LEFT JOIN actors ON show_characters.actor_id = actors.id
                    GROUP BY actors.id,
                             actors.name;
                             
                 """
    cursor.execute(sql_string)
    actors = cursor.fetchall()
    return actors



@db_connection.connection_handler
def fetch_all_with_shows(cursor):
    sql_string = """
                    SELECT actors.id,
                           actors.name,
                           array_agg(DISTINCT shows.title) AS movie
                    FROM shows
                    LEFT JOIN show_characters ON shows.id = show_characters.show_id
                    LEFT JOIN actors ON show_characters.actor_id = actors.id
                    GROUP BY actors.id,
                             actors.name
                 """
    cursor.execute(sql_string)
    actors_with_shows = cursor.fetchall()
    return actors_with_shows
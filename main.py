from flask import Flask, render_template, request, redirect
import json, jinja2

from data.data_manager import shows, season, genre, episode, actor
import validation, utils

app = Flask('codecool_series')

# ========================================================================================

# object for pagination from main page
page_details = {
    'actual': 1,
    'previous': 0,
    'next': 2,
    'column': 'rating',
    'order': 'DESC',
    'sorted_genre': None
}
movies_per_page = 25  # in main page
genres_displayed = 3  # in main page
stars_in_button = 20  # in main page in the middle button


# ========================================================================================


@app.route('/')
def go_to_index():
    return redirect('/page=1/column=rating/order=DESC/sorted_genre=null')


# ========================================================================================


@app.route('/page=<int:page_nr>/column=<string:column>/order=<string:order>/sorted_genre=<string:sorted_genre>')
def index(page_nr, column, order, sorted_genre):
    try:
        utils.update_page_object(page_details,
                                 page_nr,
                                 column,
                                 order,
                                 sorted_genre)
        all_shows = utils.get_right_shows(page_nr,
                                          column,
                                          order,
                                          movies_per_page,
                                          sorted_genre)
        if validation.shows(all_shows, movies_per_page):
            return render_template('index.html',
                                   shows=all_shows,
                                   genres=genre.get_all(),
                                   page_info=json.dumps(page_details),
                                   hide_button=False if page_nr > 1 else True,
                                   how_many_movies_per_page=movies_per_page,
                                   how_many_genres_displayed=genres_displayed,
                                   how_many_stars_in_button=stars_in_button)
        else:
            return render_template('error.html',
                                   error='Something went wrong. Try again later.')
    except (shows.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/page_info/<string:page>')
def prepare_data_before_change_page(page):
    # When change page in pagination -> update data in object
    try:
        json_obj = json.dumps(page_details)
        if page == 'next':
            page_details['actual'] += 1
            page_details['next'] += 1
            page_details['previous'] = page_details['actual'] - 1
        elif page == 'previous':
            page_details['actual'] -= 1
            page_details['previous'] -= 1
            page_details['next'] = page_details['actual'] + 1
        return json_obj

    except jinja2.exceptions.TemplateNotFound:
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/season=<int:show_id>')
def get_seasons(show_id):
    try:
        seasons = season.get_all(show_id)
        return json.dumps(seasons)
    except (shows.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/tv-show/<int:show_id>')
def show_movie_details(show_id):
    try:
        title = shows.get_details_by_show_id(show_id)['title']
        year = shows.get_details_by_show_id(show_id)['year']
        overview = shows.get_details_by_show_id(show_id)['overview']
        seasons = utils.get_seasons_with_episodes(show_id)
        total_episodes_amount = len(episode.get_details_by_show_id(show_id))
        genres = ', '.join(genre.get_by_show_id(show_id))
        trailer = utils.get_trailer(show_id)
        actors = actor.get_by_show_id(show_id)
        stars_amount = 5

        show = {
            'title': title,
            'year': year,
            'overview': overview,
            'total_episodes_amount': total_episodes_amount,
            'genres': genres,
            'trailer': trailer,
            'actors': actors,
            'stars_amount': stars_amount
        }

        return render_template('show_details.html',
                               show=show,
                               seasons=seasons)
    except (shows.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/min=<int:movies_amount>')
def show_actors_from_movies(movies_amount):
    try:
        actors = actor.get_details_by_movies_amount(movies_amount)
        options_amount = actor.get_actor_options_amount()
        return render_template('how_many_times_actor_played.html',
                               actors=actors,
                               options_amount=options_amount,
                               movies_amount=movies_amount)
    except (actor.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/add_actor')
def show_new_actor_form():
    try:
        return render_template('new_actor_form.html')
    except jinja2.exceptions.TemplateNotFound:
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/add_actor', methods=['POST'])
def add_actor():
    try:
        actor_obj = request.get_json()
        validation.check_actor_data(actor_obj)
        actor_name = actor_obj['name']

        if actor_name in actor.get_all_names():
            error = {'error_msg': 'Actor already exists in database'}
            json_obj = json.dumps(error)
            return json_obj
        else:
            birthday = actor_obj['birthday']
            death = actor_obj['death']
            biography = actor_obj['biography']
            actor.add(actor_name, birthday, death, biography)
            message_for_user = {'message': 'Actor added'}
            return json.dumps(message_for_user)

    except (validation.JsonProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/first_actors')
def show_first_actors():
    try:
        data = actor.get_all_with_shows()
        return render_template("first_20_actors.html",
                               data=data,
                               actors_amount=stars_in_button)
    except (actor.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/actor_id=<int:actor_id>')
def actor_modal(actor_id):
    try:
        actor_with_shows = actor.get_all_with_shows()

        for element in actor_with_shows:
            if actor_id == element['id']:
                shows_id = shows.get_id_by_actor_id(actor_id)

                data = {
                    'actor_id': element['id'],
                    'actor_name': element['name'],
                    'movies': element['movie'],
                    'shows_id': shows_id
                }
                return json.dumps(data)

        raise validation.JsonProblem

    except (actor.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/episode=<int:episode_id>')
def episode_details(episode_id):
    try:
        details = episode.get_details_by_episode_id(episode_id)
        return json.dumps(details)
    except (episode.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/api/top-actors')
def show_all_actors():
    try:
        actors = []
        for actor in shows.get_all_with_actors():
            actor['actor_biography'] = validation.biography(actor['actor_biography'])
            actor['actor_death'] = validation.date(actor['actor_death'])
            actor['actor_birthday'] = validation.date(actor['actor_birthday'])
            actors.append(actor)

        return render_template('all_actors_details.html',
                               actors=actors)
    except (shows.ReadingProblem, jinja2.exceptions.TemplateNotFound):
        return render_template('error.html',
                               error='Something went wrong. Try again later.')


# ========================================================================================

@app.route('/error')
def error_page():
    return render_template('error.html')


# ========================================================================================

@app.route('/new_actor', methods=['POST'])
def add_new_actor():
    data = request.get_json()
    imie = data['imie']
    nazwisko = data['nazwisko']
    print(imie)
    print(nazwisko)



if __name__ == '__main__':
    app.run(debug=True)

# ========================================================================================

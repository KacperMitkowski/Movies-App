from data.data_manager import shows, season, episode


def get_seasons_with_episodes(show_id):
    seasons = []
    for single_season in season.get_all(show_id):
        season_id = single_season['season_id']
        episodes = episode.seasons_with_episodes(season_id)
        single_season['episodes'] = episodes
        seasons.append(single_season)
    return seasons


# ========================================================================================

def get_trailer(show_id):
    show = shows.get_details_by_show_id(show_id)
    trailer = ''

    if show['trailer']:
        trailer = show['trailer'].replace('watch?v=', 'embed/')
    return trailer


# ========================================================================================

def update_page_object(page_details, page_nr, column, order, sorted_genre):
    page_details['actual'] = page_nr
    page_details['previous'] = page_nr - 1
    page_details['next'] = page_nr + 1
    page_details['column'] = column
    page_details['order'] = order
    page_details['sorted_genre'] = sorted_genre


# ========================================================================================

def get_right_shows(page_nr, column, order, movies_per_page, sorted_genre):
    if sorted_genre == 'null':
        return shows.get_details(page_nr,
                                 column,
                                 order,
                                 movies_per_page)
    else:
        return shows.get_sorted_details(page_nr,
                                        column,
                                        order,
                                        movies_per_page,
                                        sorted_genre)

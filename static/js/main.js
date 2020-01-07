export {main}
import {page} from "./pagination.js";
import {sorting} from "./sorting.js";
import {seasons} from "./seasons.js";
import {genre} from "./genre.js";
import {styles} from "./styles.js";
import {actors} from "./actors.js";
import {episodes} from "./episodes.js";

const main = {
  start: function () {
    this.pagination();
    this.sortingShows();
    this.sortingGenres();
    this.episodeModal();
    this.seasonModal();
    this.actorButtons();
    this.actorDetails();
    this.prepareStyles();
  },

  // ========================================================================================

  pagination: function () {
    let previousPageButton = document.getElementById('previousPageButton');
    let nextPageButton = document.getElementById('nextPageButton');

    if (previousPageButton || nextPageButton) {
      previousPageButton.addEventListener('click', () => page.change('previous'));
      nextPageButton.addEventListener('click', () => page.change('next'))
    }
  },

  // ========================================================================================

  sortingShows: function () {
    let shows = document.getElementById('title');
    let year = document.getElementById('year');
    let runtime = document.getElementById('runtime');
    let rating = document.getElementById('rating');
    let sortButtons = [shows, year, runtime, rating];

    if (shows && year && runtime && rating)
      sortButtons.forEach(button => button.addEventListener('click', () => sorting.changeOrder(button.id)))
  },

  // ========================================================================================

  sortingGenres: function () {
    let searchButton = document.getElementById('search_genre_button');

    if (searchButton) {
      searchButton.addEventListener('click', () => {
        let chosenGenre = document.getElementById('select_id').value;
        genre.getData(chosenGenre)
      });
    }
  },

  // ========================================================================================

  seasonModal: function () {
    let buttons = document.querySelectorAll('.season_button');

    buttons.forEach(button => button.addEventListener('click', () => {
      let showId = button.dataset.show_id;
      seasons.getAll(showId);
    }));
  },

  // ========================================================================================

  episodeModal: function() {
    let allLinks = document.querySelectorAll('.episode_link');

    if(allLinks.length > 0) {
      allLinks.forEach(link => {

        let linkId = link.dataset.single_episode_id;
        link.addEventListener('click', ()=> episodes.getData(linkId));
      })
    }
  },

  // ========================================================================================

  actorButtons: function () {
    let ActorsPageButton = document.getElementById('show_actors');
    let filmsAmountButton = document.getElementById('show_film_amount_button');
    let addActorButton = document.getElementById('add_actor_form');
    let pageNr = 1;

    if(ActorsPageButton)
      ActorsPageButton.addEventListener('click', () => actors.showPage(pageNr));

    if(filmsAmountButton)
      filmsAmountButton.addEventListener('click', ()=> actors.newActorsAmount());

    if(addActorButton)
      addActorButton.addEventListener('submit', event=> {
        event.preventDefault();
        if(actors.dataOK())
          actors.addNewActor();
        else
          styles.showAddActorError('Wrong data');
      });

  },
  // ========================================================================================

  actorDetails: function() {
    let allLinks = document.querySelectorAll('.actor_link');
    if (allLinks.length > 0) {
      allLinks.forEach(link => {
        let actorId = link.dataset.actor_id;
        link.addEventListener('click', ()=> actors.getDetails(actorId));
      })
    }
  },

  // ========================================================================================

  prepareStyles: function () {
    styles.sortingButtons();
    styles.searchedGenreOption();
    styles.searchedActorsOption();
  },
};

// ========================================================================================

window.onclick = function (event) {
  if (actors.actorModal && event.target === actors.actorModal) {
    actors.actorModal.innerHTML = '';
    actors.actorModal.style.display = 'none';
  }
  if (seasons.seasonModal && event.target === seasons.seasonModal) {
    seasons.seasonModal.innerHTML = '';
    seasons.seasonModal.style.display = 'none';
  }

  if (episodes.episode_modal && event.target === episodes.episode_modal) {
    episodes.episode_modal.innerHTML = '';
    episodes.episode_modal.style.display = 'none';
  }
};

main.start();
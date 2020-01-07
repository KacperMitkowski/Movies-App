export {styles}

const styles = {
  sortingButtons: function () {
    let page = JSON.parse(localStorage.getItem('page'));
    let sortingButton = document.getElementById(page.column);
    let sortingOrder = page.order;

    if (sortingButton) {
      if (sortingOrder === 'ASC') {
        sortingButton.setAttribute('class', 'fas fa-caret-down');
        sortingButton.style.backgroundColor = 'green';
      }
      else {
        sortingButton.setAttribute('class', 'fas fa-caret-up');
        sortingButton.style.backgroundColor = 'yellow';
      }
    }
  },

  // ========================================================================================

  searchedGenreOption: function () {
    let allOptions = document.querySelectorAll('#genre_sorting > select > option');
    let localStorageObject = JSON.parse(localStorage.getItem('page'));
    let searchedOption = localStorageObject.sorted_genre;

    allOptions.forEach(option => {
      if (option.dataset.id === searchedOption) {
        option.selected = true;
      }
    })
  },

  // ========================================================================================

  searchedActorsOption: function () {
    let allOptions = document.querySelectorAll('.actor_option');
    let actorsPageHref = /min=/i;

    if(location.pathname.match(actorsPageHref)) {

      let optionNr = location.pathname.split('=')[1];
      allOptions.forEach(option => {
        if(option.dataset.actors_amount === optionNr)
          option.selected = true;
      })
    }

  },

  // ========================================================================================

  showAddActorError: function (message) {
    let errorDiv = document.getElementById('add_actor_error');
    let addActorButton = document.getElementById('add_new_actor_button');

    errorDiv.innerHTML = message;
    errorDiv.style.display = 'block';
    addActorButton.disabled = true;

    setTimeout(()=> {
      errorDiv.innerHTML = '';
      errorDiv.style.display = 'none';
      addActorButton.disabled = false;
    }, 3000)
  }
};
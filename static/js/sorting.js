export {sorting}

const sorting = {
  changeOrder: function (column) {
    let jsObj = JSON.parse(localStorage.getItem('page'));
    if (jsObj.actual && jsObj.order && jsObj.sorted_genre) {
      let currentPage = jsObj.actual;
      let currentOrder = jsObj.order;
      let currentSortingGenre = jsObj.sorted_genre;
      let newOrder, newPage;

      currentOrder === 'DESC' ? newOrder = 'ASC' : newOrder = 'DESC';

      newPage = {
        actual: jsObj.actual,
        previous: jsObj.previous,
        next: jsObj.next,
        column: column,
        order: newOrder
      };

      localStorage.setItem('page', JSON.stringify(newPage));
      location.href = `/page=${currentPage}/column=${column}/order=${newOrder}/sorted_genre=${currentSortingGenre}`;
    }
    else
      location.href = '/error';
  }

  // ############################################################################################
};
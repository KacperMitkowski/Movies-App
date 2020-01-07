export {genre}

const genre = {
  getData: function (chosenGenre) {

    let jsObj = JSON.parse(localStorage.getItem('page'));
    if (jsObj.actual && jsObj.column && jsObj.order) {
      let actualPage = jsObj.actual;
      let actualColumn = jsObj.column;
      let actualOrder = jsObj.order;
      location.href = `/page=${actualPage}/column=${actualColumn}/order=${actualOrder}/sorted_genre=${chosenGenre}`;
    }
    else
      location.href = '/error';
  }
};
export {page}

const page = {
  change: function (pageNumber) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', `/page_info/${pageNumber}`);
    httpRequest.onload = () => {
      let pageObj = JSON.parse(httpRequest.response);
      if (pageObj[pageNumber] && pageObj.column && pageObj.order && pageObj.sorted_genre) {
        let page = pageObj[pageNumber];
        let column = pageObj.column;
        let order = pageObj.order;
        let sorted_genre = pageObj.sorted_genre;
        location.href = `/page=${page}/column=${column}/order=${order}/sorted_genre=${sorted_genre}`;
      }
      else
        location.href = '/error';
    };
    httpRequest.send();
  }

  // ############################################################################################
};

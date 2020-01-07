export {seasons}
import {utils} from "./utils.js";

const seasons = {
  seasonModal : document.getElementById('season_modal'),

  // ========================================================================================

  getAll: function (showId) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', `/season=${showId}`);
    httpRequest.onload = () => {
      let seasons = JSON.parse(httpRequest.response);
      if(seasons)
        this.showModal(seasons);
      else
        location.href = '/error';
    };
    httpRequest.send();
  },

  // ========================================================================================

  showModal: function(seasons) {
    let contentString = '';

    contentString += `
    <div class="modal-content">
      <table>
        <tr>
            <th>Title</th>
            <th>Overview</th>
        </tr>
    `;

    for(let season of seasons) {
      contentString += `
        <tr>
            <td>${season['season_title']}</td>
            <td style="text-align: left;">${utils.getComment(season['season_overview'])}</td>
        </tr>
      `;
    }

    contentString += `
      </table>
    </div>
    `;

    this.seasonModal.insertAdjacentHTML('afterbegin', contentString);
    this.seasonModal.style.display = 'block';
  },

  // ========================================================================================
};

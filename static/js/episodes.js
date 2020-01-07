export {episodes}
import {utils} from "./utils.js";

const episodes = {
  episode_modal: document.getElementById('episode_modal'),

  getData: function (episodeId) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', `/episode=${episodeId}`);
    httpRequest.onload = () => {
      let data = JSON.parse(httpRequest.response);
      if(data)
        this.showModal(data);
      else
        location.href = '/error';
    };
    httpRequest.send();
  },

  // ========================================================================================

  showModal: function (data) {
    let contentString = `
      <div class="modal-content">
        <table>
          <tr>
              <th>Title</th>
              <th>Episode number in season</th>
              <th>Overview</th>
          </tr>
          <tr>
              <td>${data[0].episode_title}</td>
              <td>${data[0].episode_number}</td>
              <td>${utils.getComment(data[0].episode_overview)}</td>
          </tr>
        </table>
      </div>
    `;

    this.episode_modal.insertAdjacentHTML('afterbegin', contentString);
    this.episode_modal.style.display = 'block';
  }
};
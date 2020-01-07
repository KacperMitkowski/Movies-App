export {actors}
import {styles} from "./styles.js";

const actors = {
  actorModal : document.getElementById('actor_details_modal'),

  showPage: function (pageNr) {
    location.href = `/min=${pageNr}`;
  },

  // ========================================================================================

  newActorsAmount: function () {
    let options = document.querySelectorAll('.actor_option');
    options.forEach(option => {
      if (option.selected === true) {
        let pageNr = option.dataset.actors_amount;
        this.showPage(pageNr);
      }
    })
  },

  // ========================================================================================

  dataOK: function () {
    return (this.nameOK() && this.datesOK());
  },

  // ========================================================================================

  nameOK: function () {
    let firstName = document.getElementById('actor_first_name').value;
    let lastName = document.getElementById('actor_last_name').value;

    // FIRST REMOVE ALL WHITESPACES
    firstName = firstName.trim();
    lastName = lastName.trim();

    // IF NO FIRST/LAST NAME OR ONLY SPACES
    if (firstName.length === 0 || lastName.length === 0)
      return false;

    // IF SPACES INSIDE FIRST/LAST NAME
    if (firstName.indexOf(' ') !== -1 || lastName.indexOf(' ') !== -1)
      return false;

    // IF WRONG SIGNS IN FIRST/LAST NAME
    let patternForDigit = /[0-9]/;
    let patternForSymbol = /[!@#$%^&*()_=+{};',./<>?|]/;

    for (let char of firstName) {
      if (char.match(patternForDigit) || char.match(patternForSymbol))
        return false;
    }

    for (let char of lastName) {
      if (char.match(patternForDigit) || char.match(patternForSymbol))
        return false;
    }

    return true;
  },

  // ========================================================================================

  datesOK: function () {
    let birthdayDate = document.getElementById('actor_birthday').value;
    let deathDate = document.getElementById('actor_death').value;
    let today = new Date();
    let birthday = new Date(birthdayDate);
    let death = new Date(deathDate);

    if (birthday >= today)
      return false;
    if (death <= today)
      return false;

    return true;
  },

  // ========================================================================================

  addNewActor: function () {
    let firstName = document.getElementById('actor_first_name').value;
    let lastName = document.getElementById('actor_last_name').value;
    let fullName = firstName + ' ' + lastName;
    let birthday = document.getElementById('actor_birthday').value;
    let death = document.getElementById('actor_death').value;
    let biography = document.getElementById('actor_biography').value;


    let httpRequest = new XMLHttpRequest();
    httpRequest.open('POST', '/add_actor');
    httpRequest.setRequestHeader('Content-Type', 'application/json');

    httpRequest.onload = () => {
      let jsObj = JSON.parse(httpRequest.response);
      if (jsObj.error_msg)
        styles.showAddActorError(jsObj.error_msg);
      else if (jsObj.message)
        this.showSuccessMessage(jsObj.message);
      else
        location.href = '/error';
    };

    let jsObj = {
      'name': fullName,
      'birthday': birthday,
      'death': death,
      'biography': biography
    };

    let jsonObj = JSON.stringify(jsObj);
    httpRequest.send(jsonObj);
  },

  // ========================================================================================

  showSuccessMessage: function (message) {
    let addNewActorDiv = document.getElementById('add_new_actor_div');
    let messageHeader = document.getElementById('message_for_the_user');
    addNewActorDiv.remove();
    messageHeader.innerHTML = message + '<br /> You will be redirected in a moment';

    setTimeout(() => {
      location.href = '/min=1';
    }, 5000)
  },

  // ========================================================================================

  getDetails: function (actorId) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', `/actor_id=${actorId}`);
    httpRequest.onload = () => {
      let details = JSON.parse(httpRequest.response);
      if(details)
        this.showModal(details);
      else
        location.href = '/error';
    };
    httpRequest.send();
  },

  // ========================================================================================

  showModal: function (data) {
    let contentString = '';

    contentString += `
     <div class="modal-content">
        <table>
            
          <tr>
              <th>Actor</th>
              <th>Shows</th>
          </tr>
            
          <tr>
            <td>${data.actor_name}</td>
            <td>
              <ol>`;

    for(let i=0; i< data.movies.length; i++)
      contentString += `<li><a href="/tv-show/${data.shows_id[i].id}">${data.movies[i]}</a></li>`;


    contentString += `
              </ol>          
            </td>
          </tr>
        </table>
      </div>
    `;

    this.actorModal.insertAdjacentHTML('afterbegin', contentString);
    this.actorModal.style.display = 'block';
  }

};

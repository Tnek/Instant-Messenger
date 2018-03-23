/** =====================================================================
  Dummy Database **/
var contactDatabase2 = ["Roy, Hui", "Felicity, Bi Ling, Alice", "Alice, Nico"];
var contactDatabase3 = {"Roy": "Hello"};


/** =====================================================================
  Create Groups **/

//Create New Conv 
function listUsers(){
  $.getJSON("/users", function(result) {
    $('all-users').html('');
    //arrow function
    result.map( contact => {
    $('#all-users').append(`

      <div class="form-group">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="gridCheck">
          <label class="form-check-label" for="gridCheck">
            ${contact}
          </label>
        </div>
      </div>

    `);
    })
  });

  // setTimeout(getUsers, 5000); //5s delay
};


/** =====================================================================
  Generate Contact Lists **/

//Private message list
function getUsers(){
  $.getJSON("/users", function(result) {
    $('#private-message-list').html('');
    //arrow function
    result.map( contact => {
    $('#private-message-list').append(`
      <li class="clearfix">
        <div class="about">
          <div class="name"> ${contact} </div>
          <div class="status">
            <i class="fa fa-circle online"></i> online
          </div>
        </div>
      </li>
    `);
    })
  });

  // setTimeout(getUsers, 5000); //5s delay
};

//Group message list
function getGroupList(){
  $.getJSON("/users", function(result) {
    $('#group-message-list').html('');
  //arrow function
  result.map( contact => {
    $('#group-message-list').append(`
        <li class="clearfix user-li" onclick="getChatWindow(this)">
          <div class="about">
            <div class="name"> ${contact} </div>
            <div class="status">
              <i class="fa fa-circle online"></i> online
            </div>
          </div>
        </li>
    `);
    })
  });

  // setTimeout(getUsers, 5000); //5s delay
};


/** =====================================================================
  Search Functions **/
function searchPrivate() {
    var input, filter, list, contact, i;
    input = document.getElementById("search-private");
    filter = input.value.toUpperCase();
    list = document.getElementById("private-message-list");
    contact = list.getElementsByClassName("name");
    for (i = 0; i < contact.length; i++) {
        if (contact[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            contact[i].parentElement.parentElement.style.display = "";
        } else {
            contact[i].parentElement.parentElement.style.display = "none";
        }
    }
}

//merge searchGroup with searchPrivate depending on db
function searchGroup() {
    var input, filter, list, contact, i;
    input = document.getElementById("search-group");
    filter = input.value.toUpperCase();
    list = document.getElementById("group-message-list");
    contact = list.getElementsByClassName("name");
    for (i = 0; i < contact.length; i++) {
        if (contact[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            contact[i].parentElement.parentElement.style.display = "";
        } else {
            contact[i].parentElement.parentElement.style.display = "none";
        }
    }
}


/** =====================================================================
  Onclick Chat **/
function getChatWindow(e){
  currContact = document.getElementById("currUser");
  currContact.innerHTML = e.getElementsByClassName("name")[0].innerHTML;
}

//Get Current Contact
function getCurr(){
  currContact = document.getElementById("currUser");
  currContact.append("Tnek");
}


/** =====================================================================
  Onload **/

$(document).ready(function() {
    getUsers();
    // getCurr();
    listUsers();
    getGroupList();
});


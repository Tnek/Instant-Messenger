/** =====================================================================
  Dummy Database **/
var contactDatabase2 = ["Roy, Hui", "Felicity, Bi Ling, Alice", "Alice, Nico"];
var contactDatabase3 = {"Roy": "Hello"};
var contacts = [];
var selectedContact = null;

/** =====================================================================
  Create Groups **/

function loadContacts(){
  $.getJSON("/users", function(result) {
    contacts = result;
    getUsers();
    getGroupList();
    getModalList();
    getCurr();
  });

  setTimeout(loadContacts, 1000); //3s delay
}

/** =====================================================================
  Generate Contact Lists **/

//Private message list
function getUsers(){
  privatesearch.render();
};

//Group message list
function getGroupList(){
  groupsearch.render();
};

//Modal message list 
function getModalList(){
  checklistsearch.render();
};

/** =====================================================================
  Search Functions **/
function searchPrivate() {
  privatesearch.render();
}

function searchGroup() {
  groupsearch.render();
}

function searchChecklist() {
  checklistsearch.render();
}

/** =====================================================================
  SearchBar **/
class SearchBar {
  constructor(input, target, is_modal) {
    this.input = document.getElementById(input);
    this.target = document.getElementById(target);
    this.is_modal = is_modal;
  }

  render() {
    let querystring = this.input.value.toLowerCase();
    let filteredList = contacts.filter(contact => contact.toLowerCase().indexOf(querystring) > -1);

    this.target.innerHTML = '';

    if( this.is_modal == false ){
      filteredList.map( contact => {
      $(this.target).append(`
        <li class="clearfix user-li" onclick="getChatWindow(this)">
          <div class="about">
            <div class="name name-field">${contact}</div>
            <div class="status">
              <i class="fa fa-circle online"></i> online
            </div>
          </div>
        </li>
      `);
      })
    }else{
      filteredList.map( contact => {
        $(this.target).append(`
          <div class="form-group">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="gridCheck">
              <label class="form-check-label name-field" for="gridCheck">${contact}</label>
            </div>
          </div>
        `);
      })
    }
  }

}

var groupsearch = new SearchBar("search-group", "group-message-list", false);
var privatesearch = new SearchBar("search-private", "private-message-list", false);
var checklistsearch = new SearchBar("search-checklist", "checklist-list", true);

/** =====================================================================
  Onclick Chat **/
function getChatWindow(e){
  selectedContact = $(e).find('.name').first().html();
  $("#currUser").html(selectedContact);
}

//Get Current Contact
function getCurr(){
  if (contacts.indexOf(selectedContact) == -1) {
    selectedContact = null;
  }
  if (!selectedContact) {
    selectedContact = contacts[0];
    $("#currUser").html(selectedContact);
  }
}


/** =====================================================================
  Onload **/
$(document).ready(function() {
    loadContacts();
});

/** =====================================================================
  Constant **/
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


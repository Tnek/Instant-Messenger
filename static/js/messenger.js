class SideBarList {
  constructor(input, target) {
    this.input = input;
    this.target = target;
  }

  render(list_of_items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = list_of_items.filter(item => item.toLowerCase().indexOf(query) > - 1);

    $(this.target).empty();

    visible_items.map( item => {
      $(this.target).append(`
        <li class="clearfix user-li" onclick="getChatWindow(this)">
          <div class="about">
            <div class="name name-field">
              <span class="fa fa-circle online"></span>
              ${item}
            </div>
          </div> 
        </li>
      `);
    });
  }
}

class ModalBox {
  constructor(input, target) {
    this.input = input;
    this.target = target;
  }

  render(list_of_items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = list_of_items.filter(item => item.toLowerCase().indexOf(query) > - 1);

    $(this.target).empty();

    visible_items.map( item => {
      $(this.target).append(`
        <div class="form-group">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="gridCheck">
            <label class="form-check-label name-field" for="gridCheck">${item}</label>
          </div>
        </div>
      `);
    });
  }
}

class Messenger {
    constructor() {
        this.selected_conversation = null;
        this.get_active_contacts();
        this.get_conversations();
        this.conversations = {};
        this.contacts = [];

        this.conversations_bar = new SideBarList("#search-group", "#group-message-list");
        this.pm_bar = new SideBarList("#search-private", "#private-message-list");

        this.users_search = new ModalBox("#search-checklist", "#checklist-list");
        this.tick();
    }

    get_active_contacts() {
        $.getJSON("/users", contacts => {
            this.contacts = contacts;
        });
        setTimeout(this.get_active_contacts, 1000);
    }

    get_conversations() {
        $.getJSON("/conversations", convs => {
            this.conversations = convs;
        });
    }

    render_conversations() { this.conversations_bar.render(Object.keys(this.conversations)); } 
    render_pms() { this.pm_bar.render(this.contacts); } 
    render_users_search() { this.users_search.render(this.contacts); }

    render() {
        this.render_conversations();
        this.render_pms();
        this.render_users_search();
    }

    tick() {
        $.getJSON("/events", result => {
            this.render();
        });

        setTimeout(this.tick.bind(this), 1000);
    }
}


var messenger = new Messenger();

$(document).ready(function() {
    messenger.tick();
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


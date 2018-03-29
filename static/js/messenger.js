class SideBarList {
  constructor(input, target, list_entry_generator) {
    this.input = input;
    this.target = target;
    this.list_entry_generator = list_entry_generator;
  }

  render(list_of_items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = list_of_items.filter(item => item.toLowerCase().indexOf(query) > - 1);

    $(this.target).empty();

    visible_items.map( item => {
      $(this.target).append(this.list_entry_generator(item));
    });
  }
}

function conv_barentry(item) {
    return `<li class="clearfix user-li" onclick="messenger.select_conv('${item}')">
          <div class="about">
            <div class="name name-field">
               <span class="fa fa-comments online"></span>
               ${item.slice(1)}
            </div>
          </div> 
        </li>`
}

function pm_barentry(item) {
    return `<li class="clearfix user-li" onclick="messenger.select_conv('${item}')">
          <div class="about">
            <div class="name name-field">
              <span class="fa fa-circle online"></span>
              ${item}
            </div>
          </div> 
        </li>`
}


class UserSelectModal {
  constructor(input, target) {
    this.input = input;
    this.target = target;
    this.selected_users = {};
  }

  render(list_of_items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = list_of_items.filter(item => item.toLowerCase().indexOf(query) > - 1);

    $(this.target).empty();

    visible_items.map( item => {
      if (!this.selected_users.hasOwnProperty(item)) {
        $(this.target).append(`
          <div class="list-group-item list-group-item-action" href="#" onclick="users_search.add_to_selected('${item}')">${item}</div>
        `);
      } else {
        $(this.target).append(`
          <div class="list-group-item list-group-item-action active" href="#" onclick="users_search.remove_selected('${item}')">${item}</div>
        `);
      }
    });

  }
  remove_selected(user) {
    delete this.selected_users[user];
    messenger.render_users_search();
  }

  add_to_selected(user) {
    this.selected_users[user] = true;
    messenger.render_users_search();
  }
  clear_selected() {
    this.selected_users = {};
  }
  make_group() {
    $.post("/newgroup", {
        title: $("#titleForm").val(),
        users: Object.keys(this.selected_users).join("&")
    });
    $('#newChatModal').modal('hide');
  }
}


var users_search = new UserSelectModal("#search-checklist", "#modal-listgroup");

class Messenger {
    constructor() {
        this.selected_conversation = null;
        this.get_conversations();
        this.get_active_contacts();
        this.conversations = [];
        this.contacts = [];

        this.conversations_bar = new SideBarList("#search-group", "#group-message-list", conv_barentry);
        this.pm_bar = new SideBarList("#search-private", "#private-message-list", pm_barentry);

        users_search = new UserSelectModal("#search-checklist", "#modal-listgroup");
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

    render_conversations() { 
        this.conversations_bar.render(this.conversations.map(values => values.title)); 
    } 
    render_pms() { this.pm_bar.render(this.contacts); } 
    render_users_search() { users_search.render(this.contacts); }

    render() {
        this.render_conversations();
        this.render_pms();
        this.render_users_search();
    }

    select_conv(conv) {
        if (this.conversations.map(values => values.title).indexOf(conv) != -1) {
            this.selected_conversation = conv;
            $("#curr_conv").text(conv.slice(1));
        } else if (this.contacts.indexOf(conv) != -1) {
            this.selected_conversation = conv;
            $("#curr_conv").text("Chat with " + conv);
        } else {
            this.selected_conversation = null;
        }
    }

    tick() {
        $.getJSON("/events", result => {
            this.render();
        });
        this.render();

        setTimeout(this.tick.bind(this), 1000);
    }
}


var messenger = new Messenger();

$(document).ready(function() {
    messenger.tick();
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})
$('#newChatModal').on('hide.bs.modal', users_search.clear_selected);


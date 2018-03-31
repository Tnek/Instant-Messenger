
// Messenger ====================================================
class Messenger {
  constructor() {
    this.selected_conversation = null;
    this.get_conversations();
    this.get_active_contacts();
    this.conversations = [];
    this.contacts = [];

    this.conv_bar = new SideBarList("#search-group", "#group-message-list", conv_barentry);
    this.pm_bar = new SideBarList("#search-private", "#private-message-list", pm_barentry);

    this.users_search = new UserSelectModal("#search-checklist", "#modal-list");


    this.tick();
  }

  get_conversations() {
    $.getJSON("/conversations", convs => {
      this.conversations = convs;
    });
  }

  get_active_contacts() {
    $.getJSON("/users", contacts => {
      this.contacts = contacts;
    });
    setTimeout(this.get_active_contacts, 1000);
  }

  render_conversations() { 
    this.conv_bar.render(this.conversations.map(values => values.title)); 
  } 

  render_pms() { this.pm_bar.render(this.contacts); } 

  render_users_search() { this.users_search.render(this.contacts); }

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

    setTimeout(this.tick.bind(this), 1000);
  }
}

var messenger = new Messenger();

// Onload ====================================================
$(document).ready(function() {
  messenger.tick();
});

// Constant ====================================================
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})


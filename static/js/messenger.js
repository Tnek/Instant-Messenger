class Conversation {
    constructor(title, users) {
        this.title = title;
        this.msgs = [];
        this.unread = false;
        this.users = users;
    }
}
// Messenger ====================================================
class Messenger {
  constructor() {
    this.selected_conversation = null;
    this.get_conversations();
    this.get_active_contacts();
    this.conversations = {};
    this.contacts = [];

    this.conv_bar = new SideBarList("#search-group", "#group-message-list", conv_barentry);
    this.pm_bar = new SideBarList("#search-private", "#private-message-list", pm_barentry);

    this.users_search = new UserSelectModal("#search-checklist", "#modal-list");
    this.chatbox = new ChatBox("#chat-history", "#chat-history-ul", "#message-to-send", "#send-button");
    this.chatbox.bind_events(this.send_message.bind(this));
    this.get_whoami();

    this.tick();
  }

  get_whoami() {
    $.get("/whoami", res => {
        this.chatbox.whoami = res;
    });
  }

  get_conversations() {
    $.getJSON("/conversations", convs => {
      convs.map(conv => {
        this.conversations[conv.title] = new Conversation(conv.title, conv.usrs);
      });
    });
  }

  get_active_contacts() {
    $.getJSON("/users", contacts => {
      this.contacts = contacts;
    });
    setTimeout(this.get_active_contacts, 1000);
  }

  render_conversations() { 
    this.conv_bar.render(Object.values(this.conversations).map(values => values.title)); 
  } 

  render_pms() { this.pm_bar.render(this.contacts); } 

  render_users_search() { this.users_search.render(this.contacts); }

  render() {
    this.render_conversations();
    this.render_pms();
    this.render_users_search();
  }

  send_message(content) {
    if (this.selected_conversation) {
      var message = {
        contents:content,
        sender:this.chatbox.whoami,
        conv:this.selected_conversation
      }
  
      $.post("/msg", message)
    }
  }

  handle_event(e) {
    switch (e.type) {
      case "msg":
        var msg = {
          contents: e.event_obj.contents,
          sender: e.event_obj.sender,
          ts: e.ts
        }
        console.log(this.conversations[e.event_obj.convo]);
        this.conversations[e.event_obj.convo].msgs.push(msg);

        if (e.event_obj.convo == this.selected_conversation) {
          this.chatbox.add_message(msg);
        }
        break;

      case "conv_create":
        var conv = e.event_obj;
        this.conversations[conv.title] = new Conversation(conv.title, conv.usrs);
        this.render_conversations();
        break;
    }

  }

  select_conv(conv) {
    if (Object.values(this.conversations).map(values => values.title).indexOf(conv) != -1) {
      this.selected_conversation = conv;
      $("#curr_conv").text(conv);
      this.chatbox.load_messages(this.conversations[conv].msgs);

    } else if (this.contacts.indexOf(conv) != -1) {
      this.selected_conversation = conv;
      $("#curr_conv").text("Chat with " + conv);
    } else {
      this.selected_conversation = null;
      return;
    }

  }

  tick() {
    $.getJSON("/events", events => {
        events.map(e => {
            this.handle_event(e);
        });
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


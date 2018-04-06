class Conversation {
  constructor(title, users, type) {
    this.title = title;
    this.msgs = [];
    this.unread = false;
    this.users = users;
    this.type = type;
  }
}
// Messenger ====================================================
class Messenger {
  constructor() {
    this.selected_conversation = null;
    this.conversations = {};
    this.contacts = {};
    this.get_conversations();
    this.get_active_contacts();

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

  whoami() {
    return this.chatbox.whoami;
  }

  get_conversations() {
    $.getJSON("/conversations", convs => {
      convs.map(conv => {
        if (!(conv.title in this.conversations)) {
          this.conversations[conv.title] = new Conversation(conv.title, conv.usrs, "channel");
        }
      });
    });
  }

  get_active_contacts() {
    $.getJSON("/users", usrs => {
      usrs.map(contact => {
        if (!(contact in this.contacts)) {
          this.contacts[contact] = new Conversation("Chat with " + contact, contact, "privmsg");
        }
      });
    });
    setTimeout(this.get_active_contacts.bind(this), 1000);
  }

  render_conversations() { 
    this.conv_bar.render(this.conversations);
  } 

  render_pms() { this.pm_bar.render(this.contacts); } 


  render_users_search() { 
    this.users_search.render(Object.keys(this.contacts).filter(item => item != this.whoami())); 
  }

  render() {
    if (!this.selected_conversation) {
        this.select_conv(Object.keys(this.conversations)[0]);
    }
    this.render_conversations();
    this.render_pms();
    this.render_users_search();
  }

  send_message(content) {
    if (this.selected_conversation) {
      if (this.selected_conversation.type == "channel") {
        let message = {
          contents:content,
          conv:this.selected_conversation.title
        }
    
        $.post("/msg", message)
      } else if (this.selected_conversation.type == "privmsg") {
        let message = {
          recipient:this.selected_conversation.users,
          contents:content
        }

        $.post("/priv_msg", message);
      }
    }
  }

  handle_event(e) {
    switch (e.type) {
      case "msg":
        let msg = {
          contents: e.event_obj.contents,
          sender: e.event_obj.sender,
          ts: e.ts
        }
        this.conversations[e.event_obj.convo].msgs.push(msg);

        if (this.selected_conversation && e.event_obj.convo == 
                                            this.selected_conversation.title) {
          this.chatbox.add_message(msg);
        }
        break;

      case "conv_create":
        let conv = e.event_obj;
        this.conversations[conv.title] = new Conversation(conv.title, conv.usrs, "channel");
        this.render_conversations();
        break;

      case "privmsg":
        console.log(e);
        let pm = {
            contents: e.event_obj.contents,
            sender: e.event_obj.sender,
            ts: e.ts
        }

        let target_pm = e.event_obj.recipient;
        if (e.event_obj.recipient == this.whoami()) {
            target_pm = e.event_obj.sender;
        }

        this.contacts[target_pm].msgs.push(pm)

        if (this.selected_conversation && "Chat with " + target_pm == 
                                            this.selected_conversation.title) {
          this.chatbox.add_message(pm);
        }
        break;
    }
  }

  _select_conv(conversation) {
    this.selected_conversation = conversation;
    this.chatbox.load_messages(conversation.msgs);
    $("#curr_conv").text(conversation.title);

  }
  select_conv(conv_title) {
    if (conv_title in this.conversations) {
      this._select_conv(this.conversations[conv_title]);
    }
  }

  select_pm(contact) {
    if (contact in this.contacts) {
      this._select_conv(this.contacts[contact]);
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


// Messenger ====================================================
class Messenger {
  constructor() {
    this.selected_conversation = null;
    this.conversations = {};
    this.contacts = {};
    this.get_whoami();
    this.get_conversations();
    this.get_active_contacts();

    this.conv_bar = new SideBarList("#search-group", "#group-message-list");
    this.pm_bar = new SideBarList("#search-private", "#private-message-list");

    this.users_search = new UserSelectModal("#search-checklist", "#modal-list", this.render_users_search.bind(this));
    this.chatbox = new ChatBox("#chat-history", "#chat-history-ul", "#message-to-send", "#send-button");
    this.chatbox.bind_events(this.send_message.bind(this));
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
      let new_convos = {}
      convs.map(conv => {
        if (conv.title in this.conversations) {
          new_convos[conv.title] = this.conversations[conv.title];
        } else {
          let conv_obj = new Channel(conv.title, conv.usrs);
          new_convos[conv.title] = conv_obj;
        }
      });
      this.conversations = new_convos;
      this.render_conversations();
    });
  }

  get_active_contacts() {
      let new_contacts = {};
      $.getJSON("/users", usrs => {
        usrs.map(contact => {
          if (contact in this.contacts) {
            new_contacts[contact] = this.contacts[contact];
          } else {
            new_contacts[contact] = new PrivateMessages(contact);
          }
        });
        this.contacts = new_contacts;
        this.render_pms();
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
    this.render_conversations();
    this.render_pms();
    this.render_users_search();
  }

  send_message(content) {
    if (this.selected_conversation) {
      let msg = this.selected_conversation.send_msg(content);
      msg.sender = this.whoami();
      this.chatbox.add_message(msg);
    }
  }

  select_conv(conversation) {
    if (this.selected_conversation) {
      this.selected_conversation.unselect();
    }
    this.selected_conversation = conversation;
    this.chatbox.load_messages(conversation.msgs);

    $("#curr_conv").text(conversation.title);
  }

  tick() {
    $.getJSON("/events", events => {
      events.map(e => {
        this.handle_event(e);
      });
    });

    setTimeout(this.tick.bind(this), 1000);
  }

  handle_event(e) {
    console.log(e)
    var relevant_conv;
    switch (e.type) {
      case "conv_create":
        let conv = e.event_obj;
        this.conversations[conv.title] = new Channel(conv.title, conv.usrs);
        this.conversations[conv.title].unread = true; 

        this.render_conversations();
        return;

      case "privmsg":
        let target = e.event_obj.recipient == this.whoami() ? 
                e.event_obj.sender : e.event_obj.recipient;
        relevant_conv = this.contacts[target];
        break;
      case "msg":
        relevant_conv = this.conversations[e.event_obj.convo];
        break;
      default:
        return
    }

    let msg = {
      contents: e.event_obj.contents,
      sender: e.event_obj.sender,
      ts: e.ts
    }

    relevant_conv.add_msg(msg);

    if (e.event_obj.sender != this.whoami()) {
      relevant_conv.unread = true;
      this.render_conversations();
      this.render_pms();

      if (this.selected_conversation && relevant_conv === this.selected_conversation) { 
        this.chatbox.add_message(msg);
      }
    }
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


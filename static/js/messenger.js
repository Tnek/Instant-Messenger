// Messenger ====================================================
class Messenger {
  constructor() {
    this.selected_conversation = null;
    this.conversations = {};
    this.contacts = {};
    this.chatbox = new ChatBox("#chat-history", "#chat-history-ul", "#message-to-send", "#send-button", "#chat-about");
    this.get_whoami();
  }
  get_whoami() {
    $.get("/whoami", res => {
      this.chatbox.whoami = res;
    }).done(this.init.bind(this));
  }

  init() {
    this.get_conversations();
    this.get_active_contacts();

    this.conv_bar = new SideBarList("#search-group", "#group-message-list");
    this.pm_bar = new SideBarList("#search-private", "#private-message-list");

    this.create_group_modal = new CreateGroupModal("newChatModal", "#people-list", this.render_users_search.bind(this))    
    this.public_conversations_modal = new PublicConversationModal("publicModal", "#people-list", "#open_global_channel_modal");
    this.chatbox.bind_events(this.send_message.bind(this));
    this.tick();
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
        this.render_users_search();
      });
    setTimeout(this.get_active_contacts.bind(this), 1000);
  }

  render_conversations() { 
    this.conv_bar.render(this.conversations);
  } 

  render_pms() { this.pm_bar.render(this.contacts); } 

  render_users_search() { 
    this.create_group_modal.search_list.render(Object.keys(this.contacts).filter(item => item != this.whoami())); 
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
    this.selected_conversation.select()
    this.chatbox.load_conversation(this.selected_conversation);

    this.render_conversations();
    this.render_pms();
  }

  tick() {
    $.getJSON("/events", events => {
      events.map(e => {
        this.handle_event(e);
      });
    });

    setTimeout(this.tick.bind(this), 500);
  }

  handle_event(e) {
    console.log(e);
    var relevant_conv;
    switch (e.type) {
      case "conv_create":
        let conv = e.event_obj;
        relevant_conv = new Channel(conv.title, conv.usrs);
        this.conversations[conv.title] = relevant_conv; 
        this.render_conversations();
        break;

      case "conv_join":
        this.conversations[e.event_obj.convo].add_user(e.event_obj.sender);
        this.chatbox.render_top_panel();
        relevant_conv = this.conversations[e.event_obj.convo];
        break;

      case "conv_leave":
        this.conversations[e.event_obj.convo].remove_user(e.event_obj.sender);
        this.chatbox.render_top_panel();
        relevant_conv = this.conversations[e.event_obj.convo];
        break;

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

    let msg = e.event_obj;
    msg.ts = e.ts;
    msg.type = e.type;

    relevant_conv.add_msg(msg);

    if (msg.sender != this.whoami()) {
      relevant_conv.unread += 1;
      this.render_conversations();
      this.render_pms();

      if (this.selected_conversation && relevant_conv === this.selected_conversation) { 
        this.chatbox.add_message(msg);
      }
    } else {
      /* 
       * Refresh conversation to update timestamps when your own messages are 
       * echoed back from the server 
       */
      this.select_conv(this.selected_conversation);
    }
  }
}

var messenger = new Messenger();

// Onload ====================================================
$(document).ready(function() {
    messenger.init();
});

// Constant ====================================================
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})


class Conversation {
  constructor(title, users) {
    this.title = title;
    this.msgs = [];
    this.unread = false;
    this.selected = false;
    this.users = users;
    this.is_conv();
  }
  is_pm() {
    this.callback_func = "messenger.select_pm";
    this.icon = "fa fa-circle";
    this.type = "privmsg";
  }

  is_conv() {
    this.callback_func = "messenger.select_conv";
    this.icon = "fa fa-comments";
    this.type = "channel";
  }

  select() {
    this.selected = true;
    this.unread = false;
  }

  render() {
    var icon_status = "readicon";
    if (this.unread) {
      icon_status = "unread";
    }

    var attrib = "user-li";
    if (this.selected) {
        attrib = "user-li-selected";
    }
    return `<li class="clearfix ${attrib}" onclick="${this.callback_func}('${this.title}')">
            <div class="about">
              <div class="name name-field">
               <span class="${this.icon} ${icon_status}"></span> ${this.title}
              </div>
            </div> 
          </li>`
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

    this.conv_bar = new SideBarList("#search-group", "#group-message-list");
    this.pm_bar = new SideBarList("#search-private", "#private-message-list");

    this.users_search = new UserSelectModal("#search-checklist", "#modal-list");
    this.chatbox = new ChatBox("#chat-history", "#chat-history-ul", "#message-to-send", "#send-button");
    this.chatbox.bind_events(this.send_message.bind(this));
    this.get_whoami();

    this.run();
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
          let conv_obj = new Conversation(conv.title, conv.usrs);
          conv_obj.is_conv();
          this.conversations[conv.title] = conv_obj;
        }
      });
    });
  }

  get_active_contacts() {
    $.getJSON("/users", usrs => {
      let new_contacts = {}
      usrs.map(contact => {
        if (contact in this.contacts) {
          new_contacts[contact] = this.contacts[contact];
        } else {
          let conv_obj = new Conversation(contact, contact);
          conv_obj.is_pm();
          new_contacts[contact] = conv_obj;
        }
      });
      this.contacts = new_contacts;
      this.render();
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
      var message;
      if (this.selected_conversation.type == "channel") {
        message = {
          contents:content,
          conv:this.selected_conversation.title
        }
    
        $.post("/msg", message)

      } else if (this.selected_conversation.type == "privmsg") {
        message = {
          recipient:this.selected_conversation.users,
          contents:content
        }
        $.post("/priv_msg", message);
      }

      message.sender = this.whoami();
      this.chatbox.add_message(message);
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
        if (e.event_obj.sender != this.whoami()) {
          this.conversations[e.event_obj.convo].unread = true;
          this.render_conversations();

          if (this.selected_conversation && e.event_obj.convo == 
                                              this.selected_conversation.title) {
            this.chatbox.add_message(msg);
          } 
        }

        break;

      case "conv_create":
        let conv = e.event_obj;
        this.conversations[conv.title] = new Conversation(conv.title, conv.usrs);
        this.conversations[conv.title].unread = true; 

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
            this.contacts[target_pm].unread = true;
            this.render_pms();
            if (this.selected_conversation && this.contacts[target_pm].title == 
                                                this.selected_conversation.title) {
              this.chatbox.add_message(pm);
            }
        }

        this.contacts[target_pm].msgs.push(pm)

        break;
    }
  }


  re_render_conv_bar(conversation) {
      if (conversation.type == "channel") {
          this.render_conversations();
      } else if (conversation.type == "privmsg") {
          this.render_pms();
      }
  }
  _select_conv(conversation) {
    let old_conv = this.selected_conversation;

    this.selected_conversation = conversation;
    this.selected_conversation.select();

    if (old_conv) {
        old_conv.selected = false;
        this.re_render_conv_bar(old_conv);
    }
    this.re_render_conv_bar(this.selected_conversation);

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


  run() {
    this.render();
    this.tick();
  }
  tick() {
    $.getJSON("/events", events => {
      events.map(e => {
        this.handle_event(e);
      });
    });

    setTimeout(this.tick.bind(this), 1000);
  }
}

var messenger = new Messenger();

// Onload ====================================================
$(document).ready(function() {
  messenger.run();
});

// Constant ====================================================
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})


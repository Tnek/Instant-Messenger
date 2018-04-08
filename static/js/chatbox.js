// ChatBox ====================================================
class ChatBox {
  constructor(chat_history, chat_history_list, send_box, send_button, curr_conv_label) {
    this.chat_history = chat_history; //chat history div
    this.chat_history_list = chat_history_list; //chat history ul
    this.send_box = send_box; 
    this.selected_conv = null;

    this.curr_conv_label = curr_conv_label;
    this.send_button = send_button;
    this.whoami = "";
  }

  bind_events(msg_callback) {
    this.msg_callback = msg_callback;
    //send message with send button
    $(this.send_button).on('click', this.send_msg.bind(this));
    //send message with enter key
    $(this.send_box).on('keyup', this.key_event.bind(this));
  }

  key_event(event) {
    // enter was pressed
    if (event.keyCode === 13) {
      this.send_msg();
    }
  }

  send_msg() {
    //send only if nonspace characters are entered
    if ($(this.send_box).val().trim() !== '') {
      this.msg_callback($(this.send_box).val());
      $(this.send_box).val('');
    }
  }

  //load messages once
  load_messages(messages) {
    $(this.chat_history_list).empty();
    messages.map(message => this._add_message(message));
    this.scrollToBottom();
  }

  //append subsequent messages
  add_message(msg) {
    this._add_message(msg);
    this.scrollToBottom();
  }

  //helper function to add individual messages based on message type
  _add_message(msg) {
    var rendered_msg;
    var system_message;

    console.log("addmsg", msg);
    switch (msg.type) {
      case "privmsg":
      case "msg":
        if (msg.sender === this.whoami) {
            rendered_msg = this._my_message(msg);
        } else { 
            rendered_msg = this._user_message(msg);
        }
        break;

      case "conv_leave":
        system_message = {contents: msg.sender + " has left the conversation."};
        rendered_msg = this._system_message(system_message);
        break;

      case "conv_join":
        console.log(msg);
        system_message = {contents: msg.sender + " has joined the conversation."};
        rendered_msg = this._system_message(system_message);
        break;

      case "conv_create":
        system_message = {contents: "A conversation has been created."};
        rendered_msg = this._system_message(system_message);
        break;

      default:
        rendered_msg = null;
        break;
    }

    if (rendered_msg) {
      $(this.chat_history_list).append(rendered_msg);
    }
  }

  //Handlebar template compilations----------

  _system_message(system_message) {
    return Handlebars.compile( $("#system-message-template").html())(system_message);
  }

  _user_message(msg) {
    return Handlebars.compile( $("#message-response-template").html())(msg);
  }
  _my_message(msg) {
    return Handlebars.compile( $("#message-template").html())(msg);
  }

  //----------------------------------------

  //jump to last message
  scrollToBottom() {
    $(this.chat_history).scrollTop($(this.chat_history)[0].scrollHeight);
  }

  //render group name and participants
  render_top_panel() {
    $(this.curr_conv_label).empty();
    $(this.curr_conv_label).append(`
      <div class="chat-with" id="curr_conv" name="curr_conv">
        ${this.selected_conv.title}
      </div>
    `);
    if (this.selected_conv.users) {
      $(this.curr_conv_label).append(`
        <div>
          <span class="fa fa-user online"/>
          ${this.selected_conv.users.length} - ${this.selected_conv.users.join(", ")}
        </div>
      `);
    }
  }

  load_conversation(conversation) {
    this.selected_conv = conversation;
    this.render_top_panel();
    this.load_messages(this.selected_conv.msgs);
  }

}

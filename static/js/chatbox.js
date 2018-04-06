// ChatBox ====================================================
class ChatBox {
	constructor(chat_history, chat_history_list, send_box, send_button){
    this.chat_history = chat_history; //chat history div
    this.chat_history_list = chat_history_list; //chat history ul
    this.send_box = send_box; 
    this.send_button = send_button;
    this.whoami = "";
  }

  bind_events(msg_callback){
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

  //helper function to add individual messages
  _add_message(msg) {
    if (msg.sender == this.whoami) { //self
      var template = Handlebars.compile( $("#message-template").html());
      $(this.chat_history_list).append(template(msg));
    } else { //other
      var templateResponse = Handlebars.compile( $("#message-response-template").html());
      $(this.chat_history_list).append(templateResponse(msg));
    }
  }

  //jump to last message
  scrollToBottom() {
    $(this.chat_history).scrollTop($(this.chat_history)[0].scrollHeight);
  }

}

//var chatBox = new ChatBox("#chat-history", "#chat-history-ul", "#message-to-send", "#send-button");

/*
// Onload ====================================================
(function(){
  chatBox.load_messages(dummy_conv);
})();

function dummy_callback(msg) {
  var message = {"sender":"Alice", 
    "contents":msg, "ts":"12:01 AM"};
  dummy_conv.push(message);
  chatBox.add_message(message);
}

chatBox.bind_events(dummy_callback);
*/

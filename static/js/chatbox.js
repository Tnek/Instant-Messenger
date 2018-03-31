// ChatBox ====================================================
class ChatBox{
	constructor(chat_history, send_box, send_button){
    this.chat_history = chat_history;
    this.send_box = send_box;
    this.send_button = send_button;
	}

  bind_events(msg_callback){
    this.msg_callback = msg_callback;
    $(this.send_button).on('click', this.send_msg.bind(this));
    $(this.send_box).on('keyup', this.key_event.bind(this));
	}

  key_event(event) {
    // enter was pressed
    if (event.keyCode === 13) {
      this.send_msg();
    }
  }

  send_msg() {
    if ($(this.send_box).val().trim() !== '') {
      this.msg_callback($(this.send_box).val());
      $(this.send_box).val('');
    }
  }

  load_messages(messages) {
    $(this.chat_history).empty();
    messages.map(message => this._add_message(message));
    this.scrollToBottom();
  }

  add_message(msg) {
    this._add_message(msg);
    this.scrollToBottom();
  }

  _add_message(msg) {
    if (msg['sender'] == "Alice"){
      var template = Handlebars.compile( $("#message-template").html());
      $(this.chat_history).append(template(msg));

    } else{
      var templateResponse = Handlebars.compile( $("#message-response-template").html());
      $(this.chat_history).append(templateResponse(msg));      
    }
  }

  scrollToBottom() {
    $("#chat-history").scrollTop($("#chat-history")[0].scrollHeight);
  }

}

var chatBox = new ChatBox("#chat-history-ul", "#message-to-send", "#send-button");

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

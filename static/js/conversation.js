class Conversation {
  constructor(label, icon) {
    this.label = label;
    this.icon = icon;

    this.unread = false;
    this.selected = false;
    this.msgs = [];
  }

  render() {
    let icon_status = this.unread ? "unread":"readicon";
    let attrib = this.selected ? "user-li-selected" : "user-li";

    this.ret_element = $(`<li class="clearfix ${attrib}">
            <div class="about name name-field">
               <span class="${this.icon} ${icon_status}" /> ${this.label}
            </div> 
          </li>`)

    this.ret_element.click(function() {
      this.select();
    }.bind(this));
    return this.ret_element;

  }
  select() {
    this.ret_element.addClass("user-li-selected");
    this.unread = false;
    this.selected = true;
    messenger.select_conv(this);
  }

  unselect() {
    this.ret_element.removeClass("user-li-selected");
    this.selected = false;
  }

  add_msg(msg) {
    this.msgs.push(msg);
  }
}

class Channel extends Conversation {
  constructor(title, users) {
    super(title, "fa fa-comments");
    this.title = title;
    this.users = users;
  }
  send_msg(content) {
    let msg = {
      contents:content,
      conv:this.label
    }
    $.post("/msg", msg);
    return msg;
  }
}

class PrivateMessages extends Conversation {
  constructor(recipient) {
    super(recipient, "fa fa-user");
    this.title = "Chat with " + recipient;
    this.recipient = recipient;
  }
  send_msg(content) {
    let msg = {
      contents:content,
      recipient:this.recipient
    }
    $.post("/priv_msg", msg);
    return msg;
  }
}

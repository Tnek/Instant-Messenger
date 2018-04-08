class Conversation {
  constructor(label, icon) {
    this.label = label;
    this.icon = icon;

    this.unread = 0;
    this.selected = false;
    this.msgs = [];
  }

  render() {
    let icon_status = this.unread ? "unread":"readicon";
    let attrib = this.selected ? "user-li-selected" : "user-li";
    let unread_count = this.unread > 0 ? this.unread : "";

    this.ret_element = $(`
          <li class="clearfix ${attrib}">
            <div class="about name name-field">
              <span class="${this.icon} ${icon_status}">${unread_count}</span> ${this.label}
            </div> 
          </li>`)

    this.ret_element.click(function() {
      this._select();
    }.bind(this));
    return this.ret_element;
  }

  _select() {
    this.select()
    messenger.select_conv(this);
  }

  select() {
    this.ret_element.addClass("user-li-selected");
    this.unread = 0;
    this.selected = true;
  }

  unselect() {
    this.ret_element.removeClass("user-li-selected");
    this.selected = 0;
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
  remove_user(uname) {
    this.users.splice(this.users.indexOf(uname), 1);
  }
  add_user(uname) {
    this.users.push(uname);
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

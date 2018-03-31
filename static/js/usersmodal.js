// UserSelectModal ====================================================
class UserSelectModal {
  constructor(input, target) {
    this.input = input;
    this.target = target;
    this.selected_users = {};
  }

  render(list_of_items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = list_of_items.filter(item => item.toLowerCase().indexOf(query) > - 1);

    $(this.target).empty();

    visible_items.map( item => {
      if (!this.selected_users.hasOwnProperty(item)) {
        $(this.target).append(`
          <i class="list-group-item list-group-item-action" onclick="messenger.users_search.add_to_selected('${item}')">${item}</i>
        `);
      } else {
        $(this.target).append(`
          <i class="list-group-item list-group-item-action active" onclick="messenger.users_search.remove_selected('${item}')">${item}</i>
        `);
      }
    });
  }

  remove_selected(user) {
    delete this.selected_users[user];
    messenger.render_users_search();
  }

  add_to_selected(user) {
    this.selected_users[user] = true;
    messenger.render_users_search();
  }
  clear_selected() {
    this.selected_users = {};
    $("input").val('');
  }
  make_group() {
    if ($("#titleForm")) {
      $.post("/newgroup", {
        title: $("#titleForm").val(),
        users: Object.keys(this.selected_users).join("&")
      });
      $('#newChatModal').modal('hide');
    }
    this.clear_selected();
  }
}



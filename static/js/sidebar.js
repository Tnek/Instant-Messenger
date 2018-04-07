class SearchableItem {
  constructor(input, target) {
    this.input = input;
    this.target = target;
  }
  render(items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = this.filter_function(query, items);
    $(this.target).empty();
    this.render_function(visible_items);
  }
}

// SideBarList ====================================================
class SideBarList extends SearchableItem {
  constructor(input, target) {
    super(input, target);
  }
  filter_function(query, map_of_items) {
    return Object.keys(map_of_items).filter(item => item.toLowerCase().indexOf(query) > -1).map(
        filtered_item => map_of_items[filtered_item]);
  }

  render_function(visible_items) {
    visible_items.map(item => {
      $(this.target).append(item.render());
    });
  }
}

// UserSelectModal ====================================================
class UserSelectModal extends SearchableItem {
  constructor(input, target) {
    super(input, target);
    this.selected_users = {};
  }

  filter_function(query, items) {
    return items.filter(item => item.toLowerCase().indexOf(query) > -1);
  }

  render_function(visible_items) {
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



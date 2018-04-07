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

class SelectableList extends SearchableItem {
  constructor(input, target, refresh_function) {
    super(input, target);
    this.refresh_function = refresh_function;
    this.selected_items = {};
  }

  filter_function(query, items) {
    return items.filter(item => item.toLowerCase().indexOf(query) > -1);
  }

  render_function(visible_items) {
    visible_items.map( item => {
      let button =  $(`<i class="list-group-item list-group-item-action">${item}</i>`)

      $(this.target).append(button);
      if (item in this.selected_items) {
        button.addClass("active");
        button.click(function() { this.remove_selected(item) }.bind(this));

      } else {
        button.click(function() { this.add_to_selected(item) }.bind(this));
      }
    });
  }

  remove_selected(item) {
    delete this.selected_items[item];
    this.refresh_function();
  }

  add_to_selected(item) {
    this.selected_items[item] = true;
    this.refresh_function();
  }
  clear_selected() {
    this.selected_items = {};
    $(this.input).val('');
  }
}



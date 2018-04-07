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



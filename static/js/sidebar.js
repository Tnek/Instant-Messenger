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
  constructor(input, target, list_entry_generator) {
    super(input, target);
    this.list_entry_generator = list_entry_generator;
  }
  filter_function(query, map_of_items) {
    return Object.keys(map_of_items).filter(item => item.toLowerCase().indexOf(query) > -1).map(
        filtered_item => map_of_items[filtered_item]);
  }

  render_function(visible_items) {
    visible_items.map(item => {
      $(this.target).append(this.list_entry_generator(item));
    });
  }
}

function conv_barentry(item) {
  var icon = "fa fa-comments readicon";
  if (item.unread) {
    icon = "fa fa-comments unread";
  }
 
  return `<li class="clearfix user-li" onclick="messenger.select_conv('${item.title}')">
            <div class="about">
              <div class="name name-field">
               <span class="${icon}"></span> ${item.title}
              </div>
            </div> 
          </li>`
}

function pm_barentry(item) {
  var icon = "fa fa-circle readicon";
  if (item.unread) {
    icon = "fa fa-circle unread";
  }
  
  return `<li class="clearfix user-li" onclick="messenger.select_pm('${item.users}')">
            <div class="about">
              <div class="name name-field">
                <span class="${icon}"></span> ${item.users}
              </div>
            </div> 
          </li>`
}



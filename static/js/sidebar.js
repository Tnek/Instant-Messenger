// SideBarList ====================================================
class SideBarList {
  constructor(input, target, list_entry_generator) {
    this.input = input;
    this.target = target;
    this.list_entry_generator = list_entry_generator;
  }

  render(list_of_items) {
    let query = $(this.input).val().toLowerCase();
    let visible_items = list_of_items.filter(item => item.toLowerCase().indexOf(query) > - 1);

    $(this.target).empty();

    visible_items.map( item => {
      $(this.target).append(this.list_entry_generator(item));
    });
  }
}

function conv_barentry(item) {
  return `<li class="clearfix user-li" onclick="messenger.select_conv('${item}')">
            <div class="about">
              <div class="name name-field">
               <span class="fa fa-comments online"></span>
               ${item}
              </div>
            </div> 
          </li>`
}

function pm_barentry(item) {
  return `<li class="clearfix user-li" onclick="messenger.select_pm('${item}')">
            <div class="about">
              <div class="name name-field">
                <span class="fa fa-circle online"></span>
                ${item}
              </div>
            </div> 
          </li>`
}


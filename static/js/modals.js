class Modal {
  constructor(target, parent_div, title) {
    this.target = target;
    this.parent_div = parent_div;
    this.title = title;
    this.target_sel = "#" + target;

    this.close_callbacks = [];
    this.submit_callbacks = [];
    this.build();
  }
  onClose(callback) {
    this.close_callbacks.append(callback);
  }
  onSubmit(callback) {
    this.submit_callbacks.append(callback);
  }
  build() {
    $(this.parent_div).append(Handlebars.compile( $("#modal-template").html())(this));
  }

  add_to_body(item) {
    $(this.target_sel+'-body').append(item);
  }

  build_footer(submit_name) {
    let cancel_button = $(`<button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>`);
    cancel_button.click(function() {
        this.close_callbacks.map(c => c());
    }.bind(this));
    $(this.target_sel+"-footer").append(cancel_button);
    
    let submit_button = $(`<button type="button" class="btn btn-primary">${submit_name}</button>`);
    submit_button.click(function() {
        this.submit_callbacks.map(c => c());
    }.bind(this));
    $(this.target_sel+"-footer").append(submit_button);
  }
}

class CreateGroupModal extends Modal {
    constructor(target, parent_div, refresh_function) {
      super(target, parent_div, "Create Channel");
      this.search_list = new SelectableList(this.target_sel+'-search', this.target_sel+'-list', refresh_function);
      this.titleform = this.target+'-title';


      this.close_callbacks.push(this.clear_forms.bind(this));
      this.submit_callbacks.push(this.make_group.bind(this));

      this.build_body();
      this.build_footer("Create");

    }
    build_body() {
      this.add_to_body(`<div class="form-group">
                  <label class="formHeader" for=${this.titleform}>Channel Name</label>
                  <input class="form-control" id=${this.titleform} type="text" autocomplete=off placeholder="Enter title"></input>
                </div>`)

      this.add_to_body(this.search_list.build());
    }


    make_group() {
      if ($(this.titleform).val()) {
        $.post("/newgroup", {
          title: $(this.titleform).val(),
          users: Object.keys(this.search_list.selected_items).join("&"),
          is_public: false
        }).done(function() {
          $(this.target).modal('hide');
          this.clear_forms();
        }.bind(this));
      }
    }

    clear_forms() {
      this.search_list.clear_selected();
    }
}

/*
class UserSelectModal extends SelectableList {
  constructor(input, target, refresh_function) {
    super(input, target, refresh_function);
  }

  make_group() {
    if ($("#titleForm")) {
      $.post("/newgroup", {
        title: $("#titleForm").val(),
        users: Object.keys(this.selected_items).join("&")
      });
      $('#newChatModal').modal('hide');
    }
    this.clear_selected();
  }
}
*/

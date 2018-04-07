class UserSelectModal extends SelectableList {
  constructor(input, target, refresh_function) {
    super(input, target, refresh_function);
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


/** =====================================================================
  Dummy Database **/

var contactDatabase = ["Arisu", "Tnek", "BleepBloop", "Spathis"];
var contactDatabase2 = ["Roy, Hui", "Felicity, Bi Ling, Alice"];

//Private message list
$(function(){
  //arrow function
  contactDatabase.map( contact => {
  	$('#private-message-list').append(`
		<li class="clearfix">
	        <div class="about">
	          <div class="name"> ${contact} </div>
	          <div class="status">
	            <i class="fa fa-circle online"></i> online
	          </div>
	        </div>
      	</li>
  	`);
  })
});

//Group message list
$(function(){
  //arrow function
  contactDatabase2.map( contact => {
  	$('#group-message-list').append(`
		<li class="clearfix">
	        <div class="about">
	          <div class="name"> ${contact} </div>
	          <div class="status">
	            <i class="fa fa-circle online"></i> online
	          </div>
	        </div>
      	</li>
  	`);
  })
});

function searchPrivate() {
    var input, filter, list, contact, i;
    input = document.getElementById("search-private");
    filter = input.value.toUpperCase();
    list = document.getElementById("private-message-list");
    contact = list.getElementsByClassName("name");
    for (i = 0; i < contact.length; i++) {
        if (contact[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            contact[i].parentElement.parentElement.style.display = "";
        } else {
            contact[i].parentElement.parentElement.style.display = "none";
        }
    }
}


/*
let x = 12;
console.log(`hello ${x}`);

`
<li>
	${object.display_name}
	${messages.map( (msg) => {
		return `
		<li>
			${msg.user}
			${msg.text}
		</li>
		`;	
	})}
</li>
`

*/

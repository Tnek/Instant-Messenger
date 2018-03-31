dummy_conv = [
    {
        "sender":"Kent",
        "msg":"Hi Alice",
        "ts":"6:01 PM"
    },
    {
        "sender":"Alice",
        "msg":"You're stupid",
        "ts":"6:02 PM"
    },
    {
        "sender":"Kent",
        "msg":":(",
        "ts":"6:04 PM"
    },
    {
        "sender":"Alice",
        "msg":"Why did you take 10 years to reply? I'm an old woman now",
        "ts":"6:04 PM"
    },
    {
        "sender":"Kent",
        "msg":":(",
        "ts":"6:04 PM"
    }
]

var cycle = -1; //tmp var for chat 
(function(){
  
  var chat = {
    messageToSend: '',
    messageResponses: [
      "Hello, would you like to hear a TCP joke?",
      "OK, I'll tell you a TCP joke.",
      "Are you ready to hear a TCP joke?",
      "OK, I'm about to send the TCP joke. It will last 10 seconds, it has two characters, it does not have a setting, it ends with a punchline.",
      "I'm sorry, your connection has timed out..."
    ],

    //main function ----------------------------
    init: function() {
      this.cacheDOM();
      this.bindEvents();
      this.render();
    },

    //major functions-------------------------------
    cacheDOM: function() {
      this.$chatHistory = $('.chat-history');
      this.$button = $('button');
      this.$textarea = $('#message-to-send');
      this.$chatHistoryList = this.$chatHistory.find('ul');
    },

    //bind() function depricated, use on() 
    bindEvents: function() {
      this.$button.on('click', this.addMessage.bind(this));
      this.$textarea.on('keyup', this.addMessageEnter.bind(this));
    },

    render: function() {
      this.scrollToBottom();
      if (this.messageToSend.trim() !== '') { //if nonspace charas are typed
        var template = Handlebars.compile( $("#message-template").html());
        var context = { 
          username: "Arisu",
          messageOutput: this.messageToSend,
          time: this.getCurrentTime()
        };

        this.$chatHistoryList.append(template(context));
        this.scrollToBottom();
        this.$textarea.val('');
        
        // responses
        var templateResponse = Handlebars.compile( $("#message-response-template").html());
        var contextResponse = { 
          username: "Tnek",
          response: this.getRandomItem(this.messageResponses),
          time: this.getCurrentTime()
        };
        
        setTimeout(function() {
          this.$chatHistoryList.append(templateResponse(contextResponse));
          this.scrollToBottom();
        }.bind(this), 500);
        
      }
      
    },
    
    //helper functions ----------------------------------
    addMessage: function() {
      this.messageToSend = this.$textarea.val()
      this.render();         
    },
    addMessageEnter: function(event) {
        // enter was pressed
        if (event.keyCode === 13) {
          this.addMessage();
        }
    },
    scrollToBottom: function() {
       this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
    },
    getCurrentTime: function() {
      return new Date().toLocaleTimeString().
              replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
    },

    getRandomItem: function(arr) {
      if (cycle >= arr.length -1){
        cycle = 0;
      }else{
        cycle++;
      }
      return arr[cycle];
    }
    
  };
  
  chat.init();
  
})();

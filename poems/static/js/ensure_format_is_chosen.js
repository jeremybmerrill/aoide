$(function(){

  var EnsureFormatIsChosen = Backbone.View.extend({
    el: $('div#formatChoice'),
    events: {
      'change input.formatName': 'validate'
    },
    validate: function(){
      if($('input.formatName:checked').length == 0){
        $("input#submitPoem").attr("disabled",true);
      }else{
        $("input#submitPoem").removeAttr("disabled");
      }
    },
    initialize: function(){
      _.bindAll(this, 'validate');
      this.validate();
    },
  })

  var ensurer = new EnsureFormatIsChosen();
});
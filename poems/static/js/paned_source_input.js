$(function(){

  var PanedSourceInput = Backbone.View.extend({
      el: $('a#switchPane'), 
      events: {
        'click' : 'togglePanes',
      },

      hidden_text: '',

      togglePanes: function(){
        $this = $(this.el);
        $('div#source-text').toggleClass('hidden');
        $('div#source-url').toggleClass('hidden');

        /*
        * What the hell is going on here, Jeremy? 
        * I don't want to run anything on the submit click.
        * But, I want the contents of the "hidden" pane to be an empty string
        * for easy testing of which is active in Django.
        * So, stash the content of the hidden pane, erase the hidden pane's content
        * and when the hidden pane is unhidden, restore the stashed content.
        */
        if($('div#source-text').hasClass('hidden')){
          $('div#source-url input').val(this.hidden_text);
          this.hidden_text = $('div#source-text textarea').val();
          console.log(this.hidden_text);
          $('div#source-text textarea').val('');
        }else{
          $('div#source-text textarea').val(this.hidden_text);
          this.hidden_text = $('div#source-url input').val();
          console.log(this.hidden_text);
          $('div#source-url input').val('')
        }

        //handles switching the "Enter a URL here"-type text
        var other = $this.data('other');
        $this.data('other', $this.text());
        $this.text(other);
      },

      initialize: function(){
        _.bindAll(this, 'togglePanes');

        if( $('textarea#source-text-textarea').val().length > 10 && $('div#source-text').hasClass('hidden')) {
          this.togglePanes();
        }
      },

    });
  var p = new PanedSourceInput();

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


  $('#partialLinesFlag').tooltip('hide');
  var ensurer = new EnsureFormatIsChosen();
});  

$(function(){

  var PanedSourceInput = Backbone.View.extend({
      el: $('a#switchPane'), 
      events: {
        'click' : 'togglePanes',
      },

      togglePanes: function(){
        $this = $(this.el);
        $('div#source-text').toggleClass('hidden');
        $('div#source-url').toggleClass('hidden');
        var other = $this.data('other');
        $this.data('other', $this.text());
        $this.text(other);
      },

      initialize: function(){
        _.bindAll(this, 'togglePanes');
        if( $('textarea#source-text-textarea').text().length > 10) {
          this.togglePanes();
        }
      },

    });
  var p = new PanedSourceInput();

  // var ensureFormatIsChosen = Backbone.View.extend({
  //   el: $('form'),
  //   events: {
  //     'click input#submitPoem': 'validate'
  //   },
  //   validate: function(){
  //     console.log("stub for validation");
  //     "div#formatChoice"
  //   }
  // })

  $('#partialLinesFlag').tooltip('hide');
});  

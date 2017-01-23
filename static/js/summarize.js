$(function() {

	// Function to call summarize function using Ajax and display results.
    $('#btnSummarize').click(function() {
        $.ajax({
            url: '/summarize',
            data: $('form').serialize(),
	    method: 'POST',
            success: function(response) {

               var list = $('<ul />'); // create UL
			   extractResult(list, $.parseJSON(response));   // run function and fill the UL with LI's
               $('#result').html(list)
               $(window).scrollTop($('#result').offset().top-20)

            },
            error: function(error) {
                console.log(error);
            }
        });
    });  
    
    // Function to call LDA summarize function using Ajax and display results.
     $('#btnLDASummarize').click(function() {
        $.ajax({
            url: '/ldasummarize',
            data: $('form').serialize(),
	    method: 'POST',
            success: function(response) {

            	var list = $('<ul />'); // create UL
				extractResult(list, $.parseJSON(response));   // run function and fill the UL with LI's
               $('#result').html(list)
               $(window).scrollTop($('#result').offset().top-20)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
   

	// helper function to display results in a list fashion
	function extractResult(list, result){     
    	jQuery.each(result, function(key, value) {
        // create a LI for each iteration and append to the UL
        $('<label />', {text: key}).appendTo(list);
        	jQuery.each(value, function(key, point) {
        		$('<li />', {text: point}).appendTo(list);});
        $('<br/>').appendTo(list);	
       
    });
	}
	
	//To load Facebook's TOS in the input text area
	$('#fbImg').click(function() {
	 	jQuery.get('static/data/Facebook.txt', function(data) {
   			$('#inputText').val(data)
		});
	})
	
	//To load Google's TOS in the input text area
	$('#goImg').click(function() {
	 	jQuery.get('static/data/Google.txt', function(data) {
   			$('#inputText').val(data)
		});
	})
	
	//To load Slack's TOS in the input text area
	$('#slImg').click(function() {
	 	jQuery.get('static/data/Slack.txt', function(data) {
   			$('#inputText').val(data)
		});
	})
	
	//To load Spotify's TOS in the input text area
	$('#spImg').click(function() {
	 	jQuery.get('static/data/Spotify.txt', function(data) {
   			$('#inputText').val(data)
		});
	})
	
	//To load Twitter's TOS in the input text area
	$('#twImg').click(function() {
	 	jQuery.get('static/data/Twitter.txt', function(data) {
   			$('#inputText').val(data)
		});
	})
});

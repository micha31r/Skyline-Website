$(function() {
	// Show a pop-up prompt when its trigger is clicked
	$(".prompt-toggle").each(function() {
		$(this).click(function() {
			const id = $(this).prop("value");
			// Get the correct prompt by id if there are multiple on the page
			const identifier = "#d-prompt" + (id ? '-'+id : '');
			var element = $(identifier);
			if (element.css("display") == "none") {
				element.css("display", "flex");
			}
		});
	});
	// Close the prompt if clicked outside of the prompt
	$(".d-prompt").click(function(e) {
		if (e.target == this) {
	        $(".d-prompt").hide();
	    } 
	})
});
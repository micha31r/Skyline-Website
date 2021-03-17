$(function() {
	$("#prompt-toggle").click(function() {
		var element = $("#d-prompt");
		if (element.css("display") == "none") {
			element.css("display", "flex");
		}
	});
	$("#d-prompt").click(function(e) {
		if (e.target == this) {
	        $("#d-prompt").hide();
	    } 
	})
});
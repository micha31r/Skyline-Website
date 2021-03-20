$(function() {
	$(".prompt-toggle").each(function() {
		$(this).click(function() {
			console.log($(this).attr("id"));
			var element = $("#d-prompt-" + $(this).prop("id"));
			if (element.css("display") == "none") {
				element.css("display", "flex");
			}
		});
	});
	$(".d-prompt").click(function(e) {
		if (e.target == this) {
	        $(".d-prompt").hide();
	    } 
	})
});
$(function() {
	$(".prompt-toggle").each(function() {
		$(this).click(function() {
			const id = $(this).prop("id");
			const identifier = "#d-prompt" + (id ? '-'+id : '');
			var element = $(identifier);
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
$(function() {
	$(".faq .question h3").each(function() {
		$(this).click(function() {
			let e = $(this).parent();
			if (e.hasClass("expand")) {
				e.removeClass("expand");
			} else {
				e.addClass("expand");
			}
		});
	});
});
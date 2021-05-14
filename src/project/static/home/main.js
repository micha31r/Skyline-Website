$(function() {
	let f = () => {
		$(".intro-container-wrapper").css("min-height", $(window).height() - $("nav").outerHeight() - $(".nav-activities").outerHeight());
		$(".bg-video").css({
			"top": $("nav").outerHeight() + $(".nav-activities").outerHeight() + "px",
			"height": $(".intro-container-wrapper").outerHeight(),
		});
		// Activity cards
		var max = 0;
		$(".card").each(function() {
			let vp = $(this).find(".vp");
			let val = vp.find("img").outerHeight() + vp.find(".initial").outerHeight() + 20;
			if (max < val) { 
				max = val;
			}
		});
		$(".vp").height(max);
		$(".text-container").outerHeight(max);
	};
	$(window).resize(f);
	f();
});
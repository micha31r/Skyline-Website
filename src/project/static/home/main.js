$(function() {
	let f = () => {
		$(".intro-container-wrapper").css("min-height", $(window).height() - $("nav").outerHeight() - $(".nav-activities").outerHeight());
		$(".bg-video").css({
			"top": $("nav").outerHeight() + $(".nav-activities").outerHeight() + "px",
			"height": $(".intro-container-wrapper").outerHeight(),
		});
	};
	$(window).resize(f);
	f();
});
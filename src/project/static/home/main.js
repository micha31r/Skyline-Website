$(function() {
	let f = () => {
		$(".bg-video").css({
			"top": $("nav").outerHeight() + $(".nav-activities").outerHeight() + "px",
			"height": $(".intro-container-wrapper").outerHeight(),
		});
	};
	$(window).resize(f);
	f();
});
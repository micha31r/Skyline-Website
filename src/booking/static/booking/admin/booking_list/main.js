$(function() {
	function resize() {
		if ($(this).width() <= 700) {
			$("#d-prompt .container").append($(".settings"));
		} else {
			$(".overview").prepend($(".settings"));
			$("#d-prompt").click();
		}
	}
	$(window).resize(resize);
	resize();
});
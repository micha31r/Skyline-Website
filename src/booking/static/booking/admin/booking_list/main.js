$(function() {
	function resize() {
		if ($(this).width() <= 700) {
			$("#d-prompt .container").append($(".settings"));
			$("#paginator-append-target").append($(".pagination"));
		} else {
			$(".overview").prepend($(".settings"));
			$(".settings").append($(".pagination"));
			$("#d-prompt").click();
		}
	}
	$(window).resize(resize);
	resize();
});
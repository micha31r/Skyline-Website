function navbar_resize() {
	if ($(window).width() <= 960) {
		$("#popup-nav").append($("nav .right"));
	} else {
		$("nav .grid").append($("#popup-nav .right"));
		$("#popup-nav").hide();
		switch_icon("close");
	}
}

function switch_icon(state) {
	switch (state) {
		case "close":
			$("#popup-nav-toggle .close").hide();
			$("#popup-nav-toggle .open").show();
			break;
		case "open":
			$("#popup-nav-toggle .close").show();
			$("#popup-nav-toggle .open").hide();
			break;
	}
}

// Timeout id
var id;

function nav_toggle() {
	if ($(window).width() <= 960) {
		var popup_nav = $("#popup-nav");
		let visiblility = popup_nav.css("display");
		if (visiblility == "block") {
			// Set ms to the same as animation-duration
			id = setTimeout(()=>{popup_nav.hide();}, 200);
			popup_nav.css("animation-name", "hide");
			switch_icon("close");
		} else {
			clearTimeout(id);
			popup_nav.show();
			popup_nav.css("animation-name", "show");
			switch_icon("open");
		}
	}
}

$(function() {
	$("#popup-nav-toggle").click(nav_toggle);
	$(window).resize(navbar_resize);
	navbar_resize();
});
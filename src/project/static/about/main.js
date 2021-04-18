function catalogResize() {
	$(".about .left").css("max-height", $(window).height() - $("nav").outerHeight() + "px");
	$(".about .left").css("top", $("nav").outerHeight()+"px");
}

$(function() {
	$(window).resize(catalogResize);
	catalogResize();
});
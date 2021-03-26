$(function() {
	let f = () => {$(".checkout-status").css("top", $("nav").height());};
	$(window).resize(f);
	f();
});
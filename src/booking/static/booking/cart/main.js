$(function() {
	$(".cart-container-wrapper").css(
		"min-height",
		`calc(100vh - ${$("nav").height()+$(".checkout-status").height()}px)`
	);
});
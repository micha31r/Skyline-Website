$(function() {
	$("input").change(function() {
		if ($(this).val() > 15) {
			$(this).val(15);
		}
	});
});
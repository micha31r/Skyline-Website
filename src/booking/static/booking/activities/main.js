$(function() {
	$("input").change(function() {
		if ($(this).val() > 15) {
			$(this).val(15);
		}
	});

	// Set input value to 0 if empty on form submission
	$("button[type='submit']").click(function(e) {
		let parent = $(this).parent();
		let adult = parent.find("input[name='adult_count']");
		let child = parent.find("input[name='child_count']");
		if (!adult.val() && child.val()) {
			adult.val("0");
		} else if (!child.val() && adult.val()) {
			child.val("0");
		}
	});
});
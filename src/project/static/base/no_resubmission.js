$(function() {
	// Prevent form resubmission
	// https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr
	if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
});

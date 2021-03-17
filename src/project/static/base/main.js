// Window dimension difference, x - y
function window_diff() {
	return Math.abs($(window).width() - $(window).height())
}

function active_link() {
	$(document).ready(
		function() {
		    $("[href]").each(
		    	function() {
			        if (this.href == window.location.href) {
			            $(this).addClass("active-link");
			        }
		    	}
		    );
		}
	);
}

$(active_link);
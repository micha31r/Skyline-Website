$(function() {
	var text = $("#copyright-symbol").text().replace("©", `© ${new Date().getFullYear()}`);
	$("#copyright-symbol").text(text);
});
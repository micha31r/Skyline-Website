document.onreadystatechange = function() {
	var bd = document.querySelector("body");
	var ld = document.querySelector("#loader");
    if (document.readyState !== "complete") { 
        bd.style.visibility = "hidden"; 
        ld.style.visibility = "visible";
    } else { 
        ld.style.display = "none";  
        bd.style.visibility = "visible"; 
    } 
};
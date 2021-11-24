/* MODAL */
// Get the modal

let modal = document.getElementById("myModal");

// Get the button that opens the modal
let btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
	$('#breadcrumbMY').css("pointer-events","none");
	$('.nav__link,.nav-toggle').css("pointer-events","none");
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
	$('#breadcrumbMY').css("pointer-events","auto");
	$('.nav__link,.nav-toggle').css("pointer-events","auto");
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
	$('#breadcrumbMY').css("pointer-events","auto");
	$('.nav__link,.nav-toggle').css("pointer-events","auto");
    modal.style.display = "none";
  }
}
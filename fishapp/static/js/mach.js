// Define the query
const mediaQuery = window.matchMedia(
	'handheld, all and (max-width:990px)'
	);


const screenMediaQuery = window.matchMedia('screen and (min-width: 250px)');


function addClass(textId, name) {
	let text = document.getElementById(textId);
	// text.classList.remove('hidden');
	text.classList.add(name);
}

function removeClass(textId, name) {
	let text = document.getElementById(textId);
	// text.classList.remove('hidden');
	text.classList.remove(name);
}



function handleTabletChange(e, e1) {

	if (e1){

		if (e.matches || (e1.matches && window.scrollY > 300.00)) {
		    addClass('header', 'header--fixed')
		} else {
		  	removeClass('header', 'header--fixed')
	    }
	     
	} else {

		if (e.matches) {
		    addClass('header', 'header--fixed');
		} else {
		  	removeClass('header', 'header--fixed');
	    }
	}
  
}

mediaQuery.addListener(handleTabletChange)
handleTabletChange(mediaQuery, screenMediaQuery)


window.addEventListener('scroll', function(e) {
  last_known_scroll_position = window.scrollY;
  
  /* Media Listener */
  handleTabletChange(mediaQuery, screenMediaQuery)

});








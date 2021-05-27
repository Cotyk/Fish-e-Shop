const __mediaQuery = window.matchMedia(
'handheld, all and (max-width:990px)'
);


const __770 = window.matchMedia(
	'handheld, all and (max-width:770px)'
	);

const __575 = window.matchMedia(
	'handheld, all and (max-width:575px)'
	);

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

mfID = 'mobile_filter';
mobileFilterOffset = 280;
mobileFilterFixed = false;

// mfHeight = Math.round($(`#${mfID}`).css('height').slice(0, -2));
mfHeight = 80;


window.addEventListener('scroll', function(e) {
  last_known_scroll_position = window.scrollY;
	
  /* Mobile Filter Listener */

  if (__mediaQuery.matches){
	  if (window.last_known_scroll_position >= mobileFilterOffset-mfHeight+7) {
	  	if (!mobileFilterFixed && __mediaQuery.matches) {
	  		mobileFilterFixed = true;
	  		removeClass("header_breadcrumb", 'hidden');
	  	}
	  } else {
	  	
	  	mobileFilterFixed = false;
	  	addClass("header_breadcrumb", 'hidden');
	  }
	} else if (__770.maches) {
		if (window.last_known_scroll_position >= mobileFilterOffset-mfHeight+19) {
	  	if (!mobileFilterFixed && __770.matches) {
	  		
	  		mobileFilterFixed = true;
	  		removeClass("header_breadcrumb", 'hidden');
	  	}
	  } else {
	  	mobileFilterFixed = false;
	  	addClass("header_breadcrumb", 'hidden');
	  }
	}
  /* Media Listener */

});
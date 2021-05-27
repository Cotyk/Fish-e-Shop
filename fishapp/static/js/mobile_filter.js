// const mediaQuery = window.matchMedia(
// 	'handheld, all and (max-width:990px)'
// 	);

const _mediaQuery = window.matchMedia(
'handheld, all and (max-width:990px)'
);


const _770 = window.matchMedia(
	'handheld, all and (max-width:770px)'
	);

const _575 = window.matchMedia(
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
mobileFilter = document.getElementById(mfID);
// mobileFilterOffset = Math.round($(`#${mfID}`).offset().top);
mobileFilterOffset = 280;
mobileFilterFixed = false;

// mfHeight = Math.round($(`#${mfID}`).css('height').slice(0, -2));
mfHeight = 80;

window.addEventListener('scroll', function(e) {
  last_known_scroll_position = window.scrollY;
  
	
  /* Mobile Filter Listener */

  if (_mediaQuery.matches){
	  if (window.last_known_scroll_position >= mobileFilterOffset-mfHeight+7) {
	  	if (!mobileFilterFixed) {
	  		addClass(mfID, 'fixed');
	  		$('#intro').css("margin-bottom", "80px");
	  		mobileFilterFixed = true;
	  		removeClass("header_breadcrumb", 'hidden');
	  	}
	  } else {
	  	removeClass(mfID, 'fixed');
	  	$('#intro').css("margin-bottom", "0");
	  	mobileFilterFixed = false;
	  	addClass("header_breadcrumb", 'hidden');
	  }
	} else if (_770.maches) {
		if (window.last_known_scroll_position >= mobileFilterOffset-mfHeight+19) {
	  	if (!mobileFilterFixed) {
	  		addClass(mfID, 'fixed');
	  		$('#intro').css("margin-bottom", "80px");
	  		mobileFilterFixed = true;
	  		removeClass("header_breadcrumb", 'hidden');
	  	}
	  } else {
	  	removeClass(mfID, 'fixed');
	  	$('#intro').css("margin-bottom", "0");
	  	mobileFilterFixed = false;
	  	addClass("header_breadcrumb", 'hidden');
	  }
	}
  /* Media Listener */

});
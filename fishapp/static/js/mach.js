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

let text = '<div class="price-slider">\n' +
'                        <span>Від\n' +
'                        <input id="input1_number" class="custom_input" type="number" value="0" min="0" max="12000"/> грн <br>До\n' +
'                        <input id="input2_number" class="custom_input" type="number" value="12000" min="0" max="12000"/> грн</span>\n' +
'                      <input id="input1_range" class="custom_input" value="0" min="0" max="12000" step="10" type="range"/>\n' +
'                      <input id="input2_range" class="custom_input" value="12000" min="0" max="12000" step="10" type="range"/>\n' +
'                      <svg width="100%" height="24">\n' +
'                        <line x1="4" y1="0" x2="300" y2="0" stroke="#212121" stroke-width="12" stroke-dasharray="1 28"></line>\n' +
'                      </svg>\n' +
'                    </div>';

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
	try {
		if (e.matches) {
		let divv = document.getElementById('show_if_mobile_div');
		let divv_screen = document.getElementById('show_if_mobile_div_screen');

		if(!divv.innerHTML){
			divv.innerHTML = text;
		}

		if(divv_screen.innerHTML){
			divv_screen.innerHTML = '';
		}

		}else{
			let divv = document.getElementById('show_if_mobile_div');
			let divv_screen = document.getElementById('show_if_mobile_div_screen');

			if(divv.innerHTML){
				divv.innerHTML = '';
			}

			if(!divv_screen.innerHTML){
				divv_screen.innerHTML = text;
			}
		}

	} catch (e) {

	}
}

mediaQuery.addListener(handleTabletChange)
handleTabletChange(mediaQuery, screenMediaQuery)


window.addEventListener('scroll', function(e) {
  last_known_scroll_position = window.scrollY;
  
  /* Media Listener */
  handleTabletChange(mediaQuery, screenMediaQuery)

});








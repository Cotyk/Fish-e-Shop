


/* nav_link Click */
$("[data-click]").on("click", function(){
	// event.preventDefault();

	$("#header-nav1 a").removeClass("active");
	$(this).addClass("active");
});

/* Menu nav toggle */
$("#nav-toggle").on("click", function(event){
	event.preventDefault();

	$this = $(this);
	$this.toggleClass("active");
	$("#header").toggleClass("active");
	$("#header_mobile_search_form").removeClass("active");
});

/* Menu nav toggle */
// $("[data-click-category]").on("click", function(event){
// 	// event.preventDefault();
//
// 	$("#intro_categories a").removeClass("active");
// 	$(this).addClass("active");
// });


/* Search toggle */
$("#header_search_a").on("click", function(event){
	event.preventDefault();

	$("#header_mobile_search_form").toggleClass("active");
	$("#header").removeClass("active");
	$("#nav-toggle").removeClass("active");
})

/* Logo scrolling */
$("[data-scroll]").on("click", function(event){
	event.preventDefault();

	let blockId = $(this).data("scroll"),
		blockOffset = Math.round($(blockId).offset().top);

	$("html, body").animate({
		scrollTop: blockOffset
	});
});

/* JS filtering products */

$('.filter__item--js').on('click', function (event){
	event.preventDefault();
	let current_content = $(this).html();
	// alert(String(current_content).trim());

	if (String(current_content).trim().includes('fas fa-th-list')){
		$('.filter__item--2').html('<i class="fas fa-th-large"></i>');
		$('.mobile_filter__item.first').html('<i class="fas fa-th-large"></i>');

		// let $recommend = $('[data-name="prod_list"]');
		let $recommend = $('.sidebar__products--for_recommend.product__list__js');
		$recommend.addClass('sidebar__products--for_catalog');
		$recommend.removeClass('sidebar__products--for_recommend');

	}else{
		$('.filter__item--2').html('<i class="fas fa-th-list"></i>');
		$('.mobile_filter__item.first').html('<i class="fas fa-th-list"></i>');

		// let $catalog = $('[data-name="prod_list"]');
		let $catalog = $('.sidebar__products--for_catalog.product__list__js');
		$catalog.addClass('sidebar__products--for_recommend');
		$catalog.removeClass('sidebar__products--for_catalog');
	}
});

const calcSidebarQuery = window.matchMedia(
	'screen and (min-width:991px)'
);

const productMach = window.matchMedia(
	'screen and (min-width:576px)'
);

$(document).ready(function (){
	if (productMach.matches){
		$('.product_photoblock').css('margin-right', '20px');
	}else{
		$('.product_photoblock').css('margin-right', 0);
	}


	if (calcSidebarQuery.matches){
		$('.product_title').css('margin-top', 0);
	}else{
		$('.product_title').css('margin-top', '25px');
	}
})

$(window).on('resize', function (){
	if (productMach.matches){
		$('.product_photoblock').css('margin-right', '20px');
	}else{
		$('.product_photoblock').css('margin-right', 0);
	}


	if (calcSidebarQuery.matches){
		$('.product_title').css('margin-top', 0);
	}else{
		$('.product_title').css('margin-top', '25px');
	}
})


if(calcSidebarQuery.matches){

	/* Wise Sidebar Feature */
	$(document).ready(function (){
		let titles = document.querySelectorAll('.recommend__title');
		let lastTitle = document.querySelectorAll('.recommend__title')[titles.length-1];

		let sidebarAll = document.querySelectorAll('.sidebar__product--native');
		let sidebarLast = document.querySelectorAll('.sidebar__product--native')[sidebarAll.length-1];
		let sidebarLastChildren = document.querySelectorAll('.sidebar__product--native:last-child');
		// alert(sidebarLastChildren[1].parentNode.childElementCount);
		let distance;
		// let first_time = true;

		let count, max, min, minI, maxI;
		let sum = 0;
		let sortedSidebarList = Array();
		// let reduceArray = Array();
		for(let i=0; i<sidebarLastChildren.length; i++){
			count = sidebarLastChildren[i].parentNode.childElementCount;
			sum += count;
			sortedSidebarList.push([count, i, sidebarLastChildren[i]]) /* [0, 1, 2] */
			// reduceArray.push(count);

			if(i === 0){
				max = count;
				min = count;
				minI = i;
				maxI = i;

			}else{
				if (count > max){
					max = count;
					maxI = i;
				}
				if(count < min){
					min = count;
					minI = i;
				}
			}

		}

		let position = 2*(maxI+1);
		let unsortedSidebarList = sortedSidebarList.slice();
		sortedSidebarList.sort(function (a, b){
			return b[0] - a[0];
		});
		//
		// reduceArray.sort(function (a, b){
		// 	return b - a;
		// });
		// $(document.querySelectorAll('.sidebar__product--native')[43]).css('display', 'none');
		// alert('min, max, minI, maxI ' + min + ' ' + max + ' ' + minI + ' ' + maxI);

		distance = $(lastTitle).offset().top - $(sidebarLast).offset().top;
		// console.log(distance);

		let c = $('.sidebar__header').length - sortedSidebarList.length;

		let groups = Array();
		// alert(c + ' - c');
		for(let u=0;u<sortedSidebarList.length;u++){
			groups.push($('.sidebar__header')[c + sortedSidebarList[u][1]].closest('.sidebar__item--for_product').querySelectorAll('.sidebar__product'));
		}

		window.addEventListener('scroll', function(e) {

			// console.log(distance);

			for (let rect=0; rect<9;rect++){
				// try {
				let sidebarLastOffset = groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]];
				let ind = 1;

				while (!sidebarLastOffset) {
					sidebarLastOffset = groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind];
					ind += 1;
				}

				if(Number(unsortedSidebarList[groups.length-1][0]) !== 0) {

					let down_ind = -1;
					let asc_index = 1;
					if ((Number($(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-1]).offset().top) !== 0)){
						distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-1]).offset().top;
					}

					/* Descending */
					while ((Number($(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-1]).offset().top) === 0) && down_ind>=-5){
						try{
							distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-1+down_ind]).offset().top;
						}catch (err){
							if (err instanceof TypeError){
								// pass

							}else{
								throw err;
							}
						}
						down_ind -= 1;
					}
					// distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-1+down_ind]).offset().top;

					/* Ascending */
					while ((Number($(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1]).offset().top) === 0) && asc_index<=6){
						try{
							distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1+asc_index]).offset().top;
						}catch (err){
							if (err instanceof TypeError){
								// pass
							}else{
								throw err;
							}
						}
						asc_index += 1;
					}
					//
					// let gr = sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1]);
					// console.log('group= '+gr);
					// let indx = unsortedSidebarList[groups.length-1][0]-ind-1+down_ind;
					// console.log('el_ind= '+indx);

				}else{
					let down_ind = -1
					let asc_index = 1;
					if ((Number($(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1]).offset().top) !== 0)){
						distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1]).offset().top;
					}

					/* Descending */
					while ((Number($(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1]).offset().top) === 0) && down_ind>=-5){
						try{
							distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1+down_ind]).offset().top;
						}catch (err){
							if (err instanceof TypeError){
								// pass

							}else{
								throw err;
							}
						}
						down_ind -= 1;
					}
					// distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1+down_ind]).offset().top;

					/* Ascending */
					while ((Number($(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1]).offset().top) === 0) && asc_index<=6){
						try{
							distance = $(lastTitle).offset().top - $(groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1+asc_index]).offset().top;
						}catch (err){
							if (err instanceof TypeError){
								// pass
							}else{
								throw err;
							}
						}
						asc_index += 1;
					}

					// let ind = groups[sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1])][unsortedSidebarList[groups.length-1][0]-ind-1+down_ind];
					// let gr = sortedSidebarList.indexOf(unsortedSidebarList[groups.length-1]);
					// console.log('group= '+gr);
					// let indx = unsortedSidebarList[groups.length-1][0]-ind-1+down_ind;
					// console.log('el_ind= '+indx);
				}

				// console.log(distance);

				// let result = reduceArray.reduce(function(acc, el) {
				//   acc[el] = (acc[el] || 0) + 1;
				//   return acc;
				// }, {});
				// let howMuchReduce = result[String(sortedSidebarList[0][0])];

				if ((Number(distance) < -280*groups.length) || (Number(distance > 280*groups.length))){

					let last = Array();
					let rLast = Array();

					for(let i=0; i<sortedSidebarList.length; i++){
						if(sortedSidebarList[i+1]) {

							if(sortedSidebarList[i][0] !== sortedSidebarList[i+1][0]){

								for (let r=i;r<=i;r++){
									if(!last.includes([groups[r][sortedSidebarList[r][0]-1]]) && last.length < sortedSidebarList.length-1) {
										last.push(groups[r][sortedSidebarList[r][0] - 1]);
										rLast.push(r);
									}
								}

								break; /* 19 19 19 */

							}else if(sortedSidebarList[i][0] === sortedSidebarList[i+1][0]){

								for (let r=i;r<=i+1;r++){
									if(!last.includes(groups[r][sortedSidebarList[r][0]-1]) && last.length < sortedSidebarList.length){
										last.push(groups[r][sortedSidebarList[r][0]-1]);
										rLast.push(r);
									}
								}

							}
						}
					}

					if(Number(distance) < -280*groups.length && position < sidebarAll.length - 1) {
						for(let j=0; j<last.length;j++){
							if (last[j]) {
								$(last[j]).css('display', 'none');
								// .css('border-bottom', '1px solid #dcdcdc')
								position += 1;
								sum -= 1;
								sortedSidebarList[rLast[j]][0] -= 1;
								// reduceArray[j] -= 1;

								$(groups[rLast[j]][sortedSidebarList[rLast[j]][0]-1]).css('border-bottom', 0);

							}
						}
					}else if(Number(distance) > 280*groups.length && position > 2*(maxI+1)-3){


						for(let j=0; j<last.length;j++){
							if (last[j]){
								$(last[j]).css('display', 'block');
								// .css('border-bottom', '0')
								position -= 1;
								sum += 1;
								sortedSidebarList[rLast[j]][0] += 1;
								// reduceArray[j] += 1;

								$(groups[rLast[j]][sortedSidebarList[rLast[j]][0]-3]).css('border-bottom', '1px solid #dcdcdc');

							}

						}

					}

				}
				// console.log('---------------------------------------------------------------------------------------');

			// } catch (e) {
			//   if (e instanceof TypeError) {
			// 	// console.log(e + ' !');
			// 	// console.log('index= '+sortedSidebarList.indexOf(unsortedSidebarList[groups.length-2]));
			// 	// console.log('val= '+(unsortedSidebarList[groups.length-1][0]-2));
			// 	// distance = $(lastTitle).offset().top - $(sortedSidebarList).offset().top;
			//
			//   }else{
			// 	// обработка остальных исключений
			// 	throw e; // передать обработчику ошибок
			//   }
			// }
			}


		});
	});

}

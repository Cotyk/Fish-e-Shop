
/* nav_link Click */
$("[data-click]").on("click", function(event){
	event.preventDefault();

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
$(document).ready(function(){
$('.first ol li a.active-1').find('span').css('color' , 'black');
$('.first ol li a.active-1').find('span').css('font-weight' , 'bold');

$('.first ol li a').click(function() {
$('.first ol li a.active-1').find('span').css('color' , 'black');
$('.first ol li a.active-1').find('span').css('font-weight' , 'normal');
$('.first ol li a.active-1').removeClass('active-1');
$('.first ol li a.active-1').addClass('text-dark');
$(this).closest('a').addClass('active-1');
$('.first ol li a.active-1').find('span').css('color' , 'black');
$('.first ol li a.active-1').find('span').css('font-weight' , 'bold');
});

});
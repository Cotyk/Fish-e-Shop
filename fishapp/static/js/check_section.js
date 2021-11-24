let select = $('#transp_select');

$(document).ready(function (){

    if(String(select.data('value')) === 'delivery'){

    $('#order_sect').css('display', 'block');
    }else{
        $('#order_sect').css('display', 'none');
    }

    $(select).on('change', function () {
        if(String(this.value) === 'delivery'){

            $('#order_sect').css('display', 'block');
        }else{
            $('#order_sect').css('display', 'none');
        }
    });
})


// let select = $('.new-select');
// let firstNeeded = true;
//
//
// $(select[0]).on('DOMSubtreeModified', function () {
//     if(select[0].textContent.length > 1 && firstNeeded){
//
//         if(String(select[0].textContent) === 'У відділення'){
//             // alert('yep');
//             $('.order_sect').css('display', 'block');
//         }
//
//         firstNeeded = false;
//     }
//
//     if(String(select[0].textContent) === 'Самовивіз'){
//         firstNeeded = true;
//         $('.order_sect').css('display', 'none');
//     }
// });
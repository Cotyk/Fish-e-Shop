function imageZoom(imgID, resultID) {
  let img, lens, result, cx, cy;
  img = document.getElementById(imgID);
  result = document.getElementById(resultID);
  /*create lens:*/
  lens = document.createElement("DIV");
  lens.setAttribute("class", "img-zoom-lens");
  /*insert lens:*/
  img.parentElement.insertBefore(lens, img);
  /*calculate the ratio between result DIV and lens:*/
  cx = result.offsetWidth / lens.offsetWidth;
  cy = result.offsetHeight / lens.offsetHeight;
  /*set background properties for the result DIV:*/
  result.style.backgroundImage = "url('" + img.src + "')";
  result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
  /*execute a function when someone moves the cursor over the image, or the lens:*/
  lens.addEventListener("mousemove", moveLens);
  img.addEventListener("mousemove", moveLens);
  /*and also for touch screens:*/
  lens.addEventListener("touchmove", moveLens);
  img.addEventListener("touchmove", moveLens);
  function moveLens(e) {
    let pos, x, y;
    /*prevent any other actions that may occur when moving over the image:*/
    e.preventDefault();
    /*get the cursor's x and y positions:*/
    pos = getCursorPos(e);
    /*calculate the position of the lens:*/
    x = pos.x - (lens.offsetWidth / 2);
    y = pos.y - (lens.offsetHeight / 2);
    /*prevent the lens from being positioned outside the image:*/
    if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;}
    if (x < 0) {x = 0;}
    if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight;}
    if (y < 0) {y = 0;}
    /*set the position of the lens:*/
    lens.style.left = x + "px";
    lens.style.top = y + "px";
    /*display what the lens "sees":*/
    result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
  }
  function getCursorPos(e) {
    let a, x = 0, y = 0;
    e = e || window.event;
    /*get the x and y positions of the image:*/
    a = img.getBoundingClientRect();
    /*calculate the cursor's x and y coordinates, relative to the image:*/
    x = e.pageX - a.left;
    y = e.pageY - a.top;
    /*consider any page scrolling:*/
    x = x - window.pageXOffset;
    y = y - window.pageYOffset;
    return {x : x, y : y};
  }
}

 let myImage = $('#myimage');
 let imgBlock = $('#product_photoblock, .product_extra_photo');

try{
    let width = Number(String(myImage.css('width')).slice(0, -2));
    if (width>101){
        imageZoom("myimage", "myresult");

        $('#myresult').css('opacity', 0);

        if(window.matchMedia('(max-width:990px)').matches){
            // myImage.on('touchstart', function (){
            //
            //     $(this).css('opacity', 0);
            //     $('#myresult').css('opacity', 1);
            // });

            $(window).on('resize', function (event){
                $('.img-zoom-result').css('width', imgBlock.css('width')).css('height', imgBlock.css('height'));
            });

            myImage.on('touchstart', function (event){
                $(this).css('opacity', 1);
                $('#myresult').css('opacity', 0);
            });
        }else{
            myImage.on('mouseover', function (){
                $(this).css('opacity', 0);
                $('#myresult').css('opacity', 1);

            });

            myImage.on('mouseleave', function (){
                $(this).css('opacity', 1);
                $('#myresult').css('opacity', 0);
            });
        }

    }
}catch (e) {
    console.log(e);
}

/* MODAL */
// Get the modal

$(document).ready(function (){
    if($('#myimage').attr('src')){
        $('.product_photoblock').css('pointer-events', 'auto');

        let modal = document.getElementById("productPhotoModal");

        // Get the button that opens the modal
        // let btn = document.getElementById("product_photoblock");
        let btn = $("#product_photoblock");
        let extra_btn = document.querySelectorAll('.product_extra_photo')

        $(btn).css('cursor', 'zoom-in')
        // Get the <span> element that closes the modal
        let span = document.getElementsByClassName("close")[0];

        // When the user clicks on the button, open the modal
        let photoBig = document.getElementById('product_photo_big');
        let initSrc = String($(photoBig).attr('src'));
        let listPhotos = $('.product_photo, .product_extra_img');
        let listSrc = []

        let i = 0;
        while (listPhotos[i] !== undefined) {
            listSrc.push($(listPhotos[i]).attr('src'));
            // alert($(listPhotos[i]).attr('src'));
            i += 1;
        }

        $(btn).on('click', function(event) {
            $('#breadcrumbMY').css("pointer-events","none");
            $('.nav__link,.nav-toggle').css("pointer-events","none");
            $(photoBig).attr('src', initSrc);
            modal.style.display = "block";
        });

        $(extra_btn).on('click', function (event){
            event.preventDefault();
            modal.style.display = 'block';
            $(photoBig).attr('src', `${event.currentTarget}`);
        });

        let last = [listSrc.length-1, listSrc[listSrc.length-1]];
        $('#modal_left_arrow').on('click', function (event){
            // alert('left');
            event.preventDefault();
            let index = 0;
            while (listSrc[index] !== undefined){
                if (String($(photoBig).attr('src')) === `${listSrc[index]}`){
                    if (index < 1) {
                        $(photoBig).attr('src', `${last[1]}`);
                    }else{
                        $(photoBig).attr('src', `${listSrc[index-1]}`);
                    }
                    break;
                }

                index += 1;
            }
        })

        $('#modal_right_arrow').on('click', function (event){
            // alert('right');
            event.preventDefault();
            let index = 0;
            while (listSrc[index] !== undefined){
                // alert(index);
                if (String($(photoBig).attr('src')) === `${listSrc[index]}`){

                    if (index >= last[0]) {
                        $(photoBig).attr('src', `${listSrc[0]}`);
                    }else{
                        $(photoBig).attr('src', `${listSrc[index+1]}`);
                    }
                    break;
                }

                index += 1;
            }
        })

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
    }else{
        $('.product_photoblock').css('pointer-events', 'none');
    }
})







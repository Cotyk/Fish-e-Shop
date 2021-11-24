
const handheld = window.matchMedia(
'handheld, all and (max-width:990px)'
);
let URL_STRING_ENCODE = {
    'price': 'За зростанням ціни',
    'price1': 'За спаданням ціни',
    'title': 'За назвою',
    'created1': 'За новизною',
};
try{
    url.hostname;
}catch (ex){
    url = window.location;
}

let wLoc, pageLgt, pageVal;
 if (String(url).includes(`?page=`)){
    let slice = `${String(url).slice(String(url).lastIndexOf('?page=')+6)}`;
    if (slice.includes('&')){
        pageLgt = slice.slice(0, slice.indexOf('&')).length;
        // pageVal = slice.slice(0, slice.indexOf('&'));
    }else{
        pageLgt = slice.length;
        // pageVal = slice;
    }
 }

if (!handheld.matches){
    let select = $('.new-select');

    let firstForFiltering = true;
    let firstForSorting = true;
    let url = document.location;
    let val0 = select[0];
    let val1 = select[1];


    if (val1 || val0){
        val0 = select[0].textContent;
        val1 = select[1].textContent;
        let VALUE1_LENGTH, VALUE2_LENGTH, VALUE1, VALUE2;
        let sliceFromFilterPlus10, sliceFromOrderPlus10;

        if (String(url).includes(`&on_page=`)){
            sliceFromOrderPlus10 = `${String(url).slice(String(url).lastIndexOf('&on_page')+9)}`;
            if (sliceFromOrderPlus10.includes('&')){
                VALUE1_LENGTH = sliceFromOrderPlus10.slice(0, sliceFromOrderPlus10.indexOf('&')).length;
                VALUE1 = sliceFromOrderPlus10.slice(0, sliceFromOrderPlus10.indexOf('&'));
            }else{
                VALUE1_LENGTH = sliceFromOrderPlus10.length;
                VALUE1 = sliceFromOrderPlus10;
            }

            select[1].textContent = VALUE1;
        }
        if (String(url).includes(`&order_by=`)){
            sliceFromFilterPlus10 = `${String(url).slice(String(url).lastIndexOf('&order_by')+10)}`;
            if (sliceFromFilterPlus10.includes('&')){
                VALUE2_LENGTH = sliceFromFilterPlus10.slice(0, sliceFromFilterPlus10.indexOf('&')).length;
                VALUE2 = sliceFromFilterPlus10.slice(0, sliceFromFilterPlus10.indexOf('&'));
            }else{
                VALUE2_LENGTH = sliceFromFilterPlus10.length;
                VALUE2 = sliceFromFilterPlus10;
            }

            select[0].textContent = URL_STRING_ENCODE[`${VALUE2}`];
        }

        $(select[1]).on('DOMSubtreeModified', function () {
            if(select[1].textContent && firstForFiltering){

                 val1 = Number(select[1].textContent);

                 if(String(url).includes(`&on_page=`)) {

                     if (String(String(url).slice(String(url).lastIndexOf('&on_page')).length > 9+1+(VALUE1_LENGTH))) {
                         wLoc = `${String(url).slice(0, String(url).lastIndexOf('&on_page'))}&on_page=${val1}${String(url).slice(String(url).lastIndexOf('&on_page') + 9+(VALUE1_LENGTH))}`;

                     } else {
                         wLoc = `${String(url).slice(0, String(url).lastIndexOf('&on_page'))}&on_page=${val1}`;
                     }
                 }else{
                    if(String(url).includes(`&`)) {
                        wLoc = `${String(url).slice(0, String(url).lastIndexOf('&'))}&on_page=${val1}${String(url).slice(String(url).lastIndexOf('&'))}`;
                    }else{
                        wLoc = `${String(url).slice(0)}&on_page=${val1}`;
                    }
                 }

                 if(wLoc){
                     window.location = `${String(wLoc).slice(0, String(url).lastIndexOf('?page=')+6)}1${String(wLoc).slice(String(url).lastIndexOf('?page=')+6+pageLgt)}`;
                 }

                firstForFiltering = false;
            }
        });

        $(select[0]).on('DOMSubtreeModified', function () {
            if(select[0].textContent && firstForSorting){

                val0 = String(select[0].textContent);
                // alert(val0);

                let translated_val0;
                if (val0 === 'За зростанням ціни'){
                    translated_val0 = 'price';
                }else if (val0 === 'За спаданням ціни'){
                    translated_val0 = 'price1';
                }else if (val0 === 'За назвою'){
                    translated_val0 = 'title';
                }else if (val0 === 'За новизною'){
                    translated_val0 = 'created1';
                }

                 if(String(url).includes(`&order_by=`)) {
                     if (String(String(url).slice(String(url).lastIndexOf('&order_by')).length > 10+1+(VALUE2_LENGTH))) {
                         wLoc = `${String(url).slice(0, String(url).lastIndexOf('&order_by'))}&order_by=${translated_val0}${String(url).slice(String(url).lastIndexOf('&order_by')+10+(VALUE2_LENGTH))}`;
                     } else {
                         wLoc = `${String(url).slice(0, String(url).lastIndexOf('&order_by'))}&order_by=${translated_val0}`;
                     }
                 }else{
                    if(String(url).includes(`&`)) {
                        wLoc = `${String(url).slice(0, String(url).lastIndexOf('&'))}&order_by=${translated_val0}${String(url).slice(String(url).lastIndexOf('&'))}`;
                    }else{
                        wLoc = `${String(url).slice(0)}&order_by=${translated_val0}`;
                    }
                 }

                 if(wLoc){
                     window.location = `${String(wLoc).slice(0, String(url).lastIndexOf('?page=')+6)}1${String(wLoc).slice(String(url).lastIndexOf('?page=')+6+pageLgt)}`;
                 }

                firstForSorting = false;
            }
        });
    }

}else{
    let select = $('.new-mobile-select');
    let firstForFiltering = true;
    let firstForSorting = true;
    let url = document.location;
    let val0 = select[0].value;
    let val1 = select[1].value;


    let VALUE1_LENGTH, VALUE2_LENGTH, VALUE1, VALUE2;
    let sliceFromFilterPlus10, sliceFromOrderPlus10;

    if (String(url).includes(`&on_page=`)){
        sliceFromOrderPlus10 = `${String(url).slice(String(url).lastIndexOf('&on_page')+9)}`;
        if (sliceFromOrderPlus10.includes('&')){
            VALUE1_LENGTH = sliceFromOrderPlus10.slice(0, sliceFromOrderPlus10.indexOf('&')).length;
            VALUE1 = sliceFromOrderPlus10.slice(0, sliceFromOrderPlus10.indexOf('&'));
        }else{
            VALUE1_LENGTH = sliceFromOrderPlus10.length;
            VALUE1 = sliceFromOrderPlus10;
        }

        select[1].value = VALUE1;
        // alert(VALUE1);
    }
    if (String(url).includes(`&order_by=`)){
        sliceFromFilterPlus10 = `${String(url).slice(String(url).lastIndexOf('&order_by')+10)}`;
        if (sliceFromFilterPlus10.includes('&')){
            VALUE2_LENGTH = sliceFromFilterPlus10.slice(0, sliceFromFilterPlus10.indexOf('&')).length;
            VALUE2 = sliceFromFilterPlus10.slice(0, sliceFromFilterPlus10.indexOf('&'));
        }else{
            VALUE2_LENGTH = sliceFromFilterPlus10.length;
            VALUE2 = sliceFromFilterPlus10;
        }

        select[0].value = URL_STRING_ENCODE[`${VALUE2}`]; /* !!! */
    }

    $(select[1]).on('change', function () {  /* !!! */
        if(select[1].value && firstForFiltering){ /* !!! */

             val1 = Number(select[1].value); /* !!! */
             if(String(url).includes(`&on_page=`)) {
                 if (String(String(url).slice(String(url).lastIndexOf('&on_page')).length > 9+1+(VALUE1_LENGTH))) {
                     wLoc = `${String(url).slice(0, String(url).lastIndexOf('&on_page'))}&on_page=${val1}${String(url).slice(String(url).lastIndexOf('&on_page') + 9+(VALUE1_LENGTH))}`;
                 } else {
                     wLoc = `${String(url).slice(0, String(url).lastIndexOf('&on_page'))}&on_page=${val1}`;
                 }
             }else{
                if(String(url).includes(`&`)) {
                    wLoc = `${String(url).slice(0, String(url).lastIndexOf('&'))}&on_page=${val1}${String(url).slice(String(url).lastIndexOf('&'))}`;
                }else{
                    wLoc = `${String(url).slice(0)}&on_page=${val1}`;
                }
             }

             if(wLoc){
                 window.location = `${String(wLoc).slice(0, String(url).lastIndexOf('?page=')+6)}1${String(wLoc).slice(String(url).lastIndexOf('?page=')+6+pageLgt)}`;
             }

            firstForFiltering = false;
        }
    });

    $(select[0]).on('change', function () {
        if(select[0].value && firstForSorting){ /* !!! */

            val0 = String(select[0].value); /* !!! */
            // alert(val0);

            let translated_val0;
            if (val0 === 'За зростанням ціни'){
                translated_val0 = 'price';
            }else if (val0 === 'За спаданням ціни'){
                translated_val0 = 'price1';
            }else if (val0 === 'За назвою'){
                translated_val0 = 'title';
            }else if (val0 === 'За новизною'){
                translated_val0 = 'created1';
            }

             if(String(url).includes(`&order_by=`)) {
                 if (String(String(url).slice(String(url).lastIndexOf('&order_by')).length > 10+1+(VALUE2_LENGTH))) {
                     wLoc = `${String(url).slice(0, String(url).lastIndexOf('&order_by'))}&order_by=${translated_val0}${String(url).slice(String(url).lastIndexOf('&order_by')+10+(VALUE2_LENGTH))}`;
                 } else {
                     wLoc = `${String(url).slice(0, String(url).lastIndexOf('&order_by'))}&order_by=${translated_val0}`;
                 }
             }else{
                if(String(url).includes(`&`)) {
                    wLoc = `${String(url).slice(0, String(url).lastIndexOf('&'))}&order_by=${translated_val0}${String(url).slice(String(url).lastIndexOf('&'))}`;
                }else{
                    wLoc = `${String(url).slice(0)}&order_by=${translated_val0}`;
                }
             }

             if(wLoc){
                 window.location = `${String(wLoc).slice(0, String(url).lastIndexOf('?page=')+6)}1${String(wLoc).slice(String(url).lastIndexOf('?page=')+6+pageLgt)}`;
             }

            firstForSorting = false;
        }
    });
}





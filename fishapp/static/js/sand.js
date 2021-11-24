//
// const handheld = window.matchMedia(
// 'handheld, all and (max-width:990px)'
// );
// let URL_STRING_ENCODE = {
//     'price': 'За зростанням ціни',
//     'price1': 'За спаданням ціни',
//     'title': 'За назвою',
//     'created1': 'За новизною',
// };
//
// let select;
//
// if (handheld.matches){
//     select = $('.new-select');
// } else {
//     select = $('.new-mobile-select');
// }
//
// let firstForFiltering = true;
// let firstForSorting = true;
// let url = document.location;
// let val0 = select[0];
// let val1 = select[1];
//
//
// if (handheld.matches ? true: (val1 || val0)){
//     if (handheld.matches){
//         val0 = select[0].value;
//         val1 = select[1].value;
//     }else{
//         val0 = select[0].textContent;
//         val1 = select[1].textContent;
//     }
//
//     let VALUE_LENGTH, VALUE;
//     let sliceFromFilterPlus10;
//
//     if (String(url).includes(`&on_page=`)){
//         if (handheld.matches){
//             select[1].value = `${String(url).slice(String(url).lastIndexOf('&on_page')+9, String(url).lastIndexOf('&on_page')+11)}`;
//         }else{
//             select[1].textContent = `${String(url).slice(String(url).lastIndexOf('&on_page')+9, String(url).lastIndexOf('&on_page')+11)}`;
//         }
//     }
//     if (String(url).includes(`&order_by=`)){
//         sliceFromFilterPlus10 = `${String(url).slice(String(url).lastIndexOf('&order_by')+10)}`;
//         if (sliceFromFilterPlus10.includes('&')){
//             VALUE_LENGTH = sliceFromFilterPlus10.slice(0, sliceFromFilterPlus10.indexOf('&')).length;
//             VALUE = sliceFromFilterPlus10.slice(0, sliceFromFilterPlus10.indexOf('&'));
//         }else{
//             VALUE_LENGTH = sliceFromFilterPlus10.length;
//             VALUE = sliceFromFilterPlus10;
//         }
//
//         if (handheld.matches){
//             select[0].value = URL_STRING_ENCODE[`${VALUE}`];
//         }else{
//             select[0].textContent = URL_STRING_ENCODE[`${VALUE}`];
//         }
//
//     }
//
//     let choice = handheld.matches ? 'change': 'DOMSubtreeModified';
//     $(select[1]).on(choice, function () {
//         alert(1);
//         if((handheld.matches ? select[1].value: select[1].textContent) && firstForFiltering){
//
//              val1 = handheld.matches ? Number(select[1].value): Number(select[1].textContent);
//
//              if(String(url).includes(`&on_page=`)) {
//                  if (String(String(url).slice(String(url).lastIndexOf('&on_page')).length > 12)) {
//                      window.location = `${String(url).slice(0, String(url).lastIndexOf('&on_page'))}&on_page=${val1}${String(url).slice(String(url).lastIndexOf('&on_page') + 11)}`;
//                  } else {
//                      window.location = `${String(url).slice(0, String(url).lastIndexOf('&on_page'))}&on_page=${val1}`;
//                  }
//              }else{
//                 if(String(url).includes(`&`)) {
//                     window.location = `${String(url).slice(0, String(url).lastIndexOf('&'))}&on_page=${val1}${String(url).slice(String(url).lastIndexOf('&'))}`;
//                 }else{
//                     window.location = `${String(url).slice(0)}&on_page=${val1}`;
//                 }
//              }
//
//             firstForFiltering = false;
//         }
//     });
//     alert(`${choice}`);
//     $(select[0]).on(`${choice}`, function () {
//         if((handheld.matches ? select[0].value: select[0].textContent) && firstForSorting){
//
//             val0 = handheld.matches ? String(select[0].value): String(select[0].textContent);
//             // alert(val0);
//
//             let translated_val0;
//             if (val0 === 'За зростанням ціни'){
//                 translated_val0 = 'price';
//             }else if (val0 === 'За спаданням ціни'){
//                 translated_val0 = 'price1';
//             }else if (val0 === 'За назвою'){
//                 translated_val0 = 'title';
//             }else if (val0 === 'За новизною'){
//                 translated_val0 = 'created1';
//             }
//
//              if(String(url).includes(`&order_by=`)) {
//                  if (String(String(url).slice(String(url).lastIndexOf('&order_by')).length > 10+1+(VALUE_LENGTH))) {
//                      window.location = `${String(url).slice(0, String(url).lastIndexOf('&order_by'))}&order_by=${translated_val0}${String(url).slice(String(url).lastIndexOf('&order_by')+10+(VALUE_LENGTH))}`;
//                  } else {
//                      window.location = `${String(url).slice(0, String(url).lastIndexOf('&order_by'))}&order_by=${translated_val0}`;
//                  }
//              }else{
//                 if(String(url).includes(`&`)) {
//                     window.location = `${String(url).slice(0, String(url).lastIndexOf('&'))}&order_by=${translated_val0}${String(url).slice(String(url).lastIndexOf('&'))}`;
//                 }else{
//                     window.location = `${String(url).slice(0)}&order_by=${translated_val0}`;
//                 }
//              }
//
//             firstForSorting = false;
//         }
//     });
// }

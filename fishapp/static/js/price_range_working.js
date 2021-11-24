
function recalculatePricerange(){
  let parent = document.querySelector(".price-slider");
  if(!parent) return;

  let
    rangeS = parent.querySelectorAll("input[type=range]"),
    numberS = parent.querySelectorAll("input[type=number]");

  rangeS.forEach(function(el) {
    el.oninput = function() {
      if (timerId){
        clearTimeout(timerId);
      }

      let slide1 = parseFloat(rangeS[0].value),
            slide2 = parseFloat(rangeS[1].value);

      if (slide1 > slide2) {
        [slide1, slide2] = [slide2, slide1];
      }

      numberS[0].value = slide1;
      numberS[1].value = slide2;

      Min.attr('value', slide1);
      Max.attr('value', slide2);

      setTimeForMinMax();
    }
  });

  numberS.forEach(function(el) {
    el.oninput = function() {
      if (timerId){
        clearTimeout(timerId);
      }
      // let timeInMs1 = Date.now();
      // alert(timeInMs1);

      let number1 = parseFloat(numberS[0].value),
      number2 = parseFloat(numberS[1].value);


      // let oldMinVal = Min.attr('value');

      if (number1 > number2) {
        let tmp = number1;
        numberS[0].value = number2;
        numberS[1].value = tmp;
      }

      rangeS[0].value = number1;
      rangeS[1].value = number2;

      Min.attr('value', number1);
      Max.attr('value', number2);

      setTimeForMinMax();
    }
  });
}

let Min = $('#input1_number');
let Max = $('#input2_number');
let url = document.location;
let VALUE0_LENGTH, VALUE1_LENGTH, VALUE0, VALUE1;
let slice0, slice1;

if (String(url).includes(`&min=`)) {
  slice0 = `${String(url).slice(String(url).lastIndexOf('&min') + 5)}`;
  if (slice0.includes('&')) {
    VALUE0_LENGTH = slice0.slice(0, slice0.indexOf('&')).length;
    VALUE0 = slice0.slice(0, slice0.indexOf('&'));
  } else {
    VALUE0_LENGTH = slice0.length;
    VALUE0 = slice0;
  }

  Min.attr('value', `${VALUE0}`);
}
if (String(url).includes(`&max=`)) {
  slice1 = `${String(url).slice(String(url).lastIndexOf('&max') + 5)}`;
  if (slice1.includes('&')) {
    VALUE1_LENGTH = slice1.slice(0, slice1.indexOf('&')).length;
    VALUE1 = slice1.slice(0, slice1.indexOf('&'));
  } else {
    VALUE1_LENGTH = slice1.length;
    VALUE1 = slice1;
  }

  Max.attr('value', `${VALUE1}`);
}

let pgLgt;
 if (String(url).includes(`?page=`)){
    let slc = `${String(url).slice(String(url).lastIndexOf('?page=')+6)}`;
    if (slc.includes('&')){
        pgLgt = slc.slice(0, slc.indexOf('&')).length;
    }else{
        pgLgt = slc.length;
    }
 }

let timerId;
function setTimeForMinMax(){
  timerId = setTimeout(
() => {
    if (Number(Min.attr('value')) >= Number(Min.attr('min'))
        && Number(Min.attr('value')) <= Number(Min.attr('max'))
        && Number(Max.attr('value')) >= Number(Min.attr('min'))
        && Number(Max.attr('value')) <= Number(Min.attr('max'))) {

      /* Start Big Block */

      let val0 = Number(Min.attr('value'));
      let val1 = Number(Max.attr('value'));
      // alert(val0);

      if(val0 || val1){

        if(Number(val0 > val1)){
          let temp = val0;
          val0 = val1;
          val1 = temp;
        }

         // val1 = Number(select[1].textContent);
         if(String(url).includes(`&min=`)) {
             if (String(String(url).slice(String(url).lastIndexOf('&min')).length > 5+1+(VALUE0_LENGTH))) {
                 url = `${String(url).slice(0, String(url).lastIndexOf('&min'))}&min=${val0}${String(url).slice(String(url).lastIndexOf('&min')+5+(VALUE0_LENGTH))}`;
             } else {
                 url = `${String(url).slice(0, String(url).lastIndexOf('&min'))}&min=${val0}`;
             }
         }else{
            if(String(url).includes(`&`)) {
                url = `${String(url).slice(0, String(url).lastIndexOf('&'))}&min=${val0}${String(url).slice(String(url).lastIndexOf('&'))}`;
            }else{
                url = `${String(url).slice(0)}&min=${val0}`;
            }
         }

         if(String(url).includes(`&max=`)) {
           if (String(String(url).slice(String(url).lastIndexOf('&max')).length > 5+1+(VALUE1_LENGTH))) {
               url = `${String(url).slice(0, String(url).lastIndexOf('&max'))}&max=${val1}${String(url).slice(String(url).lastIndexOf('&max')+5+(VALUE1_LENGTH))}`;
           } else {
               url = `${String(url).slice(0, String(url).lastIndexOf('&max'))}&max=${val1}`;
           }
       }else{
          if(String(url).includes(`&`)) {
              url = `${String(url).slice(0, String(url).lastIndexOf('&'))}&max=${val1}${String(url).slice(String(url).lastIndexOf('&'))}`;
          }else{
              url = `${String(url).slice(0)}&max=${val1}`;
          }
       }
         window.location = `${String(url).slice(0, String(url).lastIndexOf('?page=')+6)}1${String(url).slice(String(url).lastIndexOf('?page=')+6+pgLgt)}`;
      }

      /* End Big Block */
    }
  }, 4*1000)
}

(function(){
  recalculatePricerange()
})();

window.onresize=function (){
  recalculatePricerange()
}

$('#cancel_filter_criss_cross').on('click', function (event){
    event.preventDefault();
    let input1 = $('#input1_number');
    let input2 = $('#input2_number');

    input1.attr('value', `${input1.attr('min')}`);
    input2.attr('value', `${input2.attr('max')}`);
    setTimeForMinMax();
})


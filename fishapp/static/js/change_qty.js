function initCart() {
    let timerId;
    $('#ajax-td input[type="number"]').change(function(event){
        if (timerId){
            clearTimeout(timerId);
          }

        let box = $(this);
        let MAX = Number(box.attr('max'))-1;
        // alert(MAX);

        // if (box.val() >= 1 && box.val() <= MAX){
            timerId = setTimeout(() => {

                $.ajax(box.data('url'), {
                    'type': 'POST',
                    'async': true,
                    'dataType': 'json',
                    'data': { /*набір параметрів, що підуть в тіло поста - змінні,
                     які будуть доступні на серверній стороні через словник request.POST; !!!!!!!!!!!!!!!!! */
                        'value': box.val(),

                        // 'date': box.data('date'),
                        /*перевіряємо чи даний клік по чекбоксу поставив чи забрав галочку;
                        відповідно, якщо поставив галочку - відсилаємо на сервер під ключем
                        “present” значення “1”, в протилежному випадку - порожню стрічку;
                        метод is допомагає визначити чи даний об’єкт задоволняє селектору
                        “:checked”; “:checked” вказує на те, чи поточний елемент є вибраним;*/

                        // 'present': box.is(':checked') ? '1': '',
                        /*для перевірки на серверній стороні і підтвердження
                        того, що наш запит зроблений дійсно із сторінки Відвідування;*/
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    // 'beforeSend': function(xhr, settings){
                    //     indicator.show();
                    // },
                    'error': function(xhr, status, error){
                        // alert(error);
                        // indicator.hide();
                    },
                    'success': function(data, status, xhr) {
                        if (data['key']) {
                            location.reload(true);
                        }
                    }
                });
            }, 1000)

        // }else{
            if (MAX){
                if (box.val() < 1){
                    box.val(1);
                    $(this).attr('title', 'Мінімум - 1');
                    $(this).tooltip('dispose')
                    $(this).tooltip('show');
                }else if (box.val() > MAX){
                    box.val(MAX);
                    $(this).attr('title', `на складі не більше ${MAX} шт.`);
                    $(this).tooltip('dispose')
                    $(this).tooltip('show');
                }
            }else{
                if (box.val() < 1){
                    box.val(1);
                    $(this).attr('title', 'Мінімум - 1');
                    $(this).tooltip('dispose')
                    $(this).tooltip('show');
                }
            }
        // }
    });
}


$(document).ready(function () {
    initCart();
});
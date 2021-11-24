
function setCookie() {
    let url = document.location;
    // alert(url)

    $.ajax({
        'url': url,
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function (xhr, status, error) {
            // alert(error); /*!!!!!!!!!!!!!!!!*/
        },
        'success': function (data, status, xhr) {
            if (data["status"] === "OK") {
                let existing = Cookies.get('seen_products');

                if (existing) {
                    existing = existing.split(',');

                    if (!existing.includes(String(data["prod_id"]))) {
                        existing.push(String(data["prod_id"]));
                        Cookies.set('seen_products', existing, {'path': '/', 'expires': 30});
                    }

                }else{
                    Cookies.set('seen_products', String(data["prod_id"]), {'path': '/', 'expires': 30});
                }

            }
        }
    });
}


$(document).ready(function (){
    setCookie();
    // alert(document.location);
});
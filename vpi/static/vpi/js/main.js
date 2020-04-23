const user_input = $("#user-input")
const search_icon = $('#search-icon')
const vpis_div = $('#replaceable-content')
//const datatable_div = $('#dataTable')
const endpoint = '/vpi/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            vpis_div.fadeTo('fast', 0).promise().then(() => {
                // replace the HTML contents
                vpis_div.html(response['html_from_view'])
                // fade-in the div with new contents
                vpis_div.fadeTo('fast', 1)
                // stop animating search icon
                search_icon.removeClass('blink')
                // re-attach datatable bindings
                attach_datatable_bindings()
            })
            if (request_parameters['q']) {
                $('#search-results-title').html("Zoekresultaten")
            } else {
                $('#search-results-title').html("Alle VPI's")
                //re-attach datatable bindings
            }


        })
}

let attach_datatable_bindings = function () {
    table = $('#dataTable').DataTable( {
        searching: false,
        language: {
            lengthMenu: "Resultaten per pagina: _MENU_",
            paginate: {
                "previous": "Vorige",
                "next": "Volgende"
            },
            info: "Pagina _PAGE_ van _PAGES_",

        }
    });
}

$(document).ready(function() {
    attach_datatable_bindings()
})

user_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }

    // start animating the search icon with the CSS class
    search_icon.addClass('blink')

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
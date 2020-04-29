$(document).ready(function() {
    $('#formsTable').DataTable( {
        language: {
            lengthMenu: "Resultaten per pagina: _MENU_",
            paginate: {
                "previous": "Vorige",
                "next": "Volgende",
            },
            search: "Zoeken",
            info: "Pagina _PAGE_ van _PAGES_",

        }
    })
})

$(":file").filestyle();

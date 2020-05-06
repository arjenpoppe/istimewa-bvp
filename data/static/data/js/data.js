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

// $(":file").filestyle();

$("#project-select").change(function () {
  var project_number = $(this).val();

  var pm_select = document.getElementById('pm-select');
  var length = pm_select.options.length;
  for (i = length-1; i >= 0; i--) {
    pm_select.options[i] = null;
  }

  if (project_number !== "") {
       $.ajax({
          url: 'ajax/get_pms',
          data: {
              'project_number': project_number
          },
          dataType: 'json',
          success: function (data) {
              $.each(data.numbers, function(key, number){
                var option = new Option('prestatiemeting #'.concat(number), number);
                $("#pm-select").append(option);
              });
              console.log(data.numbers)
              var new_number = 1;
              if (data.numbers && data.numbers.length) {
                  new_number = Math.max.apply(Math, data.numbers) + 1;
              }
              var static_option = new Option('prestatiemeting #'.concat(new_number, ' (nieuw)' ), new_number);
              $("#pm-select").append(static_option);
              //Change the text of the default "loading" option.
          }
       })
  }


});
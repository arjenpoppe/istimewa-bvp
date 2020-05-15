$("#project-select").change(function () {
  var project_number = $(this).val();

  console.log('called')

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
              //Change the text of the default "loading" option.
          }
       })
  }
});


/* Start State and city ajax - js */
$("#state").change(function () {
      var url = $("#indexForm").attr("data-city-url");  // get the url of the `load_courses` view
      var stateId = $(this).val();  // get the selected programming ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/load-courses/)
        data: {
          'state': stateId       // add the programming id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_courses` view function
          $("#city").html(data);  // replace the contents of the course input with the data that came from the server
        }
      });

    });
/* End State and city ajax - js */



$(document).ready(function() {

    var csrftoken = $('meta[name="csrf-token"]').attr('content');

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#blah').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]); // convert to base64 string
        }
    }

    $('.addNewEmp').on('click', function() {
        $.ajax({
        url: '/get_next_emp_code/',
        method: 'GET',
        success: function(data) {
            if (data.next_emp_code) {
            $('#EmpCode1').val(data.next_emp_code);
            $('#addEmpModal').modal('show');
            }
        },
        error: function(xhr, errmsg, err) {
            Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Something went wrong!'
            });
        }
        });
    });
    
    $("#EmpImg").change(function(e) {
        e.preventDefault()
        readURL(this);
    });
    
    $("#blah").click(function(e) {
        e.preventDefault()
        $("#EmpImg").click();
    });

    $('.addEmpForm').submit(function(event) {
        event.preventDefault(); // Prevent form submission

        let formData = new FormData(this); // Create a FormData object from the form
        // console.log(formData);

          $.ajax({
              type: 'POST',
              url: '/crudemployee/',
              data: formData,
              processData: false, // Prevent jQuery from automatically transforming the data into a query string
              contentType: false, // Tell jQuery not to set the content type
              headers: {
                  'X-CSRFToken': csrftoken
              },
              success: function(response) {
                  if (response.success) {
                      Swal.fire({
                          icon: 'success',
                          title: 'Employee added successfully!',
                          confirmButtonColor: '#08655D',
                          showConfirmButton: true,
                          confirmButtonText: "Ok"
                      }).then(function() {
                          window.location.href = ''; // Redirect after success
                      });
                  } else {
                      Swal.fire({
                          icon: 'error',
                          title: 'Oops...',
                          text: response.error_message || 'Something went wrong!'
                      });
                  }
              },
              error: function(xhr, errmsg, err) {
                  Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'Something went wrong!'
                  });
              }
          });
      });

      // Attach event listener for image click to trigger file input
      $('[id^=blah_update_]').click(function() {
        var empCode = $(this).attr('id').split('_').pop();
        $('#EmpImg_update_' + empCode).click();
      });

      // Update image preview on file selection
      $('[id^=EmpImg_update_]').change(function() {
        var empCode = $(this).attr('id').split('_').pop();
        var input = this;
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          reader.onload = function(e) {
            $('#blah_update_' + empCode).attr('src', e.target.result);
          }
          reader.readAsDataURL(input.files[0]);
        }
      });

      $('.updateEmpForm').submit(function(event) {
        event.preventDefault(); // Prevent form submission

        let formData = new FormData(this); // Create a FormData object from the form

        $.ajax({
            type: 'POST',
            url: '/crudemployee/',
            data: formData,
            processData: false, // Prevent jQuery from automatically transforming the data into a query string
            contentType: false, // Tell jQuery not to set the content type
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Employee updated successfully!',
                        confirmButtonColor: '#08655D',
                        showConfirmButton: true,
                        confirmButtonText: "Ok"
                    }).then(function() {
                        window.location.href = ''; // Redirect after success
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.error_message || 'Something went wrong!'
                    });
                }
            },
            error: function(xhr, errmsg, err) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!'
                });
            }
        });
    });

    $('.deleteEmpForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission

      let formData = new FormData(this); // Create a FormData object from the form
      
      $.ajax({
          type: 'POST',
          url: '/crudemployee/',
          data: formData,
          processData: false, // Prevent jQuery from automatically transforming the data into a query string
          contentType: false, // Tell jQuery not to set the content type
          headers: {
              'X-CSRFToken': csrftoken
          },
          success: function(response) {
              if (response.success) {
                  Swal.fire({
                      icon: 'success',
                      title: 'Employee deleted successfully!',
                      confirmButtonColor: '#08655D',
                      showConfirmButton: true,
                      confirmButtonText: "Ok"
                  }).then(function() {
                      window.location.href = ''; // Redirect after success
                  });
              } else {
                  Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: response.error_message || 'Something went wrong!'
                  });
              }
          },
          error: function(xhr, errmsg, err) {
              Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Something went wrong!'
              });
          }
      });
  });
         
   });
$(document).ready(function() {

    var csrftoken = $('meta[name="csrf-token"]').attr('content');

    $('.update_or_file').submit(function(event) {
        event.preventDefault(); // Prevent form submission

        let formData = new FormData(this); // Create a FormData object from the form
        // console.log(formData);

          $.ajax({
              type: 'POST',
              url: '/upload_or_file/',
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
                          title: 'File updated successfully!',
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

    //   $('.generateReceiptList').click(function(event) {
    //     event.preventDefault();

    //     var collDate = document.getElementById('collDate').value;
    //     var c_branch_name = document.getElementById('c_branch_name').value;

    //     $.ajax({
    //         type: 'POST',
    //         url: '/read_dbf_file/',
    //         data: { collDate: collDate, c_branch_name: c_branch_name },
    //         headers: {
    //             'X-CSRFToken': csrftoken
    //         },
    //         success: function(response) {
    //             if (response.success) {
    //                 Swal.fire({
    //                     icon: 'success',
    //                     title: 'File updated successfully!',
    //                     confirmButtonColor: '#08655D',
    //                     showConfirmButton: true,
    //                     confirmButtonText: "Ok"
    //                 }).then(function() {
    //                     window.location.href = ''; // Redirect after success
    //                 });
    //             } else {
    //                 Swal.fire({
    //                     icon: 'error',
    //                     title: 'Oops...',
    //                     text: response.error_message || 'Something went wrong!'
    //                 });
    //             }
    //         },
    //         error: function(xhr, errmsg, err) {
    //             Swal.fire({
    //                 icon: 'error',
    //                 title: 'Oops...',
    //                 text: 'Something went wrong!'
    //             });
    //         }
    //     });
    // });
})
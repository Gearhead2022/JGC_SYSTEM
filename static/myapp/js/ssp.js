$(document).ready(function() {

    var csrftoken = $('meta[name="csrf-token"]').attr('content');

    $('.update_ssp_ledger_file').submit(function(event) {
        event.preventDefault(); // Prevent form submission

        let formData = new FormData(this); // Create a FormData object from the form
     
        $.ajax({
            type: 'POST',
            url: '/upload_ssp_ledger_file/',
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

    $('.table_ssp_ledger').DataTable({
        serverSide: true,
        processing: true,
        searching: true,
        ajax: {
            url: '/get_ssp_ledger_data/',
            type: 'GET',
            data: function (d) {
                // Send extra parameters if needed
                d.page = Math.ceil(d.start / d.length) + 1;
                d.pageSize = d.length;
                d.searchValue = d.search.value;  // DataTables search value
                d.sortColumnIndex = d.order.length > 0 ? d.order[0].column : 0;  // Default to the first column if not provided
                d.sortDirection = d.order.length > 0 ? d.order[0].dir : 'asc';   // Default to ascending if not provided
            },
            dataSrc: function (json) {
                if (json.error) {
                    console.error('Error loading data:', json.error);
                    return [];
                }
                return json.data;
            }
        },
        columns: [
            { data: 'ssp_ref' },  // Ensure 'action' column is not sortable
            { data: 'ssp_folio' },
            { data: 'ssp_tcode' },
            { data: 'ssp_tdate' },
            { data: 'ssp_desc' },
            { data: 'ssp_amount' },
            { data: 'ssp_old_ref' },
            { data: 'ssp_atm_bal' }
        ]
    });


});
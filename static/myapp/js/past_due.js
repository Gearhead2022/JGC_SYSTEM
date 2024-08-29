$(document).ready(function() {

  var csrftoken = $('meta[name="csrf-token"]').attr('content');

  $('.table_pastdue').DataTable({
    serverSide: true,
    processing: true,
    searching: true,
    ajax: {
        url: '/get_past_due_data/',
        type: 'GET',
        data: function (d) {
            // Send extra parameters needed by the server
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
        { data: 'action', orderable: false }, // Action column (not sortable)
        { data: 'account_id' },
        { data: 'full_name' },
        { data: 'pd_type' },
        { data: 'pd_class' },
        { data: 'pd_bank' },
        { data: 'pd_refdate' },
        { data: 'branch_name' }
    ]
});

  $('.addLedgerForm').submit(function(event) {
    event.preventDefault();

    let formData = new FormData(this);
    // console.log(formData);
      $.ajax({
          type: 'POST',
          url: '/add_ledger/',
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
                      title: 'Data has been succesfully saved!',
                      confirmButtonColor: '#08655D',
                      showConfirmButton: true,
                      confirmButtonText: "Ok"
                  }).then(function() {
                      window.location.href = '';
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

  $('.editLedgerForm').submit(function(event) {
      event.preventDefault();

      let formData = new FormData(this); 
      // console.log(formData);
        $.ajax({
            type: 'POST',
            url: '/edit_ledger/',
            data: formData,
            processData: false, 
            contentType: false, 
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Data has been succesfully saved!',
                        confirmButtonColor: '#08655D',
                        showConfirmButton: true,
                        confirmButtonText: "Ok"
                    }).then(function() {
                        window.location.href = '';
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

    $('.table_ledger').on('click', 'tbody .btn_delete_ledger', function(event) {
      event.preventDefault();

        var ledger_id = $(this).attr('data-ledger-id');

        if (!ledger_id) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Ledger ID not found!'
            });
            return;
        }

        Swal.fire({
            icon: 'warning',
            title: 'Are you sure you want to delete this data?',
            confirmButtonColor: '#08655D',
            showConfirmButton: true,
            showCancelButton: true,
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel!'
        }).then(function(response) {
            if(response.value==true){
                $.ajax({
                    type: 'POST',
                    url: '/delete_ledger_view/',
                    data: { ledger_id: ledger_id },
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Data has been succesfully deleted!',
                                confirmButtonColor: '#08655D',
                                showConfirmButton: true,
                                confirmButtonText: "Ok"
                            }).then(function() {
                                window.location.href = '';
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
                })
            }
        });
    });

    $(".print_ledger").on("click", function() {
        var account_id = $(this).attr("account-id");
        var branch_name = $(this).attr("branch-name");
        var proxy_url = `http://127.0.0.1:8003/print_ledger.php?account_id=${account_id}&branch_name=${branch_name}`;
        
        window.open(proxy_url);
    });


    $('#add_pdr_account_modal .modal-body').on("change", "#auto_fill_id", function() {
        if (this.checked) {
            var branch_name = document.getElementById('branch_name').value;
    
            $.ajax({
                url: '/get_next_olr_id_series/',
                data: {
                    branch_name: branch_name
                },
                type: "GET",
                success: function(data) {
                    $("#account_id").val(data.next_olr_id);
                    $("#account_id").attr('readonly', true);
                    $("#message2").removeAttr('hidden');
                },
                error: function() {
                    swal.close();
                    alert('Error fetching data');
                }
            });
        } else {
            $("#account_id").val("");
            $("#account_id").attr('readonly', false);
            $("#message2").attr('hidden', true);
        }
    });
    $(".table_pastdue").on("click", "tbody .btn_edit_past_due", function () {
        var past_due_id = $(this).attr('data-past-due-id');

        $.ajax({
            type: 'POST',
            url: '/view_edit_past_due/',  // URL for Django view handling
            data: {past_due_id: past_due_id},
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data.success) {
                    // Populate the modal with received data
                    $("#edit_id_pd").val(data.id);
                    $("#edit_pd_account_id").val(data.account_id);
                    $("#edit_pd_first_name").val(data.pd_first_name);
                    $("#edit_pd_middle_name").val(data.pd_middle_name);
                    $("#edit_pd_last_name").val(data.pd_last_name);
                    $("#edit_pd_class").val(data.pd_class);
                    $("#edit_pd_address").val(data.pd_address);
                    $("#edit_pd_age").val(data.pd_age);
                    $("#edit_pd_balance").val(data.pd_balance);
                    $("#edit_pd_refdate").val(data.pd_refdate);
                    $("#edit_pd_type").val(data.pd_type);
                    $("#edit_pd_bank").val(data.pd_bank);
                   
                    $("#edit_pdr_account").modal('show');
                } else {
                    Swal.fire({
                        icon: 'warning',
                        title: 'No Data',
                        text: 'No records found!'
                    });
                }
            },
            error: function (xhr, errmsg, err) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!'
                });
            }
        });
    });

    $(".table_pastdue").on("click", "tbody .btn_view_past_due", function () {
        var past_due_id = $(this).attr('data-past-due-id');
    
        $.ajax({
            type: 'POST',
            url: '/view_edit_past_due/',
            data: { past_due_id: past_due_id },
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data.success) {
                    // Populate the modal with received data
                    $("#view_pd_account_id").text(data.account_id);
                    $("#view_pd_full_name").text(data.pd_first_name + " " + data.pd_middle_name + " " + data.pd_last_name);
                    $("#view_pd_age").text(data.pd_age);
                    $("#view_pd_branch_name").text(data.branch_name);
                    $("#view_pd_address").text(data.pd_address);
                    $("#view_pd_balance").text(data.pd_balance);
                    $("#view_pd_bank").text(data.pd_bank);
                    $("#view_pd_type").text(data.pd_type);
                    $("#view_pd_class").text(data.pd_class);
                    $("#view_pd_refdate").text(data.pd_refdate);
    
                    // Dynamically set the View Ledger button URL
                    $('#btn_view_ledger').attr('onclick', `location.href='/past_due_ledger/${data.account_id}'`);
    
                    // Show the modal
                    $("#view_pdr_account_modal").modal('show');
                } else {
                    Swal.fire({
                        icon: 'warning',
                        title: 'No Data',
                        text: 'No records found!'
                    });
                }
            },
            error: function (xhr, errmsg, err) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!'
                });
            }
        });
    });

    $('.btn_add_pdr_account').on('click', function() {
        $.ajax({
        url: '/get_next_past_due_code/',
        method: 'GET',
        success: function(data) {
            if (data.next_pd_code) {
                $('#add_due_id').val(data.next_pd_code);
                $('#add_pdr_account_modal').modal('show');
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

    $('.addPastDueAccountForm').submit(function(event) {
        event.preventDefault();
    
        let formData = new FormData(this);
        // console.log(formData);
          $.ajax({
              type: 'POST',
              url: '/add_past_due/',
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
                          title: 'Data has been succesfully saved!',
                          confirmButtonColor: '#08655D',
                          showConfirmButton: true,
                          confirmButtonText: "Ok"
                      }).then(function() {
                          window.location.href = '';
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

    $('.updatePastDueAccountForm').submit(function(event) {
        event.preventDefault();
    
        let formData = new FormData(this);
        // console.log(formData);
        $.ajax({
            type: 'POST',
            url: '/update_past_due/',
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
                        title: 'Data has been succesfully saved!',
                        confirmButtonColor: '#08655D',
                        showConfirmButton: true,
                        confirmButtonText: "Ok"
                    }).then(function() {
                        window.location.href = '';
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

    $(".table_pastdue").on("click", "tbody .btn_delete_past_due", function () {
        var past_due_id = $(this).attr('data-past-due-id');
          if (!past_due_id) {
              Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Ledger ID not found!'
              });
              return;
          }
          Swal.fire({
              icon: 'warning',
              title: 'Are you sure you want to delete this data?',
              confirmButtonColor: '#08655D',
              showConfirmButton: true,
              showCancelButton: true,
              cancelButtonColor: '#d33',
              confirmButtonText: 'Yes, delete it!',
              cancelButtonText: 'No, cancel!'
          }).then(function(response) {
              if(response.value==true){
                  $.ajax({
                      type: 'POST',
                      url: '/delete_past_due/',
                      data: { past_due_id: past_due_id },
                      headers: {
                          'X-CSRFToken': csrftoken
                      },
                      success: function(response) {
                          if (response.success) {
                              Swal.fire({
                                  icon: 'success',
                                  title: 'Data has been succesfully deleted!',
                                  confirmButtonColor: '#08655D',
                                  showConfirmButton: true,
                                  confirmButtonText: "Ok"
                              }).then(function() {
                                  window.location.href = '';
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
                  })
              }
          });
      });
});

//admin Side

$('.table_pastdue_ledger').DataTable({
    serverSide: true,
    processing: true,
    searching: true,
    ajax: {
        url: '/get_past_due_ledger_data/',
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
        { data: 'action', orderable: false },  // Ensure 'action' column is not sortable
        { data: 'account_id' },
        { data: 'full_name' },
        { data: 'pdl_date' },
        { data: 'pdl_refno' },
        { data: 'pdl_debit' },
        { data: 'pdl_credit' },
        { data: 'branch_name' }
    ]
});

    $(".table_pastdue_ledger").on("click", "tbody .btn_edit_past_due_ledger", function () {
        var past_due_id = $(this).attr('data-past-due-ledger-id');
        alert(past_due_id);

    });






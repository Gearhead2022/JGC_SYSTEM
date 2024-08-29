
$(document).ready(function() {

    var csrftoken = $('meta[name="csrf-token"]').attr('content');


    $('.addNewEvent').on('click', function() {
        $.ajax({
        url: '/get_next_event_id/',
        method: 'GET',
        success: function(data) {
            if (data.next_event_code) {
            $('#event_id1').val(data.next_event_code);
            $('#addEventModal').modal('show');
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


    $('.addEventForm').submit(function(event) {
        event.preventDefault(); // Prevent form submission

        let formData = new FormData(this); // Create a FormData object from the form
        // console.log(formData);

          $.ajax({
              type: 'POST',
              url: '/crudevents/',
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
                          title: 'Event added successfully!',
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

      $('.editEventForm').submit(function(event) {
        event.preventDefault(); // Prevent form submission

        let formData = new FormData(this); // Create a FormData object from the form

        $.ajax({
            type: 'POST',
            url: '/crudevents/',
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
                        title: 'Event updated successfully!',
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

    $('.deleteEventForm').submit(function(event) {
        event.preventDefault(); // Prevent form submission
  
        let formData = new FormData(this); // Create a FormData object from the form
        
        $.ajax({
            type: 'POST',
            url: '/crudevents/',
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
                        title: 'Event deleted successfully!',
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

   document.addEventListener('DOMContentLoaded', function() {

    var viewOptions = document.querySelectorAll('.view_option');

       // Attach the event listener to each radio button
       viewOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            var view = this.value;

            // Uncheck all other radio buttons
            viewOptions.forEach(function(opt) {
                if (opt !== option) {
                    opt.checked = false;
                }
            });

            // Change the calendar view
            calendar.changeView(view);
        });
    });
    
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth', // Set initial view
        selectable: true, // Allow date selecting
        dateClick: function(info) { // Date click callback
            $.ajax({
                url: '/get_next_event_id/',
                method: 'GET',
                success: function(data) {
                    if (data.next_event_code) {
                        $('#event_id1').val(data.next_event_code);
                        $('#start_date').val(info.dateStr);
                        $('#addEventModal').modal('show');
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
        },
        events: '/get_events/', // URL to fetch events
        eventContent: function(arg) {
            let titleEl = document.createElement('div');
            titleEl.innerHTML = arg.event.title;
            return { domNodes: [titleEl] };
        },
        eventClick: function(info) {
            var eventObj = info.event;

            $('#editEventModal').modal('show');
            document.getElementById('event_id_edit').value = eventObj.extendedProps.event_id;
            document.getElementById('event_title_edit').value = eventObj.title;
            document.getElementById('category_edit').value = eventObj.extendedProps.category;
            document.getElementById('start_date_edit').value = eventObj.startStr.split('T')[0];
            document.getElementById('end_date_edit').value = eventObj.endStr.split('T')[0];
            let startTime = eventObj.startStr.split('T')[1];
            let endTime = eventObj.endStr ? eventObj.endStr.split('T')[1] : '';

            function convertTo12Hour(time) {
                if (!time) return '';
                const [hours, minutes] = time.split(':');
                // const period = hours >= 12 ? 'PM' : 'AM';
                // const hour = hours % 12 || 12;
                return `${hours}:${minutes}`;
            }

            document.getElementById('start_time_edit').value = convertTo12Hour(startTime);
            document.getElementById('end_time_edit').value = convertTo12Hour(endTime);

            document.getElementById('event_id_delete').value = eventObj.extendedProps.event_id;
            document.getElementById('event_title_delete').value = eventObj.title;
        },
        eventDidMount: function(info) {
            if (info.event.extendedProps.category === 'hostel') {
                info.el.style.backgroundImage = 'linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1))';
                info.el.style.border = 'black'; // Adjust text color if needed
            } else if (info.event.extendedProps.category === 'basketball_court') {
                info.el.style.backgroundImage = 'linear-gradient(to right, rgba(62, 176, 82, 1), rgba(32, 148, 173, 1))';
                info.el.style.border = 'black'; // Adjust text color if needed
            } else if (info.event.extendedProps.category === 'kidney_pool') {
                info.el.style.backgroundImage = 'linear-gradient(to right, rgba(17, 97, 187, 1), rgba(17, 161, 187, 1))';
                info.el.style.border = 'black'; // Adjust text color if needed
            } else if (info.event.extendedProps.category === 'cabana') {
                info.el.style.backgroundImage = 'linear-gradient(to right, rgba(187, 17, 90, 1), rgba(189, 64, 51, 1))';
                info.el.style.border = 'black'; // Adjust text color if needed
            }
        }
    });

    calendar.render();

    // Handle category change
    document.getElementById('filter_category').addEventListener('change', function() {
        var selectedCategory = this.value;
        calendar.removeAllEvents(); // Remove existing events

        document.getElementById('category1').value = selectedCategory;

        $.ajax({
            url: '/get_events/', // URL to fetch events
            data: {
                category: selectedCategory
            },
            success: function(events) {
                events.forEach(function(event) {
                    calendar.addEvent(event); // Add filtered events to the calendar
                });
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

    // document.getElementsByClassName('view_option').addEventListener('checked', function() {
    //     var view = this.value;
    //     alert(view);
    // });
});
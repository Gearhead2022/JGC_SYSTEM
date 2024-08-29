$(document).ready(function() {
    // Hide the loading screen when the page is fully loaded
    $('#loading-screen').fadeOut('slow');
});

$(window).on('beforeunload', function() {
    // Show the loading screen when the page is being refreshed or a link is clicked
    $('#loading-screen').show();
});
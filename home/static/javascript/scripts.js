// This is the main javascript file where most javascript/nodeJs functions should be written
setTimeout(function() {
  $('.myAlert-bottom').alert('close')
}, 4000);

$(document).on('click', '.saveMyself', function(){
    worker = $(this).attr("data-id");
    $.ajax({
        url: '/ajax/myInformation/',
        data:{
            'employee':worker
        },
        dataType: 'json',
        success: function(data){
            $('#edit-myself-id').val(data['id_employee']);
            $('#edit-myself-name').val(data['first_name']);
            $('#edit-myself-lastname').val(data['last_name']);
            $('#edit-myself-phone').val(data['phone']);
            $('#edit-myself-city').val(data['city']);
            $('#edit-myself-country').val(data['country']);
            $('#edit-myself-email').val(data['email']);
            $('#edit-myself-username').val(data['username']);
        }
    });
});
$(document).on('click','#deleteNotifications', function(){
    $('.nrOfNotifications').text("");
    $.ajax({
        url: '/ajax/deleteNotifications/',
        data:{},
        dataType: 'json',
        success: function(data){

        }
    });
});
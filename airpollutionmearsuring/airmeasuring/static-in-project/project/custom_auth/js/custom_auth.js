$(document).ready(function () {
    $('#login-btn').on('click', function(){
    var username = $('#id_username').val(),
        password = $('#id_password').val();
    if(username === '') {
      $('.error').fadeOut('fast', function() {
        $(this).css('top', '214px');
      });
      $('.error').fadeIn('fast', function(){
        $('#id_username').focus();
      });
      return;
    }
    if(password === '') {
      $('.error').fadeOut('fast', function() {
        $(this).css('top', '269px');
      });
      $('.error').fadeIn('fast', function(){
        $('#id_password').focus();
      });
      return;
    }
    var values = [];

    $('form#myform :input').each(function(){
      var input = $(this);
      values.push(input.val());
    });
    $.ajax({
      url: '/authen/manual/check/user/',
      data: {
        'csrfmiddlewaretoken': values[0],
        'username': values[1],
        'password': values[2]
      },
      type: 'post',
      traditional: true,
      complete: function (xmlHttp, textStatus) {
        if (xmlHttp.responseText === 'successful') {
          $('#myform').submit();
        }
        else if (xmlHttp.responseText === 'failed') {
          $('.invalid-error').text('* Invalid authentication. Try again !');
          $('.invalid-error').css('display', 'block');
        }
        else {
          $('.invalid-error').text('** Internal server error, contact admin to fix it !');
          $('.invalid-error').css('display', 'block');
        }
      }
    });
  });

  $('#forgetpass-btn').on('click', function () {
    var email = $('#id_email').val(),
        filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/,
        value = $('form#myform-forgetpass :input')[0],
        recovery_code = $('#id_resetcode').val(),
        newpass = $('#id_newpassword').val(),
        retypepass = $('#id_retypepass').val();
    if (email === '' && recovery_code === '' && (newpass === '' || retypepass === '')) {
      if (email === '' && recovery_code === '' && newpass === '') {
        $('.error1').fadeOut('fast', function() {
          $(this).css('top', '214px');
        });
        $('.error1').fadeIn('fast', function(){
          $('#id_email').focus();
          $('#id_resetcode').focus();
          $('#id_newpassword').focus();
        });
      }
      else if (email === '' && recovery_code === '' && retypepass === '') {
        $('.error1').fadeOut('fast', function() {
          $(this).css('top', '268px');
        });
        $('.error1').fadeIn('fast', function(){
          $('#id_email').focus();
          $('#id_resetcode').focus();
          $('#id_retypepass').focus();
        });
      }
      return;
    }
    if (email !== '' && !filter.test(email)) {
        $('.invalid-error2').text("* Email does not match format");
        $('.invalid-error2').css('display', 'block');
        return;
    }
    else if (email !== '') {
      $.ajax({
        url: '/authen/manual/check/email/',
        data: {
          'csrfmiddlewaretoken': $(value).val(),
          'email': email
        },
        type: 'post',
        traditional: true,
        complete: function (xmlHttp, textStatus) {
          if (xmlHttp.responseText === 'successful') {
            window.location.href = '#signin';
            window.location.href = '#signup';
            $('#id_resetcode').removeAttr('type');
            $('#id_email').attr('type', 'hidden');
            $('#id_email').val('');
            $('.invalid-error2').css('display', 'none');
          }
          else if (xmlHttp.responseText === 'failed') {
            $('.invalid-error2').text('* Email does not match any records !');
            $('.invalid-error2').css('display', 'block');
          }
          else {
            $('.invalid-error2').text('** Internal server error, contact admin to fix it !');
            $('.invalid-error2').css('display', 'block');
          }
        }
      });
    }
    else if (recovery_code !== '') {
      $.ajax({
        url: '/authen/manual/check/code/',
        data: {
          'csrfmiddlewaretoken': $(value).val(),
          'code': recovery_code
        },
        type: 'post',
        traditional: true,
        complete: function (xmlHttp, textStatus) {
          if (xmlHttp.responseText === 'successful') {
            window.location.href = '#signin';
            window.location.href = '#signup';
            $('#id_newpassword').removeAttr('type');
            $('#id_newpassword').attr('type', 'password');
            $('#id_retypepass').removeAttr('type');
            $('#id_retypepass').attr('type', 'password');
            $('#id_resetcode').attr('type', 'hidden');
            $('#id_resetcode').val('');
          }
          else if (xmlHttp.responseText === 'failed') {
            $('.invalid-error2').text('* Invalid reset code. Try again !');
            $('.invalid-error2').css('display', 'block');
          }
          else if (xmlHttp.responseText === 'expired') {
            var count = 3,
                countdown = setInterval(function () {
                  $('.invalid-error2').text('* Session is expire. Redirect ' + count.toString() + ' !');
                  $('.invalid-error2').css('display', 'block');
                  if (count == 0) {
                    clearInterval(countdown);
                    window.location.href = '#signin';
                    window.location.href = '#signup';
                    $('#id_email').removeAttr('type');
                    $('#id_resetcode').attr('type', 'hidden');
                    $('#id_email').val('');
                    $('#id_resetcode').val('');
                    $('.invalid-error2').css('display', 'none');
                  }
                  count--;
                }, 1000);
          }
          else {
            $('.invalid-error2').text('** Internal server error, contact admin to fix it !');
            $('.invalid-error2').css('display', 'block');
          }
        }
      });
    }
    else if (newpass !== '' && retypepass !== '') {
      if (newpass !== retypepass) {
        $('.invalid-error2').text('* Retyped password does not match !');
        $('.invalid-error2').css('display', 'block');
        return;
      }
      $.ajax({
        url: '/authen/manual/reset/pass/',
        data: {
          'csrfmiddlewaretoken': $(value).val(),
          'newpassword': newpass
        },
        type: 'post',
        traditional: true,
        complete: function (xmlHttp, textStatus) {
          if (xmlHttp.responseText === 'successful') {
            window.open(window.location.href.split('#')[0], '_self');
          }
          else if (xmlHttp.responseText === 'expired') {
            var count = 3,
              countdown = setInterval(function () {
                $('.invalid-error2').text('* Session is expire. Redirect ' + count.toString() + ' !');
                $('.invalid-error2').css('display', 'block');
                if (count == 0) {
                  clearInterval(countdown);
                  window.location.href = '#signin';
                  window.location.href = '#signup';
                  $('#id_email').removeAttr('type');
                  $('#id_resetcode').attr('type', 'hidden');
                  $('#id_newpassword').attr('type', 'hidden');
                  $('#id_retypepass').attr('type', 'hidden');
                  $('#id_email').val('');
                  $('#id_resetcode').val('');
                  $('#id_newpassword').val('');
                  $('#id_retypepass').val('');
                  $('.invalid-error2').css('display', 'none');
                }
                count--;
            }, 1000);
          }
          else if (xmlHttp.responseText === 'failed') {
            $('.invalid-error2').text('** Internal server error, contact admin to fix it !');
            $('.invalid-error2').css('display', 'block');
          }
        }
      });
    }
  });

  $('#return_login').on('click', function () {
    setTimeout(function () {
      $('#id_email').removeAttr('type');
      $('#id_email').val('');
      $('#id_resetcode').attr('type', 'hidden');
      $('#id_resetcode').val('');
      $('#id_newpassword').attr('type', 'hidden');
      $('#id_newpassword').val('');
      $('#id_retypepass').attr('type', 'hidden');
      $('#id_retypepass').val('');
      $('.error').fadeOut('fast');
      $('.error1').fadeOut('fast');
      $('.invalid-error2').css('display', 'none');
    }, 1000);
    $('.invalid-error').css('display', 'none');
  });

  $('#id_username, #id_password, #id_email, #id_resetcode').keyup(function(){
      $('.error').fadeOut('fast');
      $('.error1').fadeOut('fast');
      $('.invalid-error').css('display', 'none');
      $('.invalid-error2').css('display', 'none');
  });

  $('#id_username, #id_password, #id_email, #id_resetcode').mouseup(function () {
    $('.error').fadeOut('fast');
    $('.error1').fadeOut('fast');
    $('.invalid-error').css('display', 'none');
    $('.invalid-error2').css('display', 'none');
  });

});
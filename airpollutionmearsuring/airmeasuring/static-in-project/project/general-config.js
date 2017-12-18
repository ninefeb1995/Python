$(document).ready(function () {

  (function($, sr) {
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function(func, threshold, execAsap) {
        var timeout;

        return function debounced() {
            var obj = this,
                args = arguments;

            function delayed() {
                if (!execAsap)
                    func.apply(obj, args);
                timeout = null;
            }

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100);
        };
    };

    // smartresize
    jQuery.fn[sr] = function(fn) {
        return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr);
    };
  })(jQuery, 'smartresize');

  var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
    $BODY = $('body'),
    $MENU_TOGGLE = $('#menu_toggle'),
    $SIDEBAR_MENU = $('#sidebar-menu'),
    $SIDEBAR_FOOTER = $('.sidebar-footer'),
    $LEFT_COL = $('.left_col'),
    $RIGHT_COL = $('.right_col'),
    $NAV_MENU = $('.nav_menu'),
    $FOOTER = $('footer');

  // Sidebar
  function init_sidebar() {
    // We need to improve: This is some kind of easy fix, maybe we can improve this
    var setContentHeight = function() {
        // reset height
        $RIGHT_COL.css('min-height', $(window).height());

        var bodyHeight = $BODY.outerHeight(),
            footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
            leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
            contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

        // normalize content
        contentHeight -= $NAV_MENU.height() + footerHeight;

        $RIGHT_COL.css('min-height', contentHeight);
    };

    $SIDEBAR_MENU.find('a').on('click', function(ev) {
        console.log('clicked - sidebar_menu');
        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
        } else {
            // prevent closing menu if we are on child menu
            if (!$li.parent().is('.child_menu')) {
                $SIDEBAR_MENU.find('li').removeClass('active active-sm');
                $SIDEBAR_MENU.find('li ul').slideUp();
            } else {
                if ($BODY.is(".nav-sm")) {
                    $SIDEBAR_MENU.find("li").removeClass("active active-sm");
                    $SIDEBAR_MENU.find("li ul").slideUp();
                }
            }
            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                setContentHeight();
            });
        }
    });

    // toggle small or large menu
    $MENU_TOGGLE.on('click', function() {
        console.log('clicked - menu toggle');

        if ($BODY.hasClass('nav-md')) {
            $SIDEBAR_MENU.find('li.active ul').hide();
            $SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
        } else {
            $SIDEBAR_MENU.find('li.active-sm ul').show();
            $SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
        }

        $BODY.toggleClass('nav-md nav-sm');

        setContentHeight();
    });

    // check active menu
    $SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

    $SIDEBAR_MENU.find('a').filter(function() {
        return this.href == CURRENT_URL;
    }).parent('li').addClass('current-page').parents('ul').slideDown(function() {
        setContentHeight();
    }).parent().addClass('active');

    // recompute content when resizing
    $(window).smartresize(function() {
        setContentHeight();
    });

    setContentHeight();

    // fixed sidebar
    if ($.fn.mCustomScrollbar) {
        $('.menu_fixed').mCustomScrollbar({
            autoHideScrollbar: true,
            theme: 'minimal',
            mouseWheel: { preventDefault: true }
        });
    }
  };
  // End Sidebar

  // Panel toolbox
  $(document).ready(function() {
      $('.collapse-link').on('click', function() {
          var $BOX_PANEL = $(this).closest('.x_panel'),
              $ICON = $(this).find('i'),
              $BOX_CONTENT = $BOX_PANEL.find('.x_content');

          // fix for some div with hardcoded fix class
          if ($BOX_PANEL.attr('style')) {
              $BOX_CONTENT.slideToggle(200, function() {
                  $BOX_PANEL.removeAttr('style');
              });
          } else {
              $BOX_CONTENT.slideToggle(200);
              $BOX_PANEL.css('height', 'auto');
          }

          $ICON.toggleClass('fa-chevron-up fa-chevron-down');
      });

      $('.close-link').click(function() {
          var $BOX_PANEL = $(this).closest('.x_panel');

          $BOX_PANEL.remove();
      });
  });
  // End Panel toolbox

  // Tooltip
  $(document).ready(function() {
      $('[data-toggle="tooltip"]').tooltip({
          container: 'body'
      });
  });
  // /Tooltip

  // iCheck
  if ($('input.flat')[0]) {
    $(document).ready(function() {
      $('input.flat').iCheck({
        checkboxClass: 'icheckbox_flat-green',
        radioClass: 'iradio_flat-green'
      });
      $('input.flat').on('ifChecked', function(event){
        if(this.value === "node_gateway"){
          $('.gateway_id').hide();
        }
        else {
          $('.gateway_id').show();
        }
      });
    });
  }

  // /iCheck

  // Validate creating and modifying user
  $('#form-new-user, #form-edit-user').each(function () {
    $(this).validate({
      rules: {
        username: {
          required: true
        },
        password: {
          required: true
        },
        email: {
          required: true
        }
      }
    });
  });

  // Validate creating and modifying device
  $('#form-new-device, #form-edit-device').each(function () {
    $(this).validate({
      rules:{
        node_name: {
          required: true
        },
        node_identification: {
          required: true
        },
        node_area: {
          required: true
        },
        node_gateway_id: {
          required: true
        }
      }
    });
  });

  // Date range picker configuration
  $(function() {

      var start = moment().subtract(29, 'days');
      var end = moment();

      function cb(start, end) {
          $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
      }

      $('#reportrange').daterangepicker({
          startDate: start,
          endDate: end,
          ranges: {
             'Today': [moment(), moment()],
             'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
             'Last 7 Days': [moment().subtract(6, 'days'), moment()],
             'Last 30 Days': [moment().subtract(29, 'days'), moment()],
             'This Month': [moment().startOf('month'), moment().endOf('month')],
             'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
          }
      }, cb);

      cb(start, end);

  });

  function init_daterangepicker_reservation() {

    if (typeof($.fn.daterangepicker) === 'undefined') {
        return;
    }
    // console.log('init_daterangepicker_reservation');

    $('#reservation').daterangepicker(null, function(start, end, label) {
        // console.log(start.toISOString(), end.toISOString(), label);
    });

    // $('#reservation').daterangepicker({
    //     timePicker: true,
    //     timePickerIncrement: 30,
    //     viewMode: "months",
    //     minViewMode: "months",
    //     locale: {
    //       // format: 'MM/DD/YYYY h:mm A'
    //       format: "mm-yyyy"
    //     }
    // });
  }

  init_sidebar();
  init_daterangepicker_reservation();

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

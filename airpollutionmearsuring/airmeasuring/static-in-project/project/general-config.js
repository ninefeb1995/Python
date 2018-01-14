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
});

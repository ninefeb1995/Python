$(function () {
  $('input').iCheck({
    checkboxClass: 'icheckbox_square-blue',
    radioClass: 'iradio_square-blue',
    // increaseArea: '20%' // optional
  });

  // DataTable global config
  $.extend(true, $.fn.dataTable.defaults, {
    searching: false,
    ordering: false,
    serverSide: true,
    processing: true,
    ajax: {
      dataSrc: 'results'
    }
  });
});
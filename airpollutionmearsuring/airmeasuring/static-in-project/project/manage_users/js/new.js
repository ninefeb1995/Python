$('#btn-new').on('click', function(){
  $('input[value="admin"]').attr('checked', true);
  $('input[value="admin"]').parents().addClass('checked');
  $('#modal-new').modal({
    backdrop: 'static',
    show: true
  });
});
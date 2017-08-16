$('#btn-edit-save').on('click', function (){
  $('#form-edit-user').submit();
  // $('#form-edit-user').submit(function (eventObj){
  //   //var type_of_user = $('.checked').find('input:first').val();
  //   //$(this).append(`<input type="hidden" name="type_of_user" value=`${type_of_user}`>`);
  //   return true;
  // });
});

$('#btn-new-save').on('click', function (){
  $('#form-new-user').submit();
});
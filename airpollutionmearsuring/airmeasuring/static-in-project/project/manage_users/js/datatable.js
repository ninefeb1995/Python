$(document).ready(function () {

  var table = $('#datatable').DataTable({
    ajax:{
      url: "/api/users/"
    },
    columns: [
      { title: 'Username', data: 'username'},
      { title: 'Full Name', data: 'fullname'},
      { title: 'Role', data: 'is_superuser', render: function (is_superuser) {
        if(is_superuser === true){
          return "Admin";
        }
        else {
          return "Staff";
        }
      }},
      { title: 'Last Activity', data: 'last_login', render: function (data) {
        var date = new Date(data);
        var month = date.getMonth() + 1;
        return date.getDate() + "/" + (month.length > 1 ? month : "0" + month) + "/" + date.getFullYear();
      }},
      { title: 'Action', data: '', render: function (id) {
        var html = `<a href="" class="btn btn-sm btn-flat bg-purple"><i class="fa fa-edit"></i> Edit</a>
                    <a href="#" class="btn btn-sm  btn-flat btn-danger"><i class="fa fa-trash"></i> Delete</a>
                    `;
        return html;
      }}
    ]
  });

  $('#datatable tbody').on('click', '.btn-danger', function(e){
    e.preventDefault();
    var data = table.row($(this).parents('tr')).data();
    $('#form-delete').attr('action', `/manage-users/users/${data.id}/`);
    $('#modal-delete').modal('show');
  });

  $('#datatable tbody').on('click', '.bg-purple', function(e){
    e.preventDefault();
    var data = table.row($(this).parents('tr')).data();
    $('[name="username"]').val(`${data.username}`);
    $('[name="password"]').val('passwordisnotchange');
    $('[name="first_name"]').val(`${data.first_name}`);
    $('[name="last_name"]').val(`${data.last_name}`);
    $('[name="email"]').val(`${data.email}`);
    if(`${data.is_superuser}` === 'true'){
      $('input[value="admin"]').attr('checked', true);
      $('input[value="admin"]').parents().addClass('checked');
      $('input[value="staff"]').removeAttr('checked');
      $('input[value="staff"]').parents().removeClass('checked');
    }
    else {
      $('input[value="admin"]').removeAttr('checked');
      $('input[value="admin"]').parents().removeClass('checked');
      $('input[value="staff"]').attr('checked', true);
      $('input[value="staff"]').parents().addClass('checked');
    }
    $('#form-edit-user').attr('action', `/manage-users/users/${data.id}/`);
    $('#modal-edit').modal({
      backdrop: 'static',
      show: true
    });
  });

  // Submit edit form
  // language=JQuery-CSS
  $('#btn-edit-save').on('click', function (){
    var edit_form = $('#form-edit-user');
    if(edit_form.valid()){
      edit_form.submit();
    }
    // $('#form-edit-user').submit(function (eventObj){
    //   //var type_of_user = $('.checked').find('input:first').val();
    //   //$(this).append(`<input type="hidden" name="type_of_user" value=`${type_of_user}`>`);
    //   return true;
    // });
  });

  // Submit save form
  // language=JQuery-CSS
  $('#btn-new-save').on('click', function (){
    var new_from = $('#form-new-user');
    if(new_from.valid()){
      new_from.submit();
    }
  });

  // On-click new button
  $('#btn-new').on('click', function(){
    $('[name="username"]').val("");
    $('[name="password"]').val("");
    $('[name="first_name"]').val("");
    $('[name="last_name"]').val("");
    $('[name="email"]').val("");
    $('input[value="admin"]').attr('checked', true);
    $('input[value="admin"]').parents().addClass('checked');
    $('input[value="staff"]').removeAttr('checked');
    $('input[value="staff"]').parents().removeClass('checked');
    $('#modal-new').modal({
      backdrop: 'static',
      show: true
    });
  });

});

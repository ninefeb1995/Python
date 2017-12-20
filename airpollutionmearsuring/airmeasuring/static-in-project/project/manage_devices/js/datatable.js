$(document).ready(function () {

  var table = $('#datatable').DataTable({
    ajax:{
      url: '/api/nodes/'
    },
    columns: [
      { title: 'ID', data: 'node_identification'},
      { title: 'Name', data: 'name'},
      { title: 'Area', data: 'area'},
      { title: 'Active', data: 'is_available', render: function (is_available) {
          if(is_available){
              return 'Yes';
          }
          else{
              return 'No';
          }
      }},
      { title: 'Action', data: 'is_available', render: function (is_available) {
          var button_list = ` <a href="" class="btn btn-sm btn-flat bg-purple"><i class="fa fa-edit"></i> Edit</a>
                              <a href="#" class="btn btn-sm  btn-flat btn-danger"><i class="fa fa-trash"></i> Delete</a>
                             `;
         if(is_available) {
              button_list += `<a href="#" class="btn btn-sm  btn-flat btn-warning"><i class="fa fa-lock"></i> Disconnect</a>`;
          }
          else {
              button_list += `<a href="#" class="btn btn-sm  btn-flat btn-warning"><i class="fa fa-lock"></i> Connect</a>`;
          }
        return button_list;
      }}
    ],
    initComplete: function(settings, json) {
      <!-- Loading nodes to google map when table loaded-->
      google.charts.load('current', {
        'packages': ['map'],
        'mapsApiKey': 'AIzaSyBqZkodGaG-lTwl1y2EiT4dFfk99FMSytQ'
      });
      google.charts.setOnLoadCallback(drawMap);
      function drawMap () {
        var nodes = [];
        nodes.push(['Lat', 'Long', 'Name', 'Marker']);
        table.rows().every(function (rowIdx, tableLoop, rowLoop) {
          var node = this.data(), // ... do something with data(), or this.node(), etc
              node_to_push = [parseFloat(`${node.latitude}`), parseFloat(`${node.longitude}`), `${node.name}`];
          if(node.role === 'node_gateway'){
            node_to_push.push('gateway');
          }
          else{
            node_to_push.push('node');
          }
          nodes.push(
            node_to_push
          );
        });
        var data = google.visualization.arrayToDataTable(nodes);
        var options = {
          mapType: 'styledMap',
          zoomLevel: 12,
          showTooltip: true,
          showInfoWindow: true,
          useMapTypeControl: true,
          enableScrollWheel: true,
          icons: {
            gateway: {
              normal: '/static/project/google_maps/img/gateway.png',
              selected: '/static/project/google_maps/img/gateway.png'
            },
            node: {
              normal: '/static/project/google_maps/img/node.png',
              selected: '/static/project/google_maps/img/node.png'
            }
          },
          maps: {
            // Your custom mapTypeId holding custom map styles.
            styledMap: {
              name: 'Devices', // This name will be displayed in the map type control.
              styles: [
                {featureType: 'poi.attraction',
                 stylers: [{color: '#fce8b2'}]
                },
                {featureType: 'road.highway',
                 stylers: [{hue: '#0277bd'}, {saturation: -50}]
                },
                {featureType: 'road.highway',
                 elementType: 'labels.icon',
                 stylers: [{hue: '#000'}, {saturation: 100}, {lightness: 50}]
                },
                {featureType: 'landscape',
                 stylers: [{hue: '#259b24'}, {saturation: 10}, {lightness: -22}]
                }
          ]}}
        };
        var map = new google.visualization.Map(document.getElementById('device-on-map'));
        map.draw(data, options);
      }
    }
  });

  $('#datatable tbody').on('click', '.btn-danger', function(e){
    e.preventDefault();
    var data = table.row($(this).parents('tr')).data();
    $('#form-delete').attr('action', `/manage-devices/devices/${data.id}/`);
    $('#modal-delete').modal('show');
  });

  $('#datatable tbody').on('click', '.bg-purple', function(e){
    e.preventDefault();
    var data = table.row($(this).parents('tr')).data();
    if (`${data.longitude}` !== '' && `${data.latitude}` !== '') {
      $('[name="node_location"]').val(`${data.latitude}` + ';' + `${data.longitude}`);
      $('.btn-connect').hide();
    }
    $('[name="node_name"]').val(`${data.name}`);
    $('[name="node_identification"]').val(`${data.node_identification}`);
    $('[name="node_area"]').val(`${data.area}`);
    $('[name="node_gateway_id"]').val("");
    if (`${data.role}` === 'node_gateway') {
      $('input[value="node_gateway"]').attr('checked', true);
      $('input[value="node_gateway"]').parents().addClass('checked');
      $('input[value="node_cell"]').removeAttr('checked');
      $('input[value="node_cell"]').parents().removeClass('checked');
      $('.gateway_id').hide();
    }
    else {
      $('input[value="node_gateway"]').removeAttr('checked');
      $('input[value="node_gateway"]').parents().removeClass('checked');
      $('input[value="node_cell"]').attr('checked', true);
      $('input[value="node_cell"]').parents().addClass('checked');
      $('[name="node_gateway_id"]').val(`${data.gateway_id}`);
      $('.gateway_id').show();
    }
    $('#form-edit-device').attr('action', `/manage-devices/devices/${data.id}/`);
    $('#modal-edit').modal({
      backdrop: 'static',
      show: true
    });
  });

  // Submit edit form
  // language=JQuery-CSS
  $('#btn-edit-save').on('click', function (){
    var edit_form = $('#form-edit-device');
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
    var new_from = $('#form-new-device');
    if(new_from.valid()){
      new_from.submit();
    }
  });

  // On-click new button
  $('#btn-new').on('click', function(){
    $('[name="node_name"]').val("");
    $('[name="node_identification"]').val("");
    $('[name="node_area"]').val("");
    $('[name="node_gateway_id"]').val("");
    $('input[value="node_gateway"]').attr('checked', true);
    $('input[value="node_gateway"]').parents().addClass('checked');
    $('input[value="node_cell"]').removeAttr('checked');
    $('input[value="node_cell"]').parents().removeClass('checked');
    $('.gateway_id').hide();
    $('#modal-new').modal({
      backdrop: 'static',
      show: true
    });
  });

  $('.loader').css('display', 'none');

  $('.btn-connect').on('click', function () {
    $('.loader').css('display', 'block');
  });

  // $.each(items, function (i, item) {
  //   $('#node_area').append($('<option>', {
  //     value: item.value,
  //     text: item.text
  //   }));
  // });


});

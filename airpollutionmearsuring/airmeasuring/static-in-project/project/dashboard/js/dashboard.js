$(document).ready(function () {

  // Handling on click event for area drop down list
  $('.area-dropdown-list li').on('click', function (event) {

    var element = $(this); // get element which causes the event

    var element_child = element.find('a'); // get child of element which causes the event

    var area = element.val(); // get area id to show data on chart

    $('#area-header').find('span').first().text(element_child.text()); // show what area-in-text has been chosen by this event
    $('#area-dropdown-list-activated').val(area); // concurrent, passing area_id to hidden-input inside <a> tag


    var date_range = $('#reportrange').data('daterangepicker'); // get date range from date range picker to show data
    var date_start = date_range.startDate;
    var date_end = date_range.endDate;

    renderChart(area, date_start, date_end); // Call function that handles render data on chart
  });

  // Handling on click event for date range picker
  var reportdate = $('#reportrange');
  reportdate.on('apply.daterangepicker', function (event, picker) {
      var date_start = picker.startDate;
      var date_end = picker.endDate;
      var area = $('#area-dropdown-list-activated').val();
      renderChart(area, date_start, date_end);
  });

  // Handle when first loaded
  window.onload = function() {
    var date_range = reportdate.data('daterangepicker'); // get date range from date range picker to show data
    var date_start = date_range.startDate;
    var date_end = date_range.endDate;
    var area = $('#area-dropdown-list-activated').val();
    renderChart(area, date_start, date_end);
  };

  // Function responsible for rendering the line chart
  function renderChart(area, start, end){
    $.ajax({
      url: '/dashboard/observation/',
      data: {
        area: area,
        date_start: start,
        date_end: end
      },
      contentType: "application/json; charset=utf-8",
      type: 'get',
      dataType: 'json',
      traditional: true,
      complete: function (xmlHttp, textStatus) {

        var data_objects = JSON.parse(xmlHttp.responseText);

        $('#device_count').text(data_objects.node_count);
        $('#active_device_count').text(data_objects.active_node_count);
        $('#gateway_count').text(data_objects.gateway_count);
        $('#area_count').text(data_objects.area_count);

        // Rendering html-divs for real-time charts
        var active_node = data_objects.active_node;
        for(var i = 0; i < data_objects.active_node_count; i++) {
          var name = active_node[i].name.replace(" ", "").toLowerCase(),
              id = "chart-container-" + name;
          $('.real_time').append(`<div id="${id}" style="width: 50%; float: left;"></div>`);
          render_realtime_chart(name, active_node[i].name, id, '100%', 0, null, null, null, active_node[i].name.replace(" ", "+"));
        }

        var co_data = [],
            nitrogen_data = [],
	          date_data = [];

        $.each(data_objects.data, function (index, item) {
          co_data.push(item.co);
	        nitrogen_data.push(item.nitrogen);
	        date_data.push(item.measuring_date);
        });
        var lineChart = $('#lineChart'),

        dataFirst = {
          label: "CO",
          data: co_data,
          backgroundColor: 'transparent',
          borderColor: 'rgba(98, 255, 244, 1)',
          pointBorderColor: 'rgba(98, 255, 244, 1)',
          pointRadius: 5,
          pointHoverRadius: 10,
          pointHitRadius: 20,
          pointBorderWidth: 2,
          pointStyle: 'rect'
        },

        dataSecond = {
          label: "NO2",
          data: nitrogen_data,
          backgroundColor: 'transparent',
          borderColor: 'rgba(151,187,205,1)',
          pointBorderColor: 'rgba(151,187,205,1)',
          pointRadius: 5,
          pointHoverRadius: 10,
          pointHitRadius: 20,
          pointBorderWidth: 2
        },

        datasets = {
          labels: date_data,
          datasets: [dataFirst, dataSecond]
        },

        chartOptions = {
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          }
        },

        showChart = new Chart(lineChart, {
          type: 'line',
          data: datasets,
          options: chartOptions
        });
      }
    });
  }

  //The `FusionCharts.register()` API is used to register the new theme in the FusionCharts core.
  function render_realtime_chart(id, name_chart, renderAt, width, height, chartConfig, data, trendLines, name_of_node) {
    FusionCharts.ready(function() {
    var fusioncharts = new FusionCharts({
      id: id.toString(),
      type: 'realtimeline',
      renderAt: renderAt.toString(),
      width: width.toString(),
      dataFormat: 'json',
      dataSource: {
      "dataStreamURL": `/dashboard/event-stream/${name_of_node}`,
      "chart": [{
              "caption": name_chart.toString(),
              "subCaption": "",
              "xAxisName": "Time",
              "yAxisName": "Value",
              "numberPrefix": "%",
              "refreshinterval": "2",
              "numdisplaysets": "20",
              "showValues": "0",
              "showRealTimeValue": "0",
              "theme": "fint",
      }],
      "dataset": [{
              "seriesname": "CO",
              "data": [{}]
          }, {
              "seriesname": "NO2",
              "data": [{}]
          }],
      "trendlines": null
      },
      events: {
        'beforeRender': function(evt, arg) {
          var controllers = document.createElement('div'),
              tableContid = 'tableCont-' + id.toString(),
              errorView = 'errorView' + id.toString();
          controllers.setAttribute('id', tableContid);
          controllers.innerHTML = `<div id=${errorView} style='width: 50%;border: 1px solid #ffbcbc;background-color:#f99898;  color:#ffffff;display:none;padding: 3px;margin-right: auto; margin-left: auto;text-align: center'></div>`;
          //Display container div and write table
          arg.container.append(controllers);
        },
        'realTimeUpdateError': function(event, parameter) {
          var dispBox = document.getElementById("errorView" + id.toString());
          dispBox.style.display = "block";
          dispBox.innerHTML = "Lost connection !!!";
        },
        'realtimeUpdateComplete': function(event, parameter) {
          var dispBox = document.getElementById("errorView" + id.toString());
          dispBox.style.display = "none";
        }
      }
    });
    fusioncharts.render();
    });
  }
});


document.getElementById('census-min').textContent = '0';
document.getElementById('census-max').textContent = '500';
var mapStyle = [{
  'stylers': [{'visibility': 'on'}]
}, {
  'featureType': 'landscape',
  'elementType': 'geometry',
  'stylers': [{'visibility': 'on'}, {'color': '#fcfcfc'}]
}, {
  'featureType': 'water',
  'elementType': 'geometry',
  'stylers': [{'visibility': 'on'}, {'color': '#bfd4ff'}]
}];
function initMap() {
  // Create the map.
  var map = new google.maps.Map(document.getElementById('visualization-on-map'), {
    zoom: 15,
    center: {lat: 10.867949500000002, lng: 106.8074915},
    styles: mapStyle
  });

  $.ajax({
    url: '/dashboard/aqionmap/',
    data: {
    },
    contentType: "application/json; charset=utf-8",
    type: 'get',
    dataType: 'json',
    traditional: true,
    complete: function (xmlHttp, textStatus) {
      if (textStatus === 'error') {
        return;
      }
      var data = JSON.parse(xmlHttp.responseText);
      $.each(data, function (index, value) {
        var aqi = value['aqi_value'],
            delta = aqi / 500,
            color = [],
            low = [151, 83, 34], // color of smallest datum
            high = [0, 92, 35];   // color of largest datum

        for (var i = 0; i < 3; i++) {
          // calculate an integer color based on the delta
          color[i] = (high[i] - low[i]) * delta + low[i];
        }

        var cityCircle = new google.maps.Circle({
          strokeColor: 'hsl(' + color[0] + ',' + color[1] + '%,' + color[2] + '%)',
          strokeOpacity: 0.8,
          strokeWeight: 0.001,
          fillColor: 'hsl(' + color[0] + ',' + color[1] + '%,' + color[2] + '%)',
          fillOpacity: 0.75,
          map: map,
          center: value['center'],
          radius: 1.6 * 100
        }),
        center = new google.maps.Marker({
          position: value['center'],
          map: map
        });

        google.maps.event.addListener(cityCircle, 'mouseover', function (e) {
          var percent = aqi / 500 * 100;
          document.getElementById('data-label').textContent = 'AQI';
          document.getElementById('data-value').textContent = aqi.toLocaleString();
          document.getElementById('data-box').style.display = 'block';
          document.getElementById('data-caret').style.display = 'block';
          document.getElementById('data-caret').style.paddingLeft = percent + '%';
        });
      });
  }
  });
}
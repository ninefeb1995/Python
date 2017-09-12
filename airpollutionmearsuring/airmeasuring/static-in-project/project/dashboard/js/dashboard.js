$(document).ready(function () {

  // Handling on click event for area drop down list
  $('.area-dropdown-list li').on('click', function (event) {

    var element = $(this); // get element which causes the event

    var element_child = element.find('a'); // get child of element which causes the event

    var area = element.val(); // get area id to show data on chart

    $('#area-header').find('span').first().text(element_child.text()); // show what area-in-text has been chosen by this event
    $('#area-dropdown-list-activated').val(area); // concurrent, passing area_id to hidden input inside <a> tag


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

  // Function been responsible for rendering the line chart
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
        $('#gateway_count').text(data_objects.gateway_count);
        $('#area_count').text(data_objects.area_count);

        var co_data = [];
        var oxi_data = [];
	      var date_data = [];

        $.each(data_objects.data, function (index, item) {
          co_data.push(item.co);
	        oxi_data.push(item.oxi);
	        date_data.push(item.measuring_date);
        });
        var lineChart = $('#lineChart');


        var dataFirst = {
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
        };

        var dataSecond = {
            label: "Oxi",
            data: oxi_data,
            backgroundColor: 'transparent',
            borderColor: 'rgba(151,187,205,1)',
            pointBorderColor: 'rgba(151,187,205,1)',
            pointRadius: 5,
            pointHoverRadius: 10,
            pointHitRadius: 20,
            pointBorderWidth: 2
          };

        var datasets = {
          labels: date_data,
          datasets: [dataFirst, dataSecond]
        };

        var chartOptions = {
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          }
        };

        var showChart = new Chart(lineChart, {
          type: 'line',
          data: datasets,
          options: chartOptions
        });
      }

    });
  }
});

//The `FusionCharts.register()` API is used to register the new theme in the FusionCharts core.
FusionCharts.ready(function() {
  var fusioncharts = new FusionCharts({
      id: "stockRealTimeChart",
      type: 'realtimeline',
      renderAt: 'chart-container',
      width: '1000',
      height: '600',
      dataFormat: 'json',
      dataSource: {
          "chart": {
              "caption": "Real time mearsuring data",
              "subCaption": "Application",
              "xAxisName": "Time",
              "yAxisName": "Value",
              "numberPrefix": "%",
              "refreshinterval": "2",
              "numdisplaysets": "50",
              "showValues": "0",
              "showRealTimeValue": "0",
              "theme": "fint"
          },
          "dataset": [{
              "data": [{}]
          }],
          "trendlines": [{
              "line": [{
                "startValue": "1",
                "endValue": "3",
                "color": "#ff8585",
                "displayValue": "Standard",
                "isTrendZone": "1",
                "valueOnRight": "1",
                "dashed": "1"
              }]
          }]
      },
      "events": {
          "initialized": function (e) {
              function updateData() {
                  // Get reference to the chart using its ID
                  var chartRef = FusionCharts("stockRealTimeChart"),
                      // Get random number
                      randomValue = Math.random(),
                      // Build Data String in format &label=...&value=...
                      strData = "&value=" + randomValue;
                  // Feed it to chart.
                  chartRef.feedData(strData);
              }

              e.sender.chartInterval = setInterval(function () {
                  updateData();
              }, 2000);
          },
          "disposed": function (evt, arg) {
              clearInterval(evt.sender.chartInterval);
          }
      }
  });
  fusioncharts.render();
});


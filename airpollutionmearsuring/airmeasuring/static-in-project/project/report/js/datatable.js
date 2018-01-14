$(document).ready(function (){

  $('#btn-show-report').on('click', function (event) {
    var area = $('#report-area-selection').val();
    if (area === 'select'){
      $('#modal-report-warning').modal({
        backdrop: 'true',
        show: true
      });
    }
    else {
      var date_range = $('#reservation').data('daterangepicker'); // get date range from date range picker to show data
      var date_start = date_range.startDate;
      var date_end = date_range.endDate;
      renderReport(area, date_start, date_end);
    }
  });

  $('#btn-report').on('click', function (event) {
    // $.ajax({
    //   url: '/report/download/',
    //   data: {},
    //   type: 'get',
    //   traditional: true,
    //   complete: function (xmlHttp, textStatus) {
    //   }
    // });

      // var source = $('.table-responsive').html(),
      //     pdf = new jsPDF('p', 'pt', 'letter'), // Use for creating report
      //     specialElementHandlers = {
      //   '#bypassme': function (element, renderer) {
      //   return true
      //   }
      // },
      // margins = {
      //   top: 80,
      //   bottom: 60,
      //   left: 40,
      //   width: 522
      // };
      // pdf.fromHTML(source, margins.left, margins.top, {
      //   'width': margins.width,
      //   'elementHandlers': specialElementHandlers
      // }, function (dispose) {
      //
      // }, margins);

      // var canvas = $('#report-barChart-1')[0];
      // var dataURL = canvas.toDataURL('image/jpeg', 1.0);
      // var pdf = new jsPDF('p', 'pt', 'letter');
      // pdf.addImage(dataURL, 'JPEG', 10, 10);
      // pdf.save('download.pdf');
    return xepOnline.Formatter.Format('report-container', {
      render:'download',
      pageWidth:'400',
      pageHeight:'300',
      filename: 'airquality'
      }
    );
  });

  // Function responsible for rendering report
  function renderReport(area, month_start, month_end) {
    $.ajax({
      url: '/report/showchart/',
      data: {
        area: area,
        month_start: month_start,
        month_end: month_end
      },
      contentType: "application/json; charset=utf-8",
      type: 'get',
      dataType: 'json',
      traditional: true,
      complete: function (xmlHttp, textStatus) {
        let data_objects = JSON.parse(xmlHttp.responseText),
          div_content = $('#report-container');
        if (div_content.children().length > 0){
          // $('#report-container > div:gt(0)').remove();
          $('#report-container > div').remove();
        }
        if (area === 'all'){
          $.each(data_objects.areas, function (index, item) {
            let area = item;
            $.each(data_objects.nodes[area.id], function (index, item) {
              let co_data = [],
                  nitrogen_data = [],
                  date = [],
                  name = area.name.toString() + "-" + item.name.toString();
              if (data_objects.data[area.id][item.id] !== null){
                let data = data_objects.data[area.id][item.id];
                $.each(data, function (index, item) {
                  co_data.push(item.co);
                  nitrogen_data.push(item.nitrogen);
                  date.push(item.measuring_date.toString());
                });
              }
              div_content.append(template(name, item.id, item.id));
              renderTable(`report-data-${item.id}`, date, co_data, nitrogen_data);
              renderBarChart(`report-barChart-${item.id}`, date, co_data, nitrogen_data);
            });
          });
        }
        else{
          $.each(data_objects.nodes, function (index, item) {
            let co_data = [],
                nitrogen_data = [],
                date = [],
                name = data_objects.area.name.toString() + "-" + item.name.toString();
            $.each(data_objects.data[item.id], function (index, item) {
              co_data.push(item.co);
              nitrogen_data.push(item.nitrogen);
              date.push(item.measuring_date.toString())
            });
            div_content.append(template(name, item.id, item.id));
            renderTable(`report-data-${item.id}`, date, co_data, nitrogen_data);
            renderBarChart(`report-barChart-${item.id}`, date, co_data, nitrogen_data);
          });
        }
        $('.my_float').css('display', 'block');
      }
    });
  }

  // Function responsible for rendering the bar chart
  function renderBarChart(renderAt, date, co, nitrogen){
    var ctx = document.getElementById(renderAt);
    var mybarChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: date,
        datasets: [{
          label: 'CO',
          backgroundColor: "#26B99A",
          data: co
        }, {
          label: 'Nitrogen Dioxide',
          backgroundColor: "#03586A",
          data: nitrogen
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
  }

  // Function responsible for rendering table
  function renderTable(table_id, date, co, nitrogen){
    var table = $(`.${table_id} tbody`),
        html = ``;
    $.each(date, function (index, item) {
      if (index % 2 === 0){
        html += `
                  <tr class="even pointer">
                    <td class="">${item}</td>
                    <td class="">${co[index]}</td>
                    <td class="">${nitrogen[index]}</td>
                  </tr>
                `;
      }
      else{
        html += `
                  <tr class="odd pointer">
                    <td class="">${item}</td>
                    <td class="">${co[index]}</td>
                    <td class="">${nitrogen[index]}</td>
                  </tr>
                `;
      }
    });
    table.append(html);
  }

  // Function containing html template
  function template(area_name, table_id, chart_id){
    return `
      <div class="well" style="overflow: auto; display: block">
        <div class="col-md-12">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_content">
                <p>${area_name}</p>
                <div class="table-responsive">
                  <table class="table table-striped jambo_table report-data-${table_id}">
                    <thead>
                      <tr class="headings">
                        <th class="column-title">Measurement Date </th>
                        <th class="column-title">Co </th>
                        <th class="column-title">Nitrogen Dioxide </th>
                      </tr>
                    </thead>
                    <tbody>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="x_content">
                <canvas id="report-barChart-${chart_id}" width="400" height="300"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

});



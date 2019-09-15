google.charts.load("current", {packages:["corechart","bar"]});
google.charts.setOnLoadCallback(loadData);


var candidateMap = new Map([
  ["Joe Biden", "(D) Joe Biden is a former Democratic vice president of the United States."],
    ["Andrew Yang", "(D) Andrew Yang is a Democratic candidate for president of the United States in 2020."],
  ["Elizabeth Warren", "(D) Elizabeth Warren is a Democratic member of the U.S. Senate from Massachusetts."],
  ["Amy Klobuchar", "(D) Amy Klobuchar is a Democratic member of the U.S. Senate from Minnesota."],
  ["Pete Buttigieg", "(D) Pete Buttigieg is the Democratic mayor of South Bend, Indiana."],
  ["Julian Castro", "(D) Julian Castro served as U.S. secretary of housing and urban development from 2014 to 2017."],
  ["Kamala Harris", "(D) Kamala Harris is a Democratic member of the U.S. Senate from California."],
  ["Cory Booker", "(D) Cory Booker is a Democratic member of the U.S. Senate from New Jersey."],
  ["Tom Steyer", "(D) Tom Steyer is an investor, activist, philanthropist, and donor to progressive and Democratic Party causes."],
  ["Beto O\'Rourke'", "(D) Robert \"Beto\" O\'Rourke is a former U.S. representative from Texas."],
  ["Donald Trump", "(R) Donald Trump is the 45th and current president of the United States."],
  ["Bernie Sanders", "(D) Bernie Sanders is an independent member of the U.S. Senate from Vermont who caucuses with the Democratic Party."]
]);
    
function drawChart(data, div_name) {
  var height = $(window).height() - 70;
  // $('#chartDiv').height(height);
  $('#' + div_name).height(height);

  var container = document.getElementById(div_name);
  var chart = new google.visualization.ColumnChart(container);
  var dataTable = new google.visualization.DataTable();

  // add listener on select event
  // google.visualization.events.addListener(chart, 'select', function () {
  //   var selection = chart.getSelection();
  //   var row = selection[0].row;
  //   alert("Selected " + dataTable.getValue(row, 0));
  //   window.location = "http://www.google.com";
  // });
  
  dataTable.addColumn({ type: 'string', id: 'Candidate' });
  dataTable.addColumn({ type: 'number', id: 'Positive', label:'Positive' });
  dataTable.addColumn({ type: 'string', role: 'tooltip', p: {html: true} });
  dataTable.addColumn({ type: 'number', id: 'Negative', label:'Negative' });
  dataTable.addColumn({ type: 'string', role: 'tooltip', p: {html: true} });
  console.log(data.length);
  // Create the data table with data
  if ( 1==1){

      for (const [candidate, value] of Object.entries(data)) {
       console.log(candidate, value);
       if (value[0] < 0) value[0] *= -1;
       if (value[1] > 0) value[1] *= -1;

     dataTable.addRow( [candidate, value[0], createHtmlTooltip(candidate, value[0], value[1]), value[1], createHtmlTooltip(candidate, value[0], value[1]) ]);

      }
      var news_id = "news1"; 
      if (div_name == "chartDiv2") {
        news_id = "news2";
      }
      var options = {
        title: $('#' + news_id).val(),
        isStacked: true,
          tooltip: {isHtml: true }, /* use HTML tooltip */
          colors: ['#59cf8a','#ff5959'],
        hAxis: { title: 'Candidate'},
        vAxis: { title: 'Bias'},
        chartArea:{left:100,top:20,width:"67%",height:"67%"}

      };
      chart.draw(dataTable, options);
  }else{
        container.innerHTML = "No data found.";
  }
}

function drawChart2(data) {
 var height = $(window).height() - 50;
 $('#chartDiv2').height(height);

  var container = document.getElementById('chartDiv2');
  var chart = new google.visualization.ColumnChart(container);
  var dataTable = new google.visualization.DataTable();

  
  dataTable.addColumn({ type: 'string', id: 'Candidate' });
  dataTable.addColumn({ type: 'number', id: 'Positive', label:'Positive' });
  dataTable.addColumn({ type: 'string', role: 'tooltip', p: {html: true} });
  dataTable.addColumn({ type: 'number', id: 'Negative', label:'Negative' });
  dataTable.addColumn({ type: 'string', role: 'tooltip', p: {html: true} });

  // Create the data table with data
  if ( data.length > 0 ){
      $.each(data, function(candidate, scores){
        dataTable.addRow( [candidate, scores[0], createHtmlTooltip(candidate), value.bad, createHtmlTooltip(scores[1]) ]);
      });

      var options = {
        title: $('#news2').val(),
        isStacked: true,
    tooltip: {isHtml: true }, /* use HTML tooltip */
        colors: ['#59cf8a','#ff5959'],
        hAxis: { title: 'Candidate'},
        vAxis: { title: 'Bias'}
      };
      chart.draw(dataTable, options);
  }else{
        container.innerHTML = "No data found.";
  }
}

function createHtmlTooltip(candidate, good, bad) {
  c_name = candidate.replace(" ", "_");
  var img_path = "../static/images/" + c_name + ".jpg";
  var description= candidateMap.get(candidate);
  if (candidate.includes("Beto")) {
    description = "(D) Robert \"Beto\" O\'Rourke is a former U.S. representative from Texas.";
  }
  var html = '<div class="popup"><img src="' + img_path +  '" width="42" height="42">'
     + '<b>' + candidate + '</b><hr>'
     + description
     + '<br><b>Positive: </b>' + Math.round(good * 100) / 100 
     + '<br><b>Negative: </b>' + Math.round(bad * 100) / 100 
     + '<br></div>';
  return html;
}

function loadData(){
  $("#errorMsg").hide();
  let startDate = $("#startDate").datepicker({dateFormat: 'yy-mm-dd'}).val();
  let endDate = $("#endDate").datepicker({dateFormat: 'yy-mm-dd'}).val();
  // if(startDate == 0 || endDate == 0) {
  //     $("#errorMsg").show();
  //     return
  // }

  $("#spinner").show();
fetch("/news/" + $("#news1").val(), {method: 'GET'})
.then(data => data.json())
.then(resp => {
  drawChart(resp, "chartDiv");
  $("#spinner").hide();

});

$("#spinner").show();
fetch("/news/" + $("#news2").val(), {method: 'GET'})
.then(data => data.json())
.then(resp => {
  drawChart(resp, "chartDiv2");
  $("#spinner").hide();

});



$(document).ready( function(){
   // jQuery datepicker
   $(".datepicker").datepicker({
     dateFormat : 'yy-mm-dd',
     minDate : 0
   });

});


}


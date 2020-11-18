function unpackData (arr, key) {
  return arr.map(obj => obj[key]);
}
var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

window.onload = function() {

  var data=JSON.parse(httpGet(location.origin+"/data"));
  console.log(data);
  gatto=unpackData(data, 'Temperature');
  console.log(unpackData(data, 'Temperature'));
  
  var ctx = document.getElementById('canvas').getContext('2d');
  //window.myLine = new Chart(ctx, config);
  var config = {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: "My First dataset",
        backgroundColor: chartColors.red,
        borderColor: chartColors.red,
        data:gatto,
        fill: false,
      }, {
        label: "My Second dataset",
        fill: false,
        backgroundColor: chartColors.blue,
        borderColor: chartColors.blue,
        data: gatto,
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: 'Chart.js Line Chart'
      },
      tooltips: {
        mode: 'label',
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        xAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Month'
          }
        }],
        yAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Value'
          }
        }]
      }
    }
  };
  
  
  var ctx = document.getElementById("canvas").getContext("2d");
  window.myLine = new Chart(ctx, config);
  
}


function httpGet(theUrl){
var xmlHttp = new XMLHttpRequest();

xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
xmlHttp.setRequestHeader('sensor', 'Thermo');
xmlHttp.setRequestHeader('data', 'Temperature');
xmlHttp.setRequestHeader('time', 2);
xmlHttp.setRequestHeader('units', 'w');
xmlHttp.send( null );
return xmlHttp.responseText;
}

var config = {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
      label: 'My First dataset',
      backgroundColor: window.chartColors.red,
      borderColor: window.chartColors.red,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
      fill: false,
    }, {
      label: 'My Second dataset',
      fill: false,
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
      ],
    },{
      label: 'My Second dataset',
      fill: false,
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: JSON.parse(httpGet(location.origin+"/data")).Temperature
    }]
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Chart.js Line Chart'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Month'
        }
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Value'
        }
      }
    }
  }
};


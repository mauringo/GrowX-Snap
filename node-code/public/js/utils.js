function unpackData (arr, key) {
  return arr.map(obj => obj[key]);
}



function loadGraph(graph,color,title,range,sensor, dataq,time,units) {

  var data=JSON.parse(httpGet(location.origin+"/data",sensor, dataq,time,units));
  console.log(data);

  console.log(unpackData(data, dataq));
  
 
  var firstTrace = {
    type: 'scatter',
    mode: 'lines',
    name: 'Mean User Usage',
    borderWidth: 0,
    x: unpackData(data, 'time'),
    y: unpackData(data, dataq),
    line: {color: color,
           shape: 'spline', 
           smoothing: 0.2,
           width: 4}
  }
  
  var datag = [firstTrace];
  var config = {
    responsive: true,
    displaylogo: false,
    displayModeBar: false,
    editable: false,
    dragMode:false,
    scrollZoom:false
    }
  var layout = {
    title: title,
    yaxis: {
      autorange: true,
      boundmode: 'soft',
      bounds: range}
  };

  return Plotly.newPlot(graph, datag, layout, config);
  //window.myLine = new Chart(ctx, config);
  
  
}


function httpGet(theUrl, sensor, data,time,units){
var xmlHttp = new XMLHttpRequest();

xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
xmlHttp.setRequestHeader('sensor', sensor);
xmlHttp.setRequestHeader('data', data);
xmlHttp.setRequestHeader('time', time);
xmlHttp.setRequestHeader('units', units);
xmlHttp.send( null );
return xmlHttp.responseText;
}

function HTTPgetBattery(theUrl, sensor){
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
  xmlHttp.setRequestHeader('sensor', sensor);
  xmlHttp.send( null );
  return xmlHttp.responseText;
  }



var graph1='humidity';
var color1='#17BECF';
var sensor1='Thermo';
var data1='Humidity';
var range1=[0, 100];
var time1=1;
var units1='d';
var title1='Humidity %';

var graph2='temperature';
var color2='#de1c22';
var sensor2='Thermo';
var data2='Temperature';
var range2=[0, 40];
var time2=1;
var units2='d';
var title2='Temperature ºC';

function setTime(time, units){
    time2=time;
    time1=time;
    units1=units;
    units2=units;
    loadMyGraph();
}
function GetBattery(){
    
    document.getElementById('batteryindicator').innerHTML=("Device Battery Left: "+JSON.parse(HTTPgetBattery(location.origin+"/battery",sensor1))[0].last +"%");
}
function loadMyGraph(){
    
    loadGraph(graph1,color1,title1,range1,sensor1, data1,time1,units1);
    loadGraph(graph2,color2,title2,range2,sensor2, data2,time2,units2);
    GetBattery();
}



window.onload = function(){
loadMyGraph();
}

setInterval(function() {
    
    loadMyGraph();
    GetBattery();

}, 30000);
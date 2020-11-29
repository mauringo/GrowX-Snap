var sensor1='FloraPlant4';
var time1=1;
var units1='d';



var graph1='moisture';
var color1='#17BECF';
var data1='Moisture';
var range1=[0, 100];
var title1='Moisture %';

var graph2='temperature';
var color2='#de1c22';
var data2='Temperature';
var range2=[0, 40];
var title2='Temperature ºC';

var graph3='conductivity';
var color3='#8b4513';
var data3='Conductivity';
var range3=[0, 40];
var title3='Conductivity µS/cm';

var graph4='light';
var color4='#ffbf00';
var data4='Light';
var range4=[0, 40];
var title4='Light lux';

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
    loadGraph(graph2,color2,title2,range2,sensor1, data2,time1,units1);
    loadGraph(graph3,color3,title3,range3,sensor1, data3,time1,units1);
    loadGraph(graph4,color4,title4,range4,sensor1, data4,time1,units1);
  
    GetBattery();
}



window.onload = function(){
    checkLicense();
    loadMyGraph();
    }

setInterval(function() {
    
    loadMyGraph();
    GetBattery();

}, 30000);
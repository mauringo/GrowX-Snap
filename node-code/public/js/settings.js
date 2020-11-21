function updateStatus() {

  fetch(location.origin+'/info', {
    method: 'GET', // or 'PUT'
    })
    .then(response => response.json())
    .then(data => {
      //console.log('Success:', data);
      document.getElementById("pollingcheck").checked = !data.pairing;
      document.getElementById("scanningcehck").checked = data.pairing;
      if (!data.pairing){
        document.getElementById("message").value = '';
      }
      document.getElementById("sensorspresent").innerText = "Devices Synchronized: "+((data.thermos).length.toString())+ " thermometers and the following plants: " + (data.plants);
      $('#plant1c').prop('disabled',data.plants.includes("Plant1"));
      $('#plant2c').prop('disabled',data.plants.includes("Plant2"));
      $('#plant3c').prop('disabled',data.plants.includes("Plant3"));
      $('#plant4c').prop('disabled',data.plants.includes("Plant4"));
      
      $('#plant1d').prop('disabled',!data.plants.includes("Plant1"));
      $('#plant2d').prop('disabled',!data.plants.includes("Plant2"));
      $('#plant3d').prop('disabled',!data.plants.includes("Plant3"));
      $('#plant4d').prop('disabled',!data.plants.includes("Plant4"));

      $('#thermoc').prop('disabled',(data.thermos).length >0);
      $('#thermod').prop('disabled',!(data.thermos).length >0);

      
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

window.onload = function() {
  

  console.log(updateStatus());

  
}

setInterval(function() {
  updateStatus();
  
}, 1000);


function pairThermo() {

  fetch(location.origin+'/pairthermo', {
    method: 'GET', // or 'PUT'
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      document.getElementById("message").value = data.status;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function pairflora(floraname) {
  var mydata=floraname;
  console.log(floraname);
  fetch(location.origin+'/pairflora', {
    method: 'POST', // or 'PUT'
  
    body: mydata,
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      document.getElementById("message").value = data.status;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


function removeall() {

  fetch(location.origin+'/remall', {
    method: 'GET', // or 'PUT'
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function remone(sensor){
  const data = { sensor: sensor };

  fetch(location.origin+'/remone', {
    method: 'POST', // or 'PUT'
    
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}
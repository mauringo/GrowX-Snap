

var licensed=[]

function checkLicense(){

  fetch(location.origin+'/licensed', {
    method: 'GET', // or 'PUT'
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    licenseModal(data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });    
  
 
}

function license(){

 fetch(location.origin+'/licensed', {
    method: 'POST', // or 'PUT'
  })
  .catch((error) => {
    console.error('Error:', error);
  });    
  
 
}

function licenseModal(data){
  console.log("licensing")
  console.log(data);
  if (data.unlicensed){
    $('#cookieModal').modal('show');
  }
  
}



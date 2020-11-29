var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

const Influx = require('influx');

const os = require('os');
const bodyParser = require('body-parser');
const { Console } = require('console');
const { strict } = require('assert');
const { stringify } = require('querystring');
const http = require('http');
const fs = require('fs')


//const filepath = 'unlicensed' //for developing

const filepath = process.env.SNAP_DATA+'/'+'unlicensed'; //production envirnoment

const influx = new Influx.InfluxDB('http://127.0.0.1:23233/room1');
var app = express();

console.log(filepath);

const port = 23232;

app.use(bodyParser.json());
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  next();
});





influx.getMeasurements()
  .then(names => console.log('My measurement names are: ' + names.join(', ')))
  
  .catch(error => console.log({ error }));



function checkFilePresence(myfile) {
  console.log("checking Licensing");
  try {
    if(fs.existsSync(myfile)) {
        return true;

    } else {
        return false;
    }
    } catch (err) {
        console.error(err);
        return false;
    }
}

function buildQuery(a) {
 
  return `select ` + String(a.data)+ ` from ` +String(a.sensor)+` where time > now() - `+String(a.time)+ String(a.units);
}

function buildQueryBattery(a) {
 
  return `select last("Battery") from ` + String(a.sensor);
}

app.get('/licensed', (request, response) => {
  
  a=checkFilePresence(filepath);

  response.status(200).json({ unlicensed: a });
  
 
});

app.post('/licensed', (request, response) => {
  
  fs.unlinkSync(filepath);

  response.status(200).json({ done: true });
  
  
});

app.get('/data', (request, response) => {
  var a=request.headers;

  influx.query(buildQuery(a))

    .then(result => response.status(200).json(result))
    .catch(error => response.status(500).json({ error }));
});

app.get('/battery', (request, response) => {
  var a=request.headers;

  influx.query(buildQueryBattery(a))

    .then(result => response.status(200).json(result))
    .catch(error => response.status(500).json({ error }));
});


app.get("/info", (client_req, client_res)=>{
  console.log('serve: ' + client_req.url);

  var options = {
    hostname: 'localhost',
    port: 23231,
    path: client_req.url,
    method: client_req.method,
    headers: client_req.headers
  };

  var proxy = http.request(options, function (res) {
    client_res.writeHead(res.statusCode, res.headers)
    res.pipe(client_res, {
      end: true
    });
  });

  client_req.pipe(proxy, {
    end: true
  });
});

  
app.get("/pairthermo", (client_req, client_res)=>{
  console.log('serve: ' + client_req.url);

  var options = {
    hostname: 'localhost',
    port: 23231,
    path: client_req.url,
    method: client_req.method,
    headers: client_req.headers
  };

  var proxy = http.request(options, function (res) {
    client_res.writeHead(res.statusCode, res.headers)
    res.pipe(client_res, {
      end: true
    });
  });

  client_req.pipe(proxy, {
    end: true
  });
});


  
app.post("/pairflora", (client_req, client_res)=>{
  console.log('serve: ' + client_req.url);

  var options = {
    hostname: 'localhost',
    port: 23231,
    path: client_req.url,
    method: client_req.method,
    headers: client_req.headers
  };

  var proxy = http.request(options, function (res) {
    client_res.writeHead(res.statusCode, res.headers)
    res.pipe(client_res, {
      end: true
    });
  });

  client_req.pipe(proxy, {
    end: true
  });
});
  
app.get("/remall", (client_req, client_res)=>{
  console.log('serve: ' + client_req.url);

  var options = {
    hostname: 'localhost',
    port: 23231,
    path: client_req.url,
    method: client_req.method,
    headers: client_req.headers
  };

  var proxy = http.request(options, function (res) {
    client_res.writeHead(res.statusCode, res.headers)
    res.pipe(client_res, {
      end: true
    });
  });

  client_req.pipe(proxy, {
    end: true
  });
});

app.post("/remone", (client_req, client_res)=>{
  console.log('serve: ' + client_req.url);

  var options = {
    hostname: 'localhost',
    port: 23231,
    path: client_req.url,
    method: client_req.method,
    headers: client_req.headers
  };

  var proxy = http.request(options, function (res) {
    client_res.writeHead(res.statusCode, res.headers)
    res.pipe(client_res, {
      end: true
    });
  });

  client_req.pipe(proxy, {
    end: true
  });
});

app.post("/addone", (client_req, client_res)=>{
  console.log('serve: ' + client_req.url);

  var options = {
    hostname: 'localhost',
    port: 23231,
    path: client_req.url,
    method: client_req.method,
    headers: client_req.headers
  };

  var proxy = http.request(options, function (res) {
    client_res.writeHead(res.statusCode, res.headers)
    res.pipe(client_res, {
      end: true
    });
  });

  client_req.pipe(proxy, {
    end: true
  });
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

app.listen(port, () => console.log(`Hello world app listening on port ${port}!`))

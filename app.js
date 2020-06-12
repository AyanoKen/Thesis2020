require("dotenv").config();
const express = require('express');
const bodyParser = require("body-parser");
var spawn = require("child_process").spawn;

const app = express();

app.use(express.static("public"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended: true}));

const key = process.env.KEY;

app.get("/", function(req, res){
  res.render("form");
});

app.post("/findRoute", function(req, res){
  const start = req.body.startpos;
  const end = req.body.endpos;
  var distance;
  var time;

  const pythonProcess = spawn("python", ["./pythonFiles/distanceTimeCal.py", start, end, key]);
  pythonProcess.stdout.on("data", function(data){
    mystr = data.toString();
    myjson = JSON.parse(mystr);

    console.log(myjson.distance);
    console.log(myjson.time);

    distance = (myjson.distance/1000).toFixed(2);
    time = (myjson.time/60).toFixed(2);

    res.render("map", {key: key, start: start, end: end, distance:distance, time:time});
  });


});

app.post("/map", function(req, res){
  res.render("choosePointsMap", {key: key});
});

app.post("/services", function(req, res){
  const center = req.body.center;
  const radius = req.body.radius;
  const service = req.body.service;

  const pythonProcess2 = spawn("python", ["./pythonFiles/servicesNearby.py", center, radius, service, key]);
  pythonProcess2.stdout.on("data", function(data){
    mystr = data.toString();
    myjson = JSON.parse(mystr);

    let coordinates = myjson.coordinates;

    res.render("servicesMap", {key: key, results: coordinates});
  });
})

var port = process.env.PORT;
if (port == null || port == "") {
  port = 3000;
}

app.listen(port, function(){
  console.log("Server is up and running");
})

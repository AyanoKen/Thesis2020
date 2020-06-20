require("dotenv").config();
const express = require('express');
const bodyParser = require("body-parser");
const spawn = require("child_process").spawn;
const mongoose = require("mongoose");

const app = express();

app.use(express.static(__dirname + "/public"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended: true}));

mongoose.connect("mongodb+srv://admin-kireet:"+process.env.PASSWORD+"@tsunduko-hlubr.mongodb.net/Thesis2020DB", {useNewUrlParser: true, useUnifiedTopology: true});

const coordinateSchema = {
  name: String,
  points: [String]
};

const Coordinate = mongoose.model("Coordinate", coordinateSchema);

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

  const pythonProcess2 = spawn("python", ["./pythonFiles/servicesNearby3.py", center, radius, service, key]);
  pythonProcess2.stdout.on("data", function(data){
    mystr = data.toString();
    myjson = JSON.parse(mystr);

    let coordinates = myjson.coordinates;

    res.render("servicesMap", {key: key, results: coordinates, addresses: myjson.addresses});
  });
});

app.get("/services/:center&:radius&:service", function(req, res){
  const center = req.params.center;
  const radius = req.params.radius;
  const service = req.params.service;

  const pythonProcess2 = spawn("python", ["./pythonFiles/servicesNearby2.py", center, radius, service, key]);
  pythonProcess2.stdout.on("data", function(data){
    mystr = data.toString();
    myjson = JSON.parse(mystr);

    let i = 0;
    let responseData = [];

    let coordinates = myjson.coordinates;

    coordinates = coordinates.split(";");

    myjson.addresses.forEach(function(address){
      let temp = {
        location: coordinates[i].split(",").reverse(),
        address: address
      }

      responseData.push(temp);
    });

    res.send(responseData);
  });
});

app.post("/savePoints", function(req, res){
  const points = (req.body.points).split(";");

  points.pop();

  const newPoints = new Coordinate({
    name: req.body.title,
    points: points
  });

  newPoints.save(function(err){
    if(!err){
      res.redirect("/");
    }else{
      console.log(err);
    }
  });
});

app.post("/showPoints", function(req, res){
  Coordinate.find({}, function(err, results){
    if(!err){
      let data = [];
      results.forEach(function(result){
        let temp = {
          name: result.name,
          points: result.points
        };

        data.push(temp);
      });
      res.send(data);
    }
  });
});

app.post("/liveLocation", function(req, res){
  res.render("liveLocation", {key: key});
});

app.get("/speak", function(req, res){
  const pythonProcess2 = spawn("python", ["./pythonFiles/SpeechRecognition.py"]);
  pythonProcess2.stdout.on("data", function(data){
    mystr = data.toString();
    myjson = JSON.parse(mystr);

    let text = myjson.text;

    res.send(text)
  });
})

app.post("/getReviews", function(req, res){
  let speech = req.body.speech;

  console.log(speech)

  const pythonProcess2 = spawn("python", ["./pythonFiles/techReviews.py", speech]);
  pythonProcess2.stdout.on("data", function(data){
    mystr = data.toString();
    myjson = JSON.parse(mystr);

    if(myjson.Response == 200){
      res.send(myjson.articles);
    }else{
      res.send("Invalid Command, Try Again");
    }
  });
});

var port = process.env.PORT;
if (port == null || port == "") {
  port = 3000;
}

app.listen(port, function(){
  console.log("Server is up and running");
})

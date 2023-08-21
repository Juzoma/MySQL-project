// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');
const { response } = require('express');

var selectedID = "";
app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// welcome page 
app.get('/', function(req, res) {
    
    var tagline = "Welcome to my UI project";

    res.render('pages/index', {
        tagline: tagline
    });
});


// view page
app.get('/about', function(req, res) {

var vacation = "Lets take a look at your already planned vacations";

    axios.get('http://127.0.0.1:5000/trip/all')
    .then((response)=> {
        var tripdata = response.data
        console.log("trip data we got ", tripdata);
     res.render('pages/about', {
        trip: tripdata, 
    });
    });
    
});


//create destination page
app.get('/createDes', function(req, res) {
    var example = "Create a destination";

        axios.get('http://127.0.0.1:5000/destination/all')
        .then((response)=> {
            var desData = response.data
            console.log("destination data we got ", desData);
        res.render('pages/createDes', {
            des: desData, 
        });
    });
    
    });

app.post('/processdynamicform', function(req, res) {
    added = "Destination was added successfully"

    var id = req.body.id
    var country = req.body.country
    var city = req.body.city
    var sightseeing = req.body.sightseeing
    console.log("country city...", id, country, city, sightseeing)

    axios.post('http://127.0.0.1:5000/destination', {
            id: id,
            country:country,
            city:city,
            sightseeing:sightseeing
        }) 
    .then((response) => {
        added = "Destination was added successfully"
    console.log("Insert successful!");
    })

    res.render("pages/createDes", {
        added: added
    })

})


//create trip page
app.get('/createTrip', function(req, res) {

    axios.get('http://127.0.0.1:5000/trip/all')
    .then((response)=> {
        var tripData = response.data
        console.log("destination data we got ",tripData);
    res.render('pages/createTrip', {
        trip: tripData, 
    });
});

});

app.post('/processform', function(req, res) {
    added = "Trip was added successfully"
    var destination_id = req.body.destination_id
    var transportation = req.body.transportation
    var startdate = req.body.startdate
    var enddate = req.body.enddate
    var tripname = req.body.tripname
    console.log("des_id transportation...", destination_id, transportation, startdate, enddate, tripname)

    axios.post('http://127.0.0.1:5000/trip', {
            destination_id:destination_id,
            transportation:transportation,
            startdate:startdate,
            enddate:enddate,
            tripname:tripname
        })
    .then((response) => {
        added = "Trip was added successfully"
        console.log("Insert successful!");
        })
    
    res.render("pages/createTrip", {
        added: added
    })   
})

// edit destination page 
app.get('/editDes', function(req, res) {
var exampleVar = "Edit a destination";

// this will render our new example page 
res.render("pages/editDes.ejs", {exampleVar: exampleVar});
});

app.post('/process_form', function(req, res){
    updated = "Destination was updated Successfully"

    var id = req.body.id
    var country = req.body.country
    var city = req.body.city
    var sightseeing = req.body.sightseeing
    console.log("country city..", country, city, id, sightseeing)


console.log('http://127.0.0.1:5000/destination?id='+ id)
    axios.put('http://127.0.0.1:5000/destination?id='+ id, {
        
            country:country,
            city:city,
            sightseeing:sightseeing
        })
    .then((response) => {
        updated = "Destination was updated Successfully"
        
    console.log("update successful!");
    


    })

    res.render('pages/editDes', {
        updated: updated
     });

    
});


// edit trip page 
app.get('/editTrip', function(req, res) {
    axios.get('http://127.0.0.1:5000/trip/all')
    .then((response)=> {
        var tripData = response.data
        console.log("destination data we got ",tripData);
    res.render('pages/editTrip', {
        trip: tripData, 
    });
});

});

app.post('/process_tripform', function(req, res){
    updated = "Trip was updated Successfully"

    var id = req.body.id
    var destination_id = req.body.destination_id
    var transportation = req.body.transportation
    var startdate = req.body.startdate
    var enddate = req.body.enddate
    var tripname = req.body.tripname
    console.log("des_id transportation..", destination_id, transportation, startdate, enddate, tripname)


console.log('http://127.0.0.1:5000/trip?id='+ id)
    axios.put('http://127.0.0.1:5000/trip?id='+ id, {
        
            destination_id: destination_id,
            transportation: transportation,
            startdate: startdate,
            enddate: enddate,
            tripname: tripname
        })
    .then((response) => {
        updated = "Trip was updated Successfully"
        
    console.log("update successful!");
    
    })

    res.render('pages/editTrip', {
        updated: updated
     });

    
});

app.listen(8070);
console.log('8070 is the magic port');
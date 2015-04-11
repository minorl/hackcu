var express = require('express');
var app = express();

//Set up net server for communication between web server and game server
var net = require('net');

var gameServer = net.createServer(function(conn) {
    console.log("Server: Client connected");

    // If connection is closed
    conn.on("end", function() {
        console.log('Server: Client disconnected');
        // Close the server
        server.close();
        // End the process
        process.exit(0);
    });

    // Handle data from client
    conn.on("data", function(data) {
        data = JSON.parse(data);
        console.log("Response from client: %s", data);
    });

    // Let's response with a hello message
    conn.write(
        JSON.stringify(
            { response: "Hey there client!" }
        )
    );
});

// Listen for connections
gameServer.listen(31337, "localhost", function () {
    console.log("Server: Listening");
});

var _ = require('lodash');

var Eureca = require('eureca.io');

var eurecaServer = new Eureca.Server();

app.use(express.static(__dirname + '/public'));

app.use('/bootstrap', express.static(__dirname + '/node_modules/bootstrap/dist/'));

app.get('/', function(req, res) {
    res.render('index.html');
});

app.set('port', (process.env.PORT || 3000));

var server = app.listen(app.get('port'), function() {

    var host = server.address().address;
    var port = server.address().port;
    console.log('App listening at http://%s:%s', host, port);
});

//attache eureca.io to http server
eurecaServer.attach(server);

//detect client connection
eurecaServer.onConnect(function (conn) {
    console.log('New client id=%s', conn.id, conn.remoteAddress);
});

eurecaServer.exports.hello = function () {
    console.log('Hello from client');
}

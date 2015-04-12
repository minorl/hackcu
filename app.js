var express = require('express');
var app = express();

//Set up net server for communication between web server and game server
var net = require('net');

var initial_board;
var current_state;
var writeAck;
var gameServer = net.createServer(function(conn) {
    console.log("Server: Client connected");

    // If connection is closed
    conn.on("end", function() {
        console.log('Server: Client disconnected');
        // Close the server
    });

    // Handle data from client
    conn.on("data", function(data) {
        data = JSON.parse(data);
        if (initial_board == null) {
            initial_board = data;
            for (var c in clients) {
                var remote = clients[c].remote;
                remote.initBoard(data);
            }
        } else {
            for (var c in clients) {
                var remote = clients[c].remote;
                current_state = data;
                remote.redraw(data);
            }
        }
        writeAck();
    });

    // Let's response with a hello message
//    conn.write(
//        JSON.stringify(
//            { response: "Hey there client!" }
//        )
//    );
});


var gameServer2 = net.createServer(function(conn2) {

    writeAck = function() {
        conn2.write("ack");
    }
});
// Listen for connections
gameServer.listen(31337, "localhost", function () {
    console.log("Server: Listening");
});

gameServer2.listen(31338, "localhost", function() {
    console.log("GameServer2: Listening");
});
var _ = require('lodash');

var Eureca = require('eureca.io');
var clients = {};

var eurecaServer = new Eureca.Server({ allow: ['setId', 'redraw', 'initBoard']});

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

    // The getClient method provide a proxy allowing us to call remote client functions
    var remote = eurecaServer.getClient(conn.id);

    // Register the client
    clients[conn.id] = { id: conn.id, remote: remote };

    remote.setId(conn.id);
    if (initial_board != null) {
        remote.initBoard(initial_board);
    }
    if (current_state != null) {
        remote.redraw(current_state);
    }
    console.log(clients);
});

eurecaServer.exports.tryMove = function (move) {
    console.log(move);
}

eurecaServer.onDisconnect(function (conn) {
    console.log('Client disconnected ', conn.id);
});

eurecaServer.exports.hello = function () {
    console.log('Hello from client');
}

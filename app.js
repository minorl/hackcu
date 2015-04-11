var express = require('express');
var app = express();

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

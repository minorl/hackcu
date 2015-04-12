
var ready = false;
var eurecaServer;

var myId = -1;

var eurecaClientSetup = function () {
    var eurecaClient = new Eureca.Client();

    eurecaClient.ready(function (proxy) {
        eurecaServer = proxy;
    });

    eurecaClient.exports.setId = function(id) {
        myId = id;
        create();
        console.log(myId);
        ready = true;
    }
}

var game = new Phaser.Game(1400, 1200, Phaser.AUTO, 'game-container', { preload: preload, create: eurecaClientSetup, update: update, render: render});

var bmd;
var x_dist = 240;
var y_dist = 210;
var x_offset = 120;
var total_x_offset = 25;
var total_y_offset = 25;

// Variable to store the action after having clicked on an action button
// -1 => no action, 0 => build road, 1 => build settlement, 2 => build city
var action = -1;

// Group for tiles
var tileLayer;

// Group for corners
var cornerLayer;

// Group for pieces
var pieceLayer;

var sprites = ['ore', 'wheat', 'desert', 'water', 'wood', 'brick', 'sheep'];
var pieces = ['settlement_blue', 'settlement_green', 'settlement_orange', 'settlement_red',
              'city_blue', 'city_green', 'city_orange', 'city_red'];
var tiles = [] //size should be 19
var corners = [] //size should be 54
var corners_size = 54;

// Y-offsets for circle corners
var even_offsets = [0.25, 0.75, 1.75, 2.25, 3.25, 3.75];
var odd_offsets = [0, 1, 1.5, 2.5, 3, 4];

function preload() {
    sprites.forEach(function(sprite) {
        game.load.image(sprite, 'assets/img/' + sprite + '.png');
    });
    pieces.forEach(function(piece) {
        game.load.image(piece, 'assets/img/' + piece + '.png');
    });

}

function create() {

    // Set up group for the tiles and corners
    tileLayer = game.add.group();
    cornerLayer = game.add.group();
    pieceLayer = game.add.group();

    tileLayer.z = 0;
    cornerLayer.z = 1;
    pieceLayer.z = 2;

    // Set distances and offsets due to sprite scaling
    x_dist *= 0.75;
    y_dist *= 0.75;
    x_offset *= 0.75;

    game.stage.backgroundColor =  '#FFFFFF';

    // Create BitmapData
    bmd = game.add.bitmapData(1200,1000);

    // Put BitmapData in a Sprite
    sprite = game.add.sprite(0, 0, bmd);

    // game.add.tween(sprite).to( {  y: 100}, 2000, Phaser.Easing.Linear.None, true, 0, 1000, true);
    var circle_y_offset = 207;

    $.getJSON("/data/initial_state.json", function(json) {
        drawBoard(json); // this will show the info it in firebug console
    });



    var test = new Phaser.Circle(10, 10, 10);
    for (var i = 0; i < 3; i++) {
        // Offset that will change by 0.5 each j loop
        var h_offset = 2 + i;
        h_offset /= 2;
        h_offset = 3 - h_offset;
        // h_offset /= 2;
        for (var j = 0; j < 7 + i * 2; j++) {
            var x = 0;
            var y = 0;
            if ((j + i) % 2 == 0) {
                x = total_x_offset + h_offset * x_dist - 5;
                y = total_y_offset + circle_y_offset * even_offsets[i];
            } else {
                x = total_x_offset + h_offset * x_dist - 5;
                y = total_y_offset + circle_y_offset * odd_offsets[i];
            }

            var circle = new Phaser.Circle(x, y, 20);
            corners.push(circle);
            drawPiece(x, y, pieces[Math.floor((Math.random() * 8))]);
            // drawCorner(x, y, 20);
            h_offset += 0.5;
        }
    }


    console.log(corners);

    for (var i = 6; i >= 4; i--) {
        // Offset that will change by 0.5 each j loop
        var h_offset = 2 + (6 - i);
        h_offset /= 2;
        for (var j = 0; j < 11 - (6 - i) * 2; j++) {
            var x = 0;
            var y = 0;
            if ((j + i) % 2 == 0) {
                x = total_x_offset + h_offset * x_dist - 5;
                y = total_y_offset + circle_y_offset * (even_offsets[9 - i]);
            } else {
                x = total_x_offset + h_offset * x_dist - 5;
                y = total_y_offset + circle_y_offset * (odd_offsets[9 - i]);
            }

            var circle = new Phaser.Circle(x, y, 20);
            corners.push(circle);
            // drawCorner(x, y, 20);
            drawPiece(x, y, pieces[Math.floor((Math.random() * 8))]);
            h_offset += 0.5;
        }
    }

    console.log(corners);
    drawButtons();

    game.input.onDown.add(clicked, this);


}

function clicked(pointer) {
    // console.log(corners);
    // console.log(game.input.activePointer.positionDown.x + ": " + game.input.activePointer.positionDown.y);
    for (var ii = 0; ii < corners.length; ii++ ) {
        if (corners[ii].contains(game.input.activePointer.positionDown.x, game.input.activePointer.positionDown.y)) {
            console.log(ii);
            var data = {};
            if (action == 1) {
                data["build"] = { "structure" : "settlement", "location": ii, "player_id" : myId };
                eurecaServer.tryMove(data)
                action = -1;
            }
            break;
        }
    }
}

function drawButtons() {
    var settlement = game.add.sprite(1000, 800, 'settlement_green');
    settlement.inputEnabled = true;

    settlement.events.onInputDown.add(onDown, this);
}

function drawTile(x, y, tile_node) {
    // var spriteNumber = Math.floor((Math.random() * 7));
    var sprite = new Phaser.Sprite(game, x, y, tile_node.resource.toLowerCase());
    // var tile = game.add.sprite(x, y, sprites[spriteNumber]);
    tileLayer.add(sprite);
    tiles.push(sprite)
    sprite.scale.x = 0.75;
    sprite.scale.y = 0.75;
}

function drawCorner(x, y, r) {
    // Draw circle
    bmd.ctx.fillStyle = '#999999';
    bmd.ctx.beginPath();
    bmd.ctx.arc(x, y, r, 0, Math.PI*2, false);
    bmd.ctx.closePath();
    bmd.ctx.fill();
}

function drawPiece(x, y, piece_name) {
    var scale = 1;
    if (piece_name.indexOf('settlement') >= 0) {
        x -= 15;
        y -= 15;
        scale = 0.5;
    } else if (piece_name.indexOf('city') >= 0) {
        x -= 20;
        y -= 20;
        scale = 0.6;
    }
    var sprite = new Phaser.Sprite(game, x, y, piece_name);

    pieceLayer.add(sprite);
    sprite.scale.x = 0.5;
    sprite.scale.y = scale;
}

function drawBoard(tiles) {
    for (var i = 0; i < 3; i++) {
        drawTile(total_x_offset + 2 * x_offset + (i + 1) * x_dist, total_y_offset, tiles[i]);
    }

    for (var i = 0; i < 4; i++) {
        drawTile(total_x_offset + x_offset + (i + 1) * x_dist, y_dist + total_y_offset, tiles[i + 3]);
    }

    for (var i = 0; i < 5; i++) {
        drawTile(total_x_offset + (i + 1) * x_dist, 2 * y_dist + total_y_offset, tiles[i + 7]);
    }

    for (var i = 0; i < 4; i++) {
        drawTile(total_x_offset + x_offset + (i + 1) * x_dist, 3 * y_dist + total_y_offset, tiles[i + 12]);
    }

    for (var i = 0; i < 3; i++) {
        drawTile(total_x_offset + 2 * x_offset + (i + 1) * x_dist, 4 * y_dist + total_y_offset, tiles[i + 16]);
    }
}

function update() {
}

function render () {
}

function onDown(sprite, pointer) {
    if (sprite.key == "settlement") {
        console.log("Build settlement");
        action = 1;
    }
    console.log("You clicked me!");
}

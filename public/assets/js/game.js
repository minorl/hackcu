
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

    eurecaClient.exports.redraw = function(data) {
        drawPieces(data);
    }

    eurecaClient.exports.initBoard = function(data) {
        drawBoard(data);
    }
}

var game = new Phaser.Game(1400, 1200, Phaser.AUTO, 'game-container', { preload: preload, create: eurecaClientSetup, update: update, render: render});

var bmd;
var x_dist = 240;
var y_dist = 210;
var x_offset = 120;
var total_x_offset = -100;
var total_y_offset = 25;

var texts = {};

// Variable to store the action after having clicked on an action button
// -1 => no action, 0 => build road, 1 => build settlement, 2 => build city
var action = -1;

// Group for tiles
var tileLayer;

// Group for corners
var cornerLayer;

// Group for pieces
var pieceLayer;

var dieLayer;

// Lookup for player id and the color
var players = { '0': 'blue', '1': 'green', '2': 'orange', '3': 'red' }

var sprites = ['ore', 'wheat', 'desert', 'water', 'wood', 'brick', 'sheep'];
var icons = ['ore', 'wheat', 'wood', 'brick', 'sheep'];
var pieces = ['settlement_blue', 'settlement_green', 'settlement_orange', 'settlement_red',
              'city_blue', 'city_green', 'city_orange', 'city_red'];
var tiles = [] //size should be 19
var corners = [] //size should be 54
var corners_size = 54;

// Y-offsets for circle corners
var even_offsets = [0.25, 0.75, 1.75, 2.25, 3.25, 3.75];
var odd_offsets = [0, 1, 1.5, 2.5, 3, 4];

function preload() {
    sprites.forEach(function (sprite) {
        game.load.image(sprite, 'assets/img/' + sprite + '.png');
    });
    pieces.forEach(function (piece) {
        game.load.image(piece, 'assets/img/' + piece + '.png');
    });
    icons.forEach(function (icon) {
        game.load.image(icon + "_icon", 'assets/img/' + icon + '_icon.png');
    });
    for (var i = 2; i <= 12; i++) {
        if (i != 7)
            game.load.image("number_" + i, 'assets/img/' + 'number_' + i + '.png');
    }
}

function create() {

    // Set up group for the tiles and corners
    tileLayer = game.add.group();
    cornerLayer = game.add.group();
    pieceLayer = game.add.group();
    dieLayer = game.add.group();

    tileLayer.z = 0;
    cornerLayer.z = 1;
    pieceLayer.z = 2;
    dieLayer.z = 3;

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

    // $.getJSON("/data/initial_state.json", function(json) {
    //     drawBoard(json); // this will show the info it in firebug console
    // });



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
            // drawPiece(x, y, pieces[Math.floor((Math.random() * 8))]);
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
            // drawPiece(x, y, pieces[Math.floor((Math.random() * 8))]);
            h_offset += 0.5;
        }
    }



    console.log(corners);
    drawButtons();

    // $.getJSON("/data/examplegamestate.json", function(json) {
    //     drawPieces(json); // this will show the info it in firebug console
    // });

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
    if (tile_node.resource.toLowerCase() != "desert") {
        var die = new Phaser.Sprite(game, x + 45, y + 60, "number_" + tile_node.dienum);
        // var tile = game.add.sprite(x, y, sprites[spriteNumber]);

        dieLayer.add(die);

        die.scale.x = 0.5;
        die.scale.y = 0.5;
    }

    tiles.push(sprite);
    tileLayer.add(sprite);
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
    console.log(piece_name);
    var scale = 1;
    if (piece_name.indexOf('settlement') >= 0) {
        x -= 25;
        y -= 25;
        scale = 0.75;
    } else if (piece_name.indexOf('city') >= 0) {
        x -= 25;
        y -= 25;
        scale = 0.85;
    }
    // var sprite = new Phaser.Sprite(game, x, y, piece_name);

    var sprite = game.add.sprite(x, y, piece_name);
    sprite.scale.x = 0.75;
    sprite.scale.y = scale;
}

function drawPieces(data) {
    data.corner_states.forEach(function (corner_state) {
        if (corner_state.building_tag != null) {
            console.log(corner_state);
            var id = corner_state.id;
            var c = corners[id];
            drawPiece(c.x, c.y, corner_state.building_tag + '_' + players[corner_state.player_id]);
        }
    });

    data.edge_states.forEach(function (edge_state) {
        if (edge_state.player_id != null) {
            var edge_conn = edge_state.corners;
            var x1 = corners[edge_conn[0]].x;
            var y1 = corners[edge_conn[0]].y;
            var x2 = corners[edge_conn[1]].x;
            var y2 = corners[edge_conn[1]].y;
            drawRoad(x1, y1, x2, y2, players[edge_state.player_id]);
        }
    });

    var i = 0;
    data.player_states.forEach(function (player_state) {
        var c = i;
        if (player_state != null) {
            var resources = player_state.resources;
            var brick = resources.brick;
            var sheep = resources.sheep;
            var ore = resources.ore;
            var wheat = resources.wheat;
            var wood = resources.wood;
            if (texts[players[player_state.id]] == null) {
                var offset = 0;
                if (i < 2) {
                    offset = 0;
                } else {
                    c -= 2;
                    offset = 200;
                }

                var player_name = game.add.text(1000 + offset, 350 * c, players[player_state.id], { font: "24px Arial", fill: players[player_state.id], align: "center" });
                var player_score = game.add.text(1000 + offset + 100, 350 * c, ": " + player_state.score, { font: "24px Arial", fill: players[player_state.id], align: "center" });

                var brick_sprite = game.add.sprite(1000 + offset, 350 * c + 50, "brick_icon");
                var sheep_sprite = game.add.sprite(1000 + offset, 350 * c + 100, "sheep_icon");
                var ore_sprite = game.add.sprite(1005 + offset, 350 * c + 160, "ore_icon");
                var wheat_sprite = game.add.sprite(1005 + offset, 350 * c + 210, "wheat_icon");
                var wood_sprite = game.add.sprite(1005 + offset, 350 * c + 270, "wood_icon");

                var brick_text = game.add.text(1100 + offset, 350 * c + 60, ": " + brick, { font: "24px Arial", fill: players[player_state.id], align: "center" });
                var sheep_text = game.add.text(1100 + offset, 350 * c + 110, ": " + sheep, { font: "24px Arial", fill: players[player_state.id], align: "center" });
                var ore_text = game.add.text(1100 + offset, 350 * c + 170, ": " + ore, { font: "24px Arial", fill: players[player_state.id], align: "center" });
                var wheat_text = game.add.text(1100 + offset, 350 * c + 220, ": " + wheat, { font: "24px Arial", fill: players[player_state.id], align: "center" });
                var wood_text = game.add.text(1100 + offset, 350 * c + 280, ": " + wood, { font: "24px Arial", fill: players[player_state.id], align: "center" });

                texts[players[player_state.id]] = { "brick": brick_text,
                                                "sheep": sheep_text,
                                                "ore": ore_text,
                                                "wheat": wheat_text,
                                                "wood": wood_text,
                                                "score": player_score
                                            };
                i += 1;
            } else {
                texts[players[player_state.id]]["brick"].setText(": " + brick);
                texts[players[player_state.id]]["sheep"].setText(": " + sheep);
                texts[players[player_state.id]]["ore"].setText(": " + ore);
                texts[players[player_state.id]]["wheat"].setText(": " + wheat);
                texts[players[player_state.id]]["wood"].setText(": " + wood);
                texts[players[player_state.id]]["score"].setText(": " + player_state.score);
            }


        }
    });
}

function drawRoad(x1, y1, x2, y2, player) {
    bmd.ctx.beginPath();
    bmd.ctx.strokeStyle = player;
    bmd.ctx.moveTo(x1, y1);
    bmd.ctx.lineTo(x2, y2);
    bmd.ctx.lineWidth = 8;
    bmd.ctx.stroke();
    bmd.dirty = true;
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

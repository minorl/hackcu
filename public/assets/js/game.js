

var game = new Phaser.Game(1200, 1000, Phaser.AUTO, 'game-container', { preload: preload, create: create, update: update, render: render});

var bmd;
var x_dist = 240;
var y_dist = 210;
var x_offset = 120;
var total_x_offset = 25;
var total_y_offset = 25;

// Group for tiles
var tileLayer;

// Group for corners
var cornerLayer;

var sprites = ['ore', 'wheat', 'desert', 'water', 'wood', 'brick', 'sheep'];
var tiles = [] //size should be 19
var corners = [] //size should be 54
var corners_size = 54;

// Y-offsets for circle corners
var even_offsets = [0.25, 0.75, 1.75, 2.25, 3.25, 3.75];
var odd_offsets = [0, 1, 1.5, 2.5, 3, 4];

function preload() {
    sprites.forEach(function(sprite) {
        game.load.image(sprite, 'assets/img/' + sprite + '.png');
    })
}

function create() {

    // Set up group for the tiles and corners
    tileLayer = game.add.group();
    cornerLayer = game.add.group();

    tileLayer.z = 1;
    cornerLayer.z = 0;

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
    for (var i = 0; i < 3; i++) {
        drawTile(total_x_offset + 2 * x_offset + (i + 1) * x_dist, total_y_offset);
    }

    for (var i = 0; i < 4; i++) {
        drawTile(total_x_offset + x_offset + (i + 1) * x_dist, y_dist + total_y_offset);
    }

    for (var i = 0; i < 5; i++) {
        drawTile(total_x_offset + (i + 1) * x_dist, 2 * y_dist + total_y_offset);
    }

    for (var i = 0; i < 4; i++) {
        drawTile(total_x_offset + x_offset + (i + 1) * x_dist, 3 * y_dist + total_y_offset);
    }

    for (var i = 0; i < 3; i++) {
        drawTile(total_x_offset + 2 * x_offset + (i + 1) * x_dist, 4 * y_dist + total_y_offset);
    }
    // rock1.inputEnabled = true;

    // rock1.events.onInputDown.add(onDown, this);
    var circle_y_offset = 207;



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
            // drawCorner(x, y, 20);
            h_offset += 0.5;
        }
    }

    for (var i = 6; i >= 3; i--) {
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
            h_offset += 0.5;
        }
    }

    game.input.onDown.add(clicked, this);

}

clicked = function(pointer) {
    // console.log(corners);
    // console.log(game.input.activePointer.positionDown.x + ": " + game.input.activePointer.positionDown.y);
    for (var ii = 0; ii < corners.length; ii++ ) {
        if (corners[ii].contains(game.input.activePointer.positionDown.x, game.input.activePointer.positionDown.y)) {
            console.log(ii);
            break;
        }
    }
}

function drawTile(x, y) {
    var spriteNumber = Math.floor((Math.random() * 7));
    var sprite = new Phaser.Sprite(game, x, y, sprites[spriteNumber]);
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

function update() {
}

function render () {
}

function onDown(sprite, pointer) {
    console.log("You clicked me!");
}

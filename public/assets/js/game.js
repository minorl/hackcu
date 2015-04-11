

var game = new Phaser.Game(1200, 1000, Phaser.AUTO, 'game-container', { preload: preload, create: create, update: update, render: render});

var bmd;
var x_dist = 240;
var y_dist = 210;
var x_offset = 120;
var total_offset = 25;

var sprites = ['ore', 'wheat', 'desert', 'water', 'wood', 'brick', 'sheep'];
var tiles = [] //size should be 19

function preload() {
    sprites.forEach(function(sprite) {
        game.load.image(sprite, 'assets/img/' + sprite + '.png');
    })
}

function create() {

    // Set distances and offsets due to sprite scaling
    x_dist *= 0.75;
    y_dist *= 0.75;
    x_offset *= 0.75;

    game.stage.backgroundColor =  '#FFFFFF';

    // Create BitmapData
    bmd = game.add.bitmapData(1200,1000);

    // Draw circle
    bmd.ctx.fillStyle = '#999999';
    // bmd.ctx.beginPath();
    // bmd.ctx.rectangle(300, 200, 100, 100);
    // bmd.ctx.closePath();
    // bmd.ctx.fill();

    // Put BitmapData in a Sprite
    sprite = game.add.sprite(0, 0, bmd);

    // game.add.tween(sprite).to( {  y: 100}, 2000, Phaser.Easing.Linear.None, true, 0, 1000, true);
    for (var i = 0; i < 3; i++) {
        drawTile(total_offset + 2 * x_offset + (i + 1) * x_dist, 0);
    }

    for (var i = 0; i < 4; i++) {
        drawTile(total_offset + x_offset + (i + 1) * x_dist, y_dist);
    }

    for (var i = 0; i < 5; i++) {
        drawTile(total_offset + (i + 1) * x_dist, 2 * y_dist);
    }

    for (var i = 0; i < 4; i++) {
        drawTile(total_offset + x_offset + (i + 1) * x_dist, 3 * y_dist);
    }

    for (var i = 0; i < 3; i++) {
        drawTile(total_offset + 2 * x_offset + (i + 1) * x_dist, 4 * y_dist);
    }
    // var rock7 = game.add.sprite(120, 0, "ore");
    // var rock6 = game.add.sprite(360, 0, "wheat");
    // var rock1 = game.add.sprite(0, 210, "desert");
    // var rock2 = game.add.sprite(240, 210, "water");
    // var rock3 = game.add.sprite(480, 210, "wood");
    // var rock4 = game.add.sprite(120, 420, "brick");
    // var rock5 = game.add.sprite(360, 420, "sheep");
    // rock1.scale.x = 0.5;
    // rock1.inputEnabled = true;

    // rock1.events.onInputDown.add(onDown, this);
}

function drawTile(x, y) {
    var sprite = Math.floor((Math.random() * 7));
    var tile = game.add.sprite(x, y, sprites[sprite]);
    tiles.push(tile)
    tile.scale.x = 0.75;
    tile.scale.y = 0.75;
}

function update() {
}

function render () {
}

function onDown(sprite, pointer) {
    console.log("You clicked me!");
}

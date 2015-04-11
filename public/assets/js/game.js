

    var game = new Phaser.Game(1200, 1000, Phaser.AUTO, 'phaser-example', { preload: preload, create: create, update: update, render: render});

    var bmd;

    function preload() {
        game.load.image('rock', 'assets/img/rock.png');
        game.load.image('wheat', 'assets/img/wheat.png');
        game.load.image('desert', 'assets/img/desert.png');
        game.load.image('water', 'assets/img/water.png');
        game.load.image('wood', 'assets/img/wood.png');
        game.load.image('brick', 'assets/img/brick.png');
        game.load.image('sheep', 'assets/img/sheep.png');
    }

    function create() {

        game.stage.backgroundColor =  '#FFFFFF';

        // Create BitmapData
        bmd = game.add.bitmapData(800,600);

        // Draw circle
        bmd.ctx.fillStyle = '#999999';
        // bmd.ctx.beginPath();
        // bmd.ctx.rectangle(300, 200, 100, 100);
        // bmd.ctx.closePath();
        // bmd.ctx.fill();

        // Put BitmapData in a Sprite
        sprite = game.add.sprite(0, 0, bmd);

        game.add.tween(sprite).to( {  y: 100}, 2000, Phaser.Easing.Linear.None, true, 0, 1000, true);
        var rock4 = game.add.sprite(120, 0, "rock");
        var rock5 = game.add.sprite(360, 0, "wheat");
        var rock1 = game.add.sprite(0, 210, "desert");
        var rock2 = game.add.sprite(240, 210, "water");
        var rock3 = game.add.sprite(480, 210, "wood");
        var rock4 = game.add.sprite(120, 420, "brick");
        var rock5 = game.add.sprite(360, 420, "sheep");
        rock1.inputEnabled = true;

        rock1.events.onInputDown.add(onDown, this);
    }

    function update() {
    }

    function render () {
    }

    function onDown(sprite, pointer) {
        console.log("You clicked me!");
    }

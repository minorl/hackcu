

    var game = new Phaser.Game(800, 600, Phaser.AUTO, 'phaser-example', { preload: preload, create: create, update: update, render: render});

    var bmd;

    function preload() {
        game.load.image('rock', 'assets/img/rock.png');
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

        // Tweening just for fun :)
        game.add.tween(sprite).to( {  y: 100}, 2000, Phaser.Easing.Linear.None, true, 0, 1000, true);
        var rock = game.add.sprite(0, 0, "rock");
        var rock = game.add.sprite(240, 0, "rock");
        var rock = game.add.sprite(480, 0, "rock");
        var rock = game.add.sprite(120, 210, "rock");
        var rock = game.add.sprite(360, 210, "rock");
    }

    function update() {
    }

    function render () {
    }

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Battle Royale Arcade</title>

<style>
body{
    margin:0;
    overflow:hidden;
    background:#111;
    font-family:Arial;
    color:white;
}

#ui{
    position:absolute;
    top:10px;
    left:10px;
    z-index:10;
}

#deathScreen{
    display:none;
    position:absolute;
    width:100%;
    height:100%;
    background:black;
    color:red;
    font-size:50px;
    text-align:center;
    padding-top:200px;
}

.player{
    width:40px;
    height:40px;
    background:green;
    position:absolute;
    bottom:50px;
}

.enemy{
    width:40px;
    height:40px;
    background:red;
    position:absolute;
}

.chest{
    width:30px;
    height:30px;
    background:gold;
    position:absolute;
}

</style>
</head>

<body>

<div id="ui">
❤️ HP: <span id="hp">100</span><br>
💰 Money: <span id="money">0</span><br>
📈 Level: <span id="level">1</span><br>
🔊 Volume: <input type="range" min="0" max="100" value="50" id="vol">
</div>

<div id="deathScreen">
💀 YOU DIED 💀<br>
Press R to Retry
</div>

<div class="player" id="player"></div>

<audio id="music" loop autoplay>
<source src="https://cdn.pixabay.com/audio/2022/10/16/audio_1f1b8c.mp3">
</audio>

<script>

let hp = 100;
let money = 0;
let level = 1;

let player = document.getElementById("player");

let x = 200;

document.addEventListener("keydown",(e)=>{

    if(e.key=="ArrowLeft") x -= 20;
    if(e.key=="ArrowRight") x += 20;

    player.style.left = x+"px";

    if(e.key==" "){
        shoot();
    }

    if(e.key=="r"){
        location.reload();
    }

});

function shoot(){

    document.querySelectorAll(".enemy").forEach(enemy=>{

        if(hit(player,enemy)){
            enemy.remove();

            money += 100;

            if(Math.random()<0.3){
                money += 1000; // rare loot feel
            }

            update();
        }

    });

    document.querySelectorAll(".chest").forEach(chest=>{

        if(hit(player,chest)){
            chest.remove();

            let loot = Math.random();

            if(loot<0.6) money += 100;
            else if(loot<0.85) money += 10000;
            else money += 100000;

            update();
        }

    });

}

function spawnEnemy(){

    let e = document.createElement("div");
    e.classList.add("enemy");

    e.style.left = Math.random()*window.innerWidth+"px";
    e.style.top = "0px";

    document.body.appendChild(e);

    let t = setInterval(()=>{

        let top = parseInt(e.style.top);
        e.style.top = top + (2 + level*0.5) + "px";

        if(hit(e,player)){
            hp -= 10;

            if(hp<=0){
                gameOver();
            }

            update();
        }

        if(top > window.innerHeight){
            e.remove();
            clearInterval(t);
        }

    },30);

}

function spawnChest(){

    let c = document.createElement("div");
    c.classList.add("chest");

    c.style.left = Math.random()*window.innerWidth+"px";
    c.style.top = Math.random()*300+"px";

    document.body.appendChild(c);

    setTimeout(()=>c.remove(),10000);
}

function hit(a,b){
    let r1 = a.getBoundingClientRect();
    let r2 = b.getBoundingClientRect();

    return !(r1.right<r2.left ||
             r1.left>r2.right ||
             r1.bottom<r2.top ||
             r1.top>r2.bottom);
}

function gameOver(){
    document.getElementById("deathScreen").style.display="block";
}

function update(){
    document.getElementById("hp").innerText = hp;
    document.getElementById("money").innerText = money;
    document.getElementById("level").innerText = level;
}

setInterval(spawnEnemy,1000);
setInterval(spawnChest,3000);

setInterval(()=>{
    level++;
},15000);

document.getElementById("vol").addEventListener("input",(e)=>{
    document.getElementById("music").volume = e.target.value/100;
});

update();

</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
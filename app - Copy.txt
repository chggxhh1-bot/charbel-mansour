from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Emoji Game PRO MAX</title>

<style>
body{
    margin:0;
    font-family:Arial;
    text-align:center;
    color:white;

    background:url("https://media.giphy.com/media/xT0GqtpF1NWd9VZL7q/giphy.gif") no-repeat center center fixed;
    background-size:cover;
}

/* SCREENS */
.screen{
    position:absolute;
    width:100%;
    height:100%;
}

#menu{ display:block; }
#game{ display:none; }
#gameover{ display:none; }
#pause{ display:none; }

/* BUTTONS */
button{
    padding:12px 18px;
    margin:8px;
    border:none;
    border-radius:12px;
    cursor:pointer;
    font-size:16px;
}

/* HUD */
#hud{
    display:flex;
    justify-content:space-around;
    font-size:18px;
    margin-top:10px;
}

/* BIG EMOJI */
#emoji{
    font-size:100px;
    margin:25px;
}

/* TIMER */
#timer{
    font-size:20px;
    color:yellow;
}

/* HANDICAP */
#handicap{
    display:none;
    color:lime;
    font-weight:bold;
}
</style>
</head>

<body>

<!-- 🎮 MENU -->
<div id="menu" class="screen">

<h1>🎮 EMOJI GAME PRO</h1>

<button onclick="setMode('humans')">👤 Humains</button>
<button onclick="setMode('faces')">😀 Visages</button>
<button onclick="setMode('cars')">🚗 Voitures</button>

<br><br>

<button onclick="setDiff('normal')">Normal</button>
<button onclick="setDiff('handicap')">♿ Handicap</button>

<br><br>

<button onclick="startGame()">▶ START</button>

</div>

<!-- 🎯 GAME -->
<div id="game" class="screen">

<div id="hud">
    <div>Score: <span id="score">0</span></div>
    <div>Combo: <span id="combo">0</span></div>
    <div>Level: <span id="level">1</span></div>
</div>

<div id="timer">⏳ 120</div>

<div id="handicap">♿ HANDICAP</div>

<button onclick="pauseGame()">⏸ PAUSE</button>

<div id="emoji">❓</div>

<input id="input" placeholder="type answer">
<br><br>

<button onclick="check()">SUBMIT</button>

<p id="msg"></p>

</div>

<!-- ⏸ PAUSE -->
<div id="pause" class="screen">

<h1>⏸ PAUSE</h1>

<button onclick="resumeGame()">▶ RESUME</button>
<button onclick="goMenu()">🏠 MENU</button>

</div>

<!-- 💀 GAME OVER -->
<div id="gameover" class="screen">

<h1>💀 GAME OVER</h1>

<p>Your score: <span id="finalScore"></span></p>

<button onclick="restart()">🔁 TRY AGAIN</button>
<button onclick="goMenu()">🏠 MENU</button>

</div>

<script>

let mode="humans";
let score=0;
let combo=0;
let level=1;
let current="";
let handicap=false;

let time=120;
let timer;

const data={
 humans:["🧑","👨","👩","🧒","👶","🧓"],
 faces:["😀","😂","😍","😎","😭","😡","😱"],
 cars:["🚗","🚕","🚙","🏎️","🚓","🚑"]
};

/* MODE */
function setMode(m){ mode=m; }

/* DIFF */
function setDiff(d){ handicap=(d==="handicap"); }

/* START */
function startGame(){
    document.getElementById("menu").style.display="none";
    document.getElementById("game").style.display="block";

    if(handicap){
        document.getElementById("handicap").style.display="block";
    }

    time=120;
    score=0;
    combo=0;
    level=1;

    startTimer();
    next();
}

/* TIMER */
function startTimer(){
    timer=setInterval(()=>{
        time--;
        document.getElementById("timer").innerText="⏳ "+time;

        if(time<=0){
            gameOver();
        }
    },1000);
}

/* NEXT */
function next(){
    let list=data[mode];
    current=list[Math.floor(Math.random()*list.length)];

    document.getElementById("emoji").innerText=current;
    document.getElementById("input").value="";
}

/* CHECK */
function check(){

    let g=document.getElementById("input").value.trim();

    let ok=false;

    if(handicap) ok=true;
    else if(g===current) ok=true;

    if(ok){
        combo++;
        score+=combo*10;
        level++;
        document.getElementById("msg").innerText="🔥 GOOD";
    }else{
        combo=0;
        document.getElementById("msg").innerText="❌ WRONG";
    }

    updateUI();
    setTimeout(next,600);
}

function updateUI(){
    document.getElementById("score").innerText=score;
    document.getElementById("combo").innerText=combo;
    document.getElementById("level").innerText=level;
}

/* PAUSE */
function pauseGame(){
    clearInterval(timer);
    document.getElementById("game").style.display="none";
    document.getElementById("pause").style.display="block";
}

function resumeGame(){
    document.getElementById("pause").style.display="none";
    document.getElementById("game").style.display="block";
    startTimer();
}

/* GAME OVER */
function gameOver(){
    clearInterval(timer);
    document.getElementById("game").style.display="none";
    document.getElementById("gameover").style.display="block";

    document.getElementById("finalScore").innerText=score;
}

/* TRY AGAIN */
function restart(){
    document.getElementById("gameover").style.display="none";
    startGame();
}

/* MENU */
function goMenu(){
    location.reload();
}

</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
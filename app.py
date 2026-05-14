from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Emoji Game V7</title>

<style>
body{
  margin:0;
  font-family:Arial;
  text-align:center;
  background:#111;
  color:white;
}

.screen{display:none; padding-top:30px;}
#menu{display:block;}

button{
  padding:10px;
  margin:5px;
  border-radius:10px;
  border:none;
  cursor:pointer;
}

#emoji{font-size:90px; margin:20px;}
</style>
</head>

<body>

<!-- MENU -->
<div id="menu" class="screen">
<h1>🎮 Emoji Game V7</h1>

<button onclick="setMode('cars')">🚗 Cars</button>
<button onclick="setMode('faces')">😀 Faces</button>

<br><br>

<input id="player" placeholder="Your name">

<br><br>

<button onclick="startGame()">▶ START</button>
</div>

<!-- GAME -->
<div id="game" class="screen">

<h2>Score: <span id="score">0</span></h2>

<div id="emoji">❓</div>

<input id="input" placeholder="type OR speak">

<br><br>

<button onclick="check()">OK</button>
<button onclick="startVoice()">🎤 MIC</button>

<p id="msg"></p>

<audio id="good" src="https://www.soundjay.com/buttons/sounds/button-3.mp3"></audio>
<audio id="bad" src="https://www.soundjay.com/buttons/sounds/button-10.mp3"></audio>
<audio id="music" src="https://cdn.pixabay.com/audio/2022/10/16/audio_12b6b1c1d2.mp3" loop></audio>

<h3>🏆 Leaderboard</h3>
<ul id="board"></ul>

</div>

<script>

let mode="cars";
let score=0;
let current="";
let answer="";
let player="Player";

/* 🚗 DATA */
const data={
 cars:[
  {emoji:"🚗", answer:"car"},
  {emoji:"🚕", answer:"taxi"},
  {emoji:"🚒", answer:"fire engine"},
  {emoji:"🚚", answer:"truck"},
  {emoji:"🚓", answer:"police car"}
 ],
 faces:[
  {emoji:"😀", answer:"happy"},
  {emoji:"😡", answer:"angry"},
  {emoji:"😴", answer:"sleep"}
 ]
};

/* 🌍 AI MULTI-LANG (10+ variations) */
function aiNormalize(t){
  return t.toLowerCase().trim();
}

function aiCheck(input, correct){

const map={
 "car":["car","voiture","siyara","سيارة","auto","automobile"],
 "taxi":["taxi","تاكسي"],
 "fire engine":["fire engine","camion pompier","اطفاء","fire truck"],
 "truck":["truck","camion","شاحنة"],
 "police car":["police","voiture police","شرطة","douriye"],
 "happy":["happy","smile","sourire","happy face","😀"],
 "angry":["angry","rage","غاضب"],
 "sleep":["sleep","dormir","نائم"]
};

let i=aiNormalize(input);
let c=aiNormalize(correct);

return map[c] ? map[c].includes(i) : i===c;
}

/* 🎮 START */
function startGame(){
  player=document.getElementById("player").value || "Player";

  document.getElementById("menu").style.display="none";
  document.getElementById("game").style.display="block";

  document.getElementById("music").play();

  next();
}

/* NEXT */
function next(){
  let list=data[mode];
  let item=list[Math.floor(Math.random()*list.length)];

  current=item.emoji;
  answer=item.answer;

  document.getElementById("emoji").innerText=current;
  document.getElementById("input").value="";
}

/* 🔊 SOUND */
function soundGood(){
  document.getElementById("good").play();
}

function soundBad(){
  document.getElementById("bad").play();
}

/* 🎤 VOICE */
function startVoice(){
  let rec = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
  rec.lang = "en-US";

  rec.onresult = function(e){
    document.getElementById("input").value = e.results[0][0].transcript;
    check();
  }

  rec.start();
}

/* 🏆 LEADERBOARD */
function saveScore(){
  let board = JSON.parse(localStorage.getItem("board") || "[]");

  board.push({name:player, score:score});
  board.sort((a,b)=>b.score-a.score);
  board = board.slice(0,5);

  localStorage.setItem("board", JSON.stringify(board));
  showBoard();
}

function showBoard(){
  let board = JSON.parse(localStorage.getItem("board") || "[]");
  let html="";

  board.forEach(b=>{
    html+=`<li>${b.name} - ${b.score}</li>`;
  });

  document.getElementById("board").innerHTML=html;
}

/* CHECK */
function check(){
  let val=document.getElementById("input").value;

  if(aiCheck(val,answer)){
    score+=10;
    document.getElementById("msg").innerText="🔥 GOOD";
    soundGood();
  }else{
    document.getElementById("msg").innerText="❌ WRONG";
    soundBad();
  }

  document.getElementById("score").innerText=score;

  saveScore();

  setTimeout(next,600);
}

</script>

</body>
</html>
"""

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
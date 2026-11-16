
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neon Flappy Bird",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 50% 0%, #14213d 0%, #080d1c 48%, #050812 100%);
    color: #eaf7ff;
}
[data-testid="stHeader"], footer, #MainMenu {visibility:hidden;}
.block-container {padding-top: 1.2rem; max-width: 1050px;}
.hero {text-align:center; margin-bottom: 12px;}
.hero h1 {
    font-family: 'Orbitron', sans-serif; font-weight:800; letter-spacing:3px;
    font-size: clamp(28px, 5vw, 48px); margin: 0;
    color:#e9fbff; text-shadow:0 0 8px #00d9ff, 0 0 24px #0077ff;
}
.hero p {color:#8ba8c7; font-family:Inter,sans-serif; margin-top:8px; letter-spacing:1px;}
.hint {text-align:center;color:#7895b7;font-size:12px;letter-spacing:1px;margin-top:10px;}
</style>
<div class="hero">
  <h1>NEON FLAPPY</h1>
  <p>FLY • DODGE • SURVIVE</p>
</div>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
*{box-sizing:border-box}
body{margin:0;background:transparent;color:#e9faff;font-family:Arial,sans-serif;overflow:hidden}
.shell{width:100%;max-width:820px;margin:auto}
.hud{display:flex;justify-content:space-between;align-items:center;padding:10px 4px 12px;gap:8px}
.pill{border:1px solid #174b70;background:rgba(5,20,39,.85);border-radius:12px;padding:8px 14px;min-width:105px;text-align:center;box-shadow:0 0 16px #00bfff18}
.small{font-size:10px;letter-spacing:2px;color:#72a9c9}
.value{font-size:22px;font-weight:800;color:#dffaff;text-shadow:0 0 10px #00d9ff}
#game{display:block;width:100%;height:auto;aspect-ratio: 7 / 5;border:1px solid #14527a;border-radius:16px;background:#071326;box-shadow:0 0 22px #00bfff30, inset 0 0 20px #00bfff12;touch-action:manipulation}
.controls{display:flex;justify-content:center;gap:10px;margin-top:12px;flex-wrap:wrap}
button{background:linear-gradient(135deg,#00c9ed,#0875ff);color:#00101e;border:0;border-radius:10px;padding:12px 24px;font-weight:900;letter-spacing:1px;cursor:pointer;box-shadow:0 0 18px #00bfff55}
button.secondary{background:#0b1c31;color:#b9eaff;border:1px solid #205174;box-shadow:none}
.note{text-align:center;color:#7695b4;font-size:12px;line-height:1.6;margin:10px 0 0}
@media(max-width:520px){.pill{min-width:82px;padding:7px 9px}.value{font-size:19px}button{padding:11px 18px}}
</style>
</head>
<body>
<div class="shell">
 <div class="hud">
  <div class="pill"><div class="small">SCORE</div><div class="value" id="score">0</div></div>
  <div class="pill"><div class="small">BEST</div><div class="value" id="best">0</div></div>
  <div class="pill"><div class="small">SPEED</div><div class="value" id="speed">1.0x</div></div>
 </div>
 <canvas id="game" width="700" height="500" tabindex="0" aria-label="Neon Flappy Bird game. Press Space or Arrow Up to flap."></canvas>
 <div class="controls">
  <button id="start">START GAME</button>
  <button class="secondary" id="sound">SOUND: ON</button>
 </div>
 <div class="note">SPACE / CLICK / TAP TO FLAP &nbsp; • &nbsp; Avoid the neon pipes</div>
</div>
<script>
(() => {
const canvas=document.getElementById('game'), ctx=canvas.getContext('2d');
const W=700,H=500, scoreEl=document.getElementById('score'),bestEl=document.getElementById('best'),speedEl=document.getElementById('speed');
let best=0; try{best=Number(localStorage.getItem('neonFlappyBest')||0)}catch(e){}
bestEl.textContent=best;
let state='ready',score=0,frame=0, bird, pipes=[], particles=[], stars=[], soundOn=true, audioCtx=null;
const rand=(a,b)=>Math.random()*(b-a)+a;
for(let i=0;i<90;i++) stars.push({x:rand(0,W),y:rand(0,H),r:rand(.5,2),a:rand(.2,.9),s:rand(.15,.55)});
function reset(){score=0;frame=0;pipes=[];particles=[];bird={x:165,y:245,vy:0,r:15,rot:0};scoreEl.textContent=0;speedEl.textContent='1.0x';state='ready';}
reset();
function beep(freq=500,dur=.06,type='sine'){if(!soundOn)return;try{audioCtx=audioCtx||new(window.AudioContext||window.webkitAudioContext)();let o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type=type;o.frequency.value=freq;g.gain.setValueAtTime(.045,audioCtx.currentTime);g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+dur);o.connect(g);g.connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+dur)}catch(e){}}
function flap(){if(state==='over'){reset();state='playing';bird.vy=-6.4;beep(620);return}if(state==='ready')state='playing';if(state==='playing'){bird.vy=-6.4;beep(620,.07,'triangle');for(let i=0;i<5;i++)particles.push({x:bird.x-10,y:bird.y+rand(-5,5),vx:rand(-2,-.5),vy:rand(-1,1),life:20});}}
function action(e){if(e)e.preventDefault();flap()}
canvas.addEventListener('pointerdown',e=>{canvas.focus();action(e)});
function handleKey(e){
 if(e.code==='Space'||e.code==='ArrowUp'){
  e.preventDefault();
  if(!e.repeat) flap();
 }
}
// Capture keys at the iframe window and document level. Focusing the canvas
// ensures the embedded game receives keyboard input after a click or tap.
window.addEventListener('keydown',handleKey);
document.addEventListener('keydown',handleKey);
document.getElementById('start').onclick=()=>{
 if(state==='over'||state==='ready'){
  reset();state='playing';flap();
 }
 canvas.focus();
};
canvas.addEventListener('blur',()=>{});
document.getElementById('sound').onclick=()=>{soundOn=!soundOn;document.getElementById('sound').textContent='SOUND: '+(soundOn?'ON':'OFF');};
function roundedRect(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill()}
function drawBackground(){
 let g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#07152d');g.addColorStop(.65,'#0a2140');g.addColorStop(1,'#102c48');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 stars.forEach(s=>{s.x-=s.s;if(s.x<0)s.x=W;ctx.globalAlpha=s.a*(.65+.35*Math.sin(frame*.04+s.y));ctx.fillStyle='#a7eaff';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
 // distant neon skyline
 ctx.fillStyle='#0a1a32';for(let i=0;i<14;i++){let x=i*58-(frame*.25%58),h=45+(i*37%75);ctx.fillRect(x,H-48-h,38,h)}
 ctx.strokeStyle='#0c4565';ctx.globalAlpha=.35;ctx.lineWidth=1;for(let y=H-48;y<H;y+=14){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}ctx.globalAlpha=1;
 ctx.fillStyle='#0b2741';ctx.fillRect(0,H-44,W,44);ctx.fillStyle='#00d9ff';ctx.shadowBlur=14;ctx.shadowColor='#00d9ff';ctx.fillRect(0,H-45,W,2);ctx.shadowBlur=0;
}
function drawPipe(p){
 const gap= p.gap, topH=p.top, botY=topH+gap;
 const grad=ctx.createLinearGradient(p.x,0,p.x+66,0);grad.addColorStop(0,'#087b9e');grad.addColorStop(.45,'#20f3db');grad.addColorStop(1,'#087b9e');
 ctx.fillStyle=grad;ctx.shadowColor='#00ffd5';ctx.shadowBlur=17;
 roundedRect(p.x,0,66,topH-17,8);roundedRect(p.x-7,topH-18,80,18,5);
 roundedRect(p.x,botY+17,66,H-botY-17,8);roundedRect(p.x-7,botY,80,18,5);
 ctx.shadowBlur=0;ctx.fillStyle='rgba(255,255,255,.22)';ctx.fillRect(p.x+10,5,4,Math.max(0,topH-28));ctx.fillRect(p.x+10,botY+27,4,H-botY-35);
}
function drawBird(){
 ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot);
 ctx.shadowColor='#00d9ff';ctx.shadowBlur=22;
 let gr=ctx.createLinearGradient(-16,-15,17,16);gr.addColorStop(0,'#fff');gr.addColorStop(.35,'#50f4ff');gr.addColorStop(1,'#087dff');
 ctx.fillStyle=gr;ctx.beginPath();ctx.ellipse(0,0,18,14,0,0,Math.PI*2);ctx.fill();
 ctx.shadowBlur=0;ctx.fillStyle='#b8ffff';ctx.beginPath();ctx.ellipse(-8,5,9,5,-.3,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(8,-5,5,0,Math.PI*2);ctx.fill();ctx.fillStyle='#06152a';ctx.beginPath();ctx.arc(10,-5,2.2,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#ffb84d';ctx.shadowColor='#ff8c00';ctx.shadowBlur=8;ctx.beginPath();ctx.moveTo(15,1);ctx.lineTo(27,5);ctx.lineTo(15,8);ctx.closePath();ctx.fill();

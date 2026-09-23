(() => {
  const $ = (s) => document.querySelector(s);
  const terminal = $('#terminal');
  const boot = $('#boot');
  const app = $('#app');
  const reveal = $('#reveal');
  const input = $('#commandInput');
  const timeline = $('#timeline');
  let paused = false, soundOn = true, started = Date.now(), revealed = false;
  let eventIndex = 0;
  const timers = [];

  const fake = {
    hex(n=4){ return Array.from({length:n},()=>Math.floor(Math.random()*16).toString(16)).join('').toUpperCase(); },
    ip(){ return `10.${20+Math.floor(Math.random()*60)}.${10+Math.floor(Math.random()*240)}.${10+Math.floor(Math.random()*240)}`; },
    session(){ return `BT-${fake.hex(6)}`; },
    trace(){ return `TR-${1000+Math.floor(Math.random()*8999)}`; }
  };

  $('#sessionId').textContent = fake.session();
  $('#virtualIp').textContent = fake.ip();
  $('#traceId').textContent = fake.trace();

  function beep(freq=440, duration=.045){
    if(!soundOn) return;
    try{
      const C = window.AudioContext || window.webkitAudioContext;
      if(!C) return;
      const ctx = new C(); const o=ctx.createOscillator(); const g=ctx.createGain();
      o.frequency.value=freq; o.type='square'; g.gain.value=.018; o.connect(g); g.connect(ctx.destination);
      o.start(); o.stop(ctx.currentTime+duration);
      o.onended=()=>ctx.close();
    }catch{}
  }

  function addLine(text, type='info', delay=0){
    const t=setTimeout(()=>{
      if(paused){ addLine(text,type,250); return; }
      const div=document.createElement('div'); div.className=`line ${type}`; div.textContent=text;
      terminal.appendChild(div); terminal.scrollTop=terminal.scrollHeight; beep(type==='alert'?160:420, .025);
    }, delay); timers.push(t);
  }

  function setTimeline(label, state='done'){
    const li=document.createElement('li'); li.textContent=label; li.className=state; timeline.appendChild(li);
  }

  function bootSequence(){
    const msgs=['LOADING COGNITIVE ENGINE...','LOADING CRYPTOGRAPHIC MODULE...','LOADING THREAT-ANALYSIS MODULE...','LOADING VISUALIZATION ENGINE...','SIMULATION ENVIRONMENT READY.'];
    let i=0;
    const iv=setInterval(()=>{
      $('#bootLine').textContent=msgs[Math.min(i,msgs.length-1)];
      $('#bootBar').style.width=`${Math.min(100,(i+1)*20)}%`;
      beep(240+i*45,.025); i++;
      if(i>msgs.length){clearInterval(iv); setTimeout(()=>{boot.classList.add('hidden');app.classList.remove('hidden');start();},500);}
    },420);
  }

  function start(){
    setTimeline('Initialize operation','current');
    addLine('BLACKTRACE // ZERO-DAY SIMULATION', 'ok');
    addLine('> This terminal is a visual simulation. No real system access is performed.', 'dim', 100);
    addLine('> initialize --operation ZERO-DAY','info',500);
    addLine('[21:47:03] Initializing operation...','info',800);
    addLine('[21:47:04] Establishing virtual session...','info',1050);
    addLine('[21:47:05] Generating simulated target...','ok',1300);
    addLine('[21:47:06] Mapping virtual environment...','info',1550);
    setTimeout(()=>runStage(),1800);
  }

  function runStage(){
    if(revealed) return;
    const stages=[
      {label:'Virtual environment mapped', lines:[['> generate-target --virtual','info'],['[+] Virtual target generated.','ok'],['[+] NODE-07 linked to NODE-42.','ok']]},
      {label:'Surface analysis', lines:[['> analyze-surface --virtual','info'],['[+] Simulated attack surface: 17 nodes.','ok'],['[+] No real network traffic generated.','dim']]},
      {label:'NEXUS AI activated', lines:[['> activate-nexus','ai'],['[NEXUS] Pattern recognition initialized.','ai'],['[NEXUS] Decision confidence: 99%.','ai']]},
      {label:'Route calculation', lines:[['> calculate-route --simulation','info'],['[+] Virtual route calculated.','ok'],['[+] Countermeasure protocol staged.','ok']]},
      {label:'Anomaly detected', lines:[['[!] ANOMALY DETECTED','alert'],['[!] VIRTUAL SECURITY LAYER RESPONDING','alert'],['[!] TRACE SIGNATURE GENERATED','warn']]}
    ];
    const s=stages[eventIndex++];
    if(!s){escalate();return;}
    timeline.querySelectorAll('li.current').forEach(x=>x.classList.replace('current','done'));
    setTimeline(s.label,'current'); s.lines.forEach((x,i)=>addLine(x[0],x[1],i*350));
    if(s.label==='Anomaly detected'){
      setTimeout(()=>{$('#traceStatus').textContent='DETECTED';$('#traceStatus').style.color='var(--red)';$('#warningBox').classList.add('hot');$('#threatLevel').textContent='CRITICAL';$('#threatEvents').textContent='07';$('#nexusMessage').textContent='Wait... this pattern is inconsistent. Analyzing anomaly...';},900);
    }
    setTimeout(runStage, s.lines.length*380+800);
  }

  function escalate(){
    timeline.querySelectorAll('li.current').forEach(x=>x.classList.replace('current','done'));
    setTimeline('Countermeasure protocol','current');
    addLine('> run-countermeasure --test','warn');
    const steps=[12,27,41,68,83,97,99];
    steps.forEach((v,i)=>addLine(`[SIMULATION] Countermeasure progress: ${v}%`,v>80?'warn':'info',500+i*450));
    setTimeout(()=>{
      document.body.classList.add('shake');
      $('#warningBox').textContent='EXTERNAL TRACE DETECTED — SIMULATED EVENT';
      $('#nexusMessage').textContent='NEXUS: Wait... this does not look right.';
      addLine('!!! WARNING !!!','alert');
      addLine('EXTERNAL TRACE DETECTED','alert',300);
      addLine('SOURCE: UNKNOWN [SIMULATED]','alert',600);
      addLine('TRACE DISTANCE: 0.7 KM [FICTIONAL]','warn',900);
      addLine('RESPONSE: IMMEDIATE [SIMULATION]','warn',1200);
      setTimeout(revealPrank,2600);
    },3900);
  }

  function revealPrank(){
    if(revealed) return; revealed=true; document.body.classList.remove('shake');
    reveal.classList.remove('hidden');
    $('#nexusFinal').textContent='';
    setTimeout(()=>$('#nexusFinal').textContent='[NEXUS] Honestly... I think you were the easiest target today. 😂',1400);
    beep(180,.15); setTimeout(()=>beep(520,.1),180); setTimeout(()=>beep(760,.12),360);
  }

  function executeCommand(cmd){
    const c=cmd.trim().toLowerCase(); if(!c) return;
    addLine(`> ${cmd}`,'info');
    const replies={
      'whoami':['You are... apparently very curious.','[NEXUS] Operator identity: HUMAN [SIMULATED]'],
      'sudo coffee':['[NEXUS] Coffee level critically low.','Human operator required. ☕'],
      'hack nasa':['NEXUS: Absolutely not. 😂','SIMULATION MODE ONLY.'],
      'help':['Available simulation commands: whoami · sudo coffee · hack nasa · status · clear'],
      'status':['SYSTEM STATUS: SIMULATION','REAL SYSTEM ACCESS: NONE','NETWORK ACCESS: NONE','PRANK ENGINE: READY'],
      'clear':[]
    };
    if(c==='clear'){terminal.innerHTML='';return;}
    (replies[c]||['Unknown simulation command. Type "help".']).forEach((x,i)=>addLine(x,c==='hack nasa'?'warn':'ai',300+i*300));
  }

  input.addEventListener('keydown',e=>{if(e.key==='Enter'){executeCommand(input.value);input.value='';}});
  $('#pauseBtn').onclick=()=>{paused=!paused;$('#pauseBtn').textContent=paused?'RESUME':'PAUSE';$('#terminalState').textContent=paused?'PAUSED':'STREAMING';};
  $('#soundBtn').onclick=()=>{soundOn=!soundOn;$('#soundBtn').textContent=`SOUND: ${soundOn?'ON':'OFF'}`;};
  $('#fullscreenBtn').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.();};
  $('#exitBtn').onclick=()=>location.href='about:blank';
  $('#closeReveal').onclick=()=>location.href='about:blank';
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(!reveal.classList.contains('hidden')) location.href='about:blank'; else location.href='about:blank';}});

  setInterval(()=>{
    const sec=Math.floor((Date.now()-started)/1000), h=String(Math.floor(sec/3600)).padStart(2,'0'),m=String(Math.floor(sec/60)%60).padStart(2,'0'),s=String(sec%60).padStart(2,'0');$('#clock').textContent=`${h}:${m}:${s}`;
    $('#cpu').textContent=`${35+Math.floor(Math.random()*35)}%`;$('#mem').textContent=`${52+Math.floor(Math.random()*25)}%`;
    ['p1','p2','p3'].forEach((id,i)=>{const v=55+Math.floor(Math.random()*45);$('#'+id).textContent=v+'%';$('#'+id+'bar').style.width=v+'%';});
  },1200);

  // Canvas network visualization: all nodes are fictional and local.
  const canvas=$('#mapCanvas'), ctx=canvas.getContext('2d');
  const nodes=Array.from({length:18},(_,i)=>({x:40+Math.random()*680,y:25+Math.random()*250,r:2+Math.random()*2,phase:Math.random()*6.28,red:i===7||i===13}));
  function drawMap(){
    const dpr=window.devicePixelRatio||1, rect=canvas.getBoundingClientRect();
    if(canvas.width!==Math.floor(rect.width*dpr)){canvas.width=Math.floor(rect.width*dpr);canvas.height=Math.floor(rect.height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);}
    const w=rect.width,h=rect.height;ctx.clearRect(0,0,w,h);
    nodes.forEach((a,i)=>{nodes.slice(i+1).forEach(b=>{const dx=a.x-b.x,dy=a.y-b.y,dist=Math.hypot(dx,dy);if(dist<210){ctx.strokeStyle='rgba(67,230,255,.10)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(a.x/760*w,a.y/310*h);ctx.lineTo(b.x/760*w,b.y/310*h);ctx.stroke();}})});
    const t=performance.now()/700;nodes.forEach(n=>{const x=n.x/760*w,y=n.y/310*h,p=(Math.sin(t+n.phase)+1)/2;ctx.beginPath();ctx.arc(x,y, n.r+2*p,0,Math.PI*2);ctx.fillStyle=n.red?'rgba(255,73,104,.9)':'rgba(67,230,255,.9)';ctx.shadowBlur=10;ctx.shadowColor=n.red?'#ff4968':'#43e6ff';ctx.fill();ctx.shadowBlur=0;});
    requestAnimationFrame(drawMap);
  }
  drawMap();
  bootSequence();
})();

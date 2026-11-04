import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
const dir=path.join(root,'2026-2027/vjezbe/class2/bpmn-class2');
const manifest=JSON.parse(await fs.readFile(path.join(dir,'manifest.json'),'utf8'));
const browser=await chromium.launch({headless:true,...(process.env.BPMN_BROWSER ? {executablePath:process.env.BPMN_BROWSER} : {})});
const page=await browser.newPage({viewport:{width:1600,height:1000},deviceScaleFactor:2});
await page.setContent('<html><head><meta charset="utf-8"></head><body style="margin:0;background:white"><div id="canvas" style="width:1600px;height:1000px"></div></body></html>');
await page.addScriptTag({path:path.join(here,'node_modules/bpmn-js/dist/bpmn-viewer.development.js')});

let failures=[];
for(const item of manifest){
 await page.evaluate(fontSize=>{window.viewer?.destroy();window.viewer=new BpmnJS({container:'#canvas',textRenderer:{defaultStyle:{fontFamily:'DejaVu Sans',fontSize},externalStyle:{fontFamily:'DejaVu Sans',fontSize:fontSize-2}}});},item.fontSize??16);
 const xml=await fs.readFile(path.join(dir,item.name+'.bpmn'),'utf8');
 const result=await page.evaluate(async xml=>{
   const {warnings}=await viewer.importXML(xml);
   const {svg}=await viewer.saveSVG();
   return {svg,warnings:warnings.map(w=>w.message)};
 },xml);
 if(result.warnings.length)failures.push({name:item.name,warnings:result.warnings});
 await fs.writeFile(path.join(dir,item.name+'.svg'),result.svg);
 // Render the exported SVG, independent of canvas chrome or viewport zoom.
 const shot=await browser.newPage({deviceScaleFactor:2});
 await shot.setContent('<html><body style="margin:0;background:#fff">'+result.svg+'</body></html>');
 await shot.locator('svg').screenshot({path:path.join(dir,item.name+'.png')});
 await shot.close();
 console.log(item.name, result.warnings.length ? result.warnings : 'OK');
}
// Coloured sequence flows show successive states of one process instance.
const views=[
 {name:'43-exercise-preparation',source:'28-exit-preparation',title:'Припрема испоруке: дио којем треба додати рок',bounds:[100,25,550,330],keep:['Fork','Budget','Stock','Join'],flowSources:['Start','Fork','Budget','Stock','Join']},
 {name:'41-exercise-checks',source:'17-base-overview',title:'Дио рјешења A који проширујемо',bounds:[650,20,475,390],keep:['Fork','Budget','Stock','Join'],flowSources:['Merge','Fork','Budget','Stock','Join']},
 {name:'42-exercise-error',source:'11-error-scope',title:'Провјере након додавања обраде грешке',bounds:[100,20,1010,550],keep:['Sub','InnerStart','Fork','Budget','Code','Stock','Valid','Join','InnerEnd','Error','Catch','Notify','InvalidEnd','Next'],flowSources:['Sub','InnerStart','Fork','Budget','Code','Valid','Stock','Join','Catch','Notify']},
 {name:'29-and-running',source:'34-and-execution',title:'Обје провјере раде',
  activeEdges:['Fork:Budget','Fork:Stock'],activeNodes:['Budget','Stock'],futureEdges:['Join:Next','Next:End'],futureNodes:['Next'],statuses:[['Budget','У току'],['Stock','У току'],['Next','Није почело']]},
 {name:'30-and-waiting',source:'34-and-execution',title:'Буџет је провјерен, чека се доступност',
  doneEdges:['Fork:Budget','Budget:Join'],doneNodes:['Budget'],activeEdges:['Fork:Stock'],activeNodes:['Stock'],waitingNodes:['Join'],futureEdges:['Join:Next','Next:End'],futureNodes:['Next'],joinLabel:['Чека','доступност'],statuses:[['Budget','Завршено'],['Stock','У току'],['Next','Није почело']]},
 {name:'35-and-joined',source:'34-and-execution',title:'Обје провјере су завршене, процес наставља',
  doneEdges:['Fork:Budget','Fork:Stock','Budget:Join','Stock:Join'],doneNodes:['Budget','Stock','Join'],activeEdges:['Join:Next'],activeNodes:['Next'],futureEdges:['Next:End'],joinLabel:['Обје','завршене'],statuses:[['Budget','Завршено'],['Stock','Завршено'],['Next','У току']]},
 {name:'31-boundary-detail',source:'19-shared-deadline-solution',title:'Три догађаја на граници потпроцеса',bounds:[55,380,710,200],keep:['Sub','Catch','Reminder','Deadline'],flowSources:['Catch','Reminder','Deadline']}
];
for(const view of views){
 const original=await fs.readFile(path.join(dir,view.source+'.svg'),'utf8');
 const xml=await fs.readFile(path.join(dir,view.source+'.bpmn'),'utf8');
 const svg=await page.evaluate(({original,xml,view})=>{
  const doc=new DOMParser().parseFromString(original,'image/svg+xml'),root=doc.documentElement;
  if(view.keep){
   const ids=new Set(view.keep);
   const model=new DOMParser().parseFromString(xml,'text/xml');
   for(const f of model.getElementsByTagNameNS('http://www.omg.org/spec/BPMN/20100524/MODEL','sequenceFlow')){
    if(view.flowSources.includes(f.getAttribute('sourceRef')))ids.add(f.id||f.getAttribute('id'));
   }
   for(const g of [...root.querySelectorAll('g[data-element-id]')]){
    const id=g.getAttribute('data-element-id');
    if(!ids.has(id)&&!ids.has(id.replace(/_label$/,'')))g.remove();
   }
  }
  if(view.bounds){const [x,y,w,h]=view.bounds;root.setAttribute('viewBox',`${x} ${y} ${w} ${h}`);root.setAttribute('width',w);root.setAttribute('height',h);}
  const model=new DOMParser().parseFromString(xml,'text/xml');
  const flowIds=new Map([...model.getElementsByTagNameNS('http://www.omg.org/spec/BPMN/20100524/MODEL','sequenceFlow')].map(f=>[f.getAttribute('sourceRef')+':'+f.getAttribute('targetRef'),f.getAttribute('id')]));
  const group=id=>[...root.querySelectorAll('g[data-element-id]')].find(g=>g.getAttribute('data-element-id')===id);
  const palette={active:['#1565a9','#e6f1fb'],done:['#8a94a3','#ffffff'],waiting:['#8a94a3','#ffffff'],future:['#8a94a3','#ffffff']};
  if(view.statuses){
   for(const g of root.querySelectorAll('g.djs-connection')){
    for(const path of g.querySelectorAll('.djs-visual > path')){path.style.stroke='#8a94a3';path.style.strokeWidth='2px';}
    for(const path of g.querySelectorAll('marker path')){path.style.fill='#8a94a3';path.style.stroke='#8a94a3';}
   }
   for(const g of root.querySelectorAll('g.djs-shape')){
    const visual=g.querySelector('.djs-visual');
    const shape=visual?.querySelector(':scope > rect,:scope > polygon,:scope > circle')??visual?.querySelector(':scope > path');
    if(shape){shape.style.stroke='#8a94a3';shape.style.fill='white';}
   }
  }

  for(const [state,[stroke,fill]] of Object.entries(palette)){
   for(const key of view[state+'Edges']??[]){
    const g=group(flowIds.get(key));
    if(!g)throw new Error('Missing flow: '+key);
    for(const path of g.querySelectorAll('.djs-visual > path')){path.style.stroke=stroke;path.style.strokeWidth=state==='active'?'4px':'2px';}
    for(const path of g.querySelectorAll('marker path')){path.style.fill=stroke;path.style.stroke=stroke;}
   }
   for(const id of view[state+'Nodes']??[]){
    const visual=group(id)?.querySelector('.djs-visual');
    const shape=visual?.querySelector(':scope > rect,:scope > polygon,:scope > circle')??visual?.querySelector(':scope > path');
    if(!shape)throw new Error('Missing shape: '+id);
    shape.style.stroke=stroke;shape.style.fill=fill;shape.style.strokeWidth='3px';
   }
  }
  if(view.statuses){
   const [x,y,w,h]=root.getAttribute('viewBox').split(/\s+/).map(Number);
   root.setAttribute('viewBox',`${x} 10 ${w} ${y+h-10}`);root.setAttribute('height',y+h-10);
   const positions={Budget:[362.5,30],Stock:[362.5,240],Next:[780,127]};
   for(const [id,text] of view.statuses){
    const label=doc.createElementNS('http://www.w3.org/2000/svg','text');
    const [lx,ly]=positions[id];
    for(const [k,v] of Object.entries({x:lx,y:ly,fill:text==='У току'?palette.active[0]:'#4b5563','font-size':16,'font-family':'DejaVu Sans','text-anchor':'middle'}))label.setAttribute(k,v);
    label.textContent=text;root.appendChild(label);
   }
  }
  if(view.joinLabel){
   const label=doc.createElementNS('http://www.w3.org/2000/svg','text');
   for(const [k,v] of Object.entries({x:625,y:235,fill:'#4b5563','font-size':14,'font-family':'DejaVu Sans'}))label.setAttribute(k,v);
   const top=doc.createElementNS('http://www.w3.org/2000/svg','tspan');top.textContent=view.joinLabel[0];label.appendChild(top);
   const bottom=doc.createElementNS('http://www.w3.org/2000/svg','tspan');bottom.setAttribute('x',625);bottom.setAttribute('dy',18);bottom.textContent=view.joinLabel[1];label.appendChild(bottom);root.appendChild(label);
  }
  return new XMLSerializer().serializeToString(doc);
 },{original,xml,view});
 await fs.writeFile(path.join(dir,view.name+'.svg'),svg);
 const shot=await browser.newPage({deviceScaleFactor:2});
 await shot.setContent('<html><body style="margin:0;background:white">'+svg+'</body></html>');
 await shot.locator('svg').screenshot({path:path.join(dir,view.name+'.png')});await shot.close();
 console.log(view.name,'view OK');
}
await fs.writeFile(path.join(dir,'views.json'),JSON.stringify(views,null,2)+'\n');
const cataloguePath=path.join(dir,'README.md');
let catalogue=(await fs.readFile(cataloguePath,'utf8')).split('\n<!-- derived views -->')[0];
catalogue+='\n<!-- derived views -->\n## Tok izvršavanja i uvećani detalji\n\nPlavo označava samo rad koji sada traje. Završene aktivnosti, čekanje i posao koji još nije počeo označeni su riječima. Ostale strelice su neutralne. Boje služe objašnjenju i nisu dio BPMN notacije.\nPrikaz granice je izrez modela B; izlazni tokovi nastavljaju van izreza.\n\n';
for(const v of views)catalogue+=`### ${v.title}\n\n![${v.title}](${v.name}.png)\n\n[SVG](${v.name}.svg) · [Izvorni model](${v.source}.bpmn)\n\n`;
await fs.writeFile(cataloguePath,catalogue.trimEnd()+'\n');
await browser.close();
await fs.writeFile(path.join(dir,'validation.json'),JSON.stringify({renderer:'bpmn-js 18.31.1',models:manifest.length,importWarnings:failures},null,2)+'\n');
if(failures.length)process.exitCode=1;

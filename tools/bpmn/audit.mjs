import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const dir=path.join(root,'2026-2027/vjezbe/class2/bpmn-class2');
const manifest=JSON.parse(await fs.readFile(path.join(dir,'manifest.json')));
const browser=await chromium.launch({headless:true,...(process.env.BPMN_BROWSER?{executablePath:process.env.BPMN_BROWSER}:{})});
const page=await browser.newPage({viewport:{width:1600,height:1000}});
await fs.writeFile('/tmp/upp-bpmn-contact.html','<html><body style="margin:0;padding:20px;font:16px sans-serif;background:#e8eaed"><main style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+manifest.map(m=>`<article style="background:white;padding:12px"><h3>${m.name}</h3><img style="width:100%;height:340px;object-fit:contain" src="file://${dir}/${m.name}.png"></article>`).join('')+'</main></body></html>');
await page.goto('file:///tmp/upp-bpmn-contact.html');
await page.screenshot({path:'/tmp/upp-bpmn-contact.png',fullPage:true});
// HTML QA: all deck images must load and fit inside their visible slide.
await page.goto('file://'+root+'/2026-2027/vjezbe/class2/class2.html');
await page.waitForFunction(()=>window.Reveal?.isReady(),null,{timeout:30000});
await page.evaluate(()=>Reveal.configure({transition:'none'}));
let checks=[];
const slideCount=await page.evaluate(()=>Reveal.getTotalSlides());
for(let i=1;i<slideCount;i++){
 await page.evaluate(i=>Reveal.slide(i),i);
 await page.waitForFunction(()=>{const imgs=[...document.querySelectorAll('.present img')];return imgs.every(im=>im.complete&&im.naturalWidth>0);},null,{timeout:10000});
 const data=await page.evaluate(()=>{
  const s=Reveal.getCurrentSlide(),r=s.getBoundingClientRect();
  const title=s.querySelector('h2')?.textContent,imgs=[...s.querySelectorAll('img')];
  return {title,imageCount:imgs.length,imageLoaded:imgs.length?imgs.every(im=>im.naturalWidth>0):title==='Провјерите свој модел',overflow:s.scrollHeight>s.clientHeight+3,offscreen:[...s.children].some(c=>c.getBoundingClientRect().bottom>innerHeight+2),height:r.height};
 });checks.push(data);
 if([1,3,4,5,7,9,18,19,23,24].includes(i))await page.screenshot({path:`/tmp/upp-html-slide-${i}.png`});
}
await fs.writeFile('/tmp/upp-html-audit.json',JSON.stringify(checks,null,2));
console.log(JSON.stringify({slides:checks.length,problems:checks.filter(c=>!c.imageLoaded||c.overflow||c.offscreen)},null,2));
await browser.close();

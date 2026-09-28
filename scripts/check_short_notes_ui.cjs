const {chromium}=require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{const browser=await chromium.launch({headless:true,channel:'msedge'});try{
const page=await browser.newPage({viewport:{width:1440,height:1050}}); page.setDefaultTimeout(20000);
const errors=[];page.on('pageerror',error=>errors.push(error.message));
await page.route('**/api/practice',route=>route.fulfill({path:'public/practice-question-bank.json',contentType:'application/json'}));
let submitted; let fail=true;let saved=[];
await page.route('**/api/short-notes/reviews',async route=>{
 if(route.request().method()==='GET')return route.fulfill({json:{reviews:saved}});
 submitted=route.request().postDataJSON();
 if(fail)return route.fulfill({status:502,json:{message:'Temporary AI error. Please retry.'}});
 const review={questionId:submitted.questionId,answer:submitted.answer,hasImage:!!submitted.answerImageDataUrl,score:8,feedback:'A well-organised response. Add a little more detail to cover the whole question.',strengths:['Clear structure'],improvements:['Cover all requested points'],modelAnswerSections:[{label:'A',heading:'Model answer',points:['A structured explanation covering the source prompt.','Relevant supporting details and a labelled diagram where requested.']}],submittedAt:new Date().toISOString()};saved=[review];return route.fulfill({status:201,json:{review}});
});
await page.goto('http://127.0.0.1:4173',{waitUntil:'domcontentloaded',timeout:60000});await page.getByRole('button',{name:'Explore as guest'}).click();
// Stub authentication and reviews only; do not create or modify real accounts.
await page.evaluate(()=>localStorage.setItem('medicomm-session-token','short-notes-ui-test'));
async function openSubject(subject){await page.locator('.shell-nav').getByRole('button',{name:'Practice',exact:true}).click();await page.locator('.practice-path-card').filter({hasText:'THEORY'}).click();await page.locator('.practice-subject-card').filter({has:page.locator('.practice-subject-label',{hasText:new RegExp('^'+subject+'$')})}).click();await page.getByRole('button',{name:/NOTE.*Short Notes/}).click();}
await openSubject('Anatomy');await page.locator('.sn-topic-card').first().waitFor();assert.equal(await page.locator('.sn-topic-card').count(),10);
await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => { window.scrollTo(0,0); requestAnimationFrame(resolve); })));await page.screenshot({animations:'disabled',path:'output/short-notes/topics-desktop.png',fullPage:true});
await page.getByRole('textbox',{name:'Search topics or questions'}).fill('brachial');assert.equal(await page.locator('.sn-topic-card').count(),1);await page.getByRole('button',{name:'Clear search'}).click();
await page.locator('.sn-topic-card').filter({hasText:'Head, Neck & Face'}).click();assert.equal(await page.locator('.sn-question-row').count(),26);
await page.getByRole('button',{name:'Long answers',exact:true}).click();assert.equal(await page.locator('.sn-question-row').count(),9);
await page.getByRole('button',{name:'Short notes',exact:true}).click();assert.equal(await page.locator('.sn-question-row').count(),17);
await page.getByRole('button',{name:'All questions',exact:true}).click();await page.getByRole('button',{name:'Starred in source',exact:true}).click();assert((await page.locator('.sn-question-row').count())<26);await page.getByRole('button',{name:'Starred in source',exact:true}).click();
await page.getByRole('textbox',{name:'Search questions'}).fill('impossible-keyword');await page.getByRole('heading',{name:'No matching questions'}).waitFor();await page.getByRole('button',{name:'Reset filters'}).click();
await page.evaluate(()=>document.documentElement.dataset.theme='dark');await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => { window.scrollTo(0,0); requestAnimationFrame(resolve); })));await page.screenshot({animations:'disabled',path:'output/short-notes/questions-dark.png',fullPage:true});
const rect=await page.locator('.sn-question-row').first().boundingBox();assert(rect.width>rect.height*3);
await page.locator('.sn-question-row').first().click();
const answer=page.getByRole('textbox',{name:'Your theory answer'});await answer.fill('My draft with headings and a structured explanation.');
await page.getByRole('button',{name:'Back to questions'}).click();await page.locator('.sn-question-row').first().click();assert.equal(await answer.inputValue(),'My draft with headings and a structured explanation.');
await page.locator('input[type=file][accept="image/jpeg,image/png,image/webp,image/heic,image/heif"]').setInputFiles('output/short-notes/source-page-1.png');await page.getByAltText('Your handwritten answer').waitFor();await page.getByRole('button',{name:'Remove photo'}).click();
await page.evaluate(()=>document.documentElement.dataset.theme='light');await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => { window.scrollTo(0,0); requestAnimationFrame(resolve); })));await page.screenshot({animations:'disabled',path:'output/short-notes/answer-desktop.png',fullPage:true});
await page.getByRole('checkbox').check();await page.getByRole('button',{name:'Submit for AI review'}).click();await page.getByRole('alert').filter({hasText:'Temporary AI error'}).waitFor();assert((await answer.inputValue()).includes('My draft'));
fail=false;await page.getByRole('button',{name:'Submit for AI review'}).click();await page.getByRole('heading',{name:'Exam-ready model answer'}).waitFor();assert.equal(submitted.privacyAccepted,true);assert.equal(submitted.questionId,'bhalani-anatomy-head-neck-face-001');await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => { window.scrollTo(0,0); requestAnimationFrame(resolve); })));await page.screenshot({animations:'disabled',path:'output/short-notes/review-desktop.png',fullPage:true});
await page.getByRole('button',{name:'Practise again'}).click();
await page.getByRole('textbox',{name:'Your theory answer'}).fill('A new attempt that must survive leaving this subject.');
await openSubject('Anatomy');await page.locator('.sn-topic-card').filter({hasText:'Head, Neck & Face'}).click();
await page.locator('.sn-question-row').first().click();
assert.equal(await page.getByRole('textbox',{name:'Your theory answer'}).inputValue(),'A new attempt that must survive leaving this subject.');
await page.getByRole('button',{name:'Back to questions'}).click();assert.equal(await page.locator('.sn-question-row.is-reviewed').count(),1);
await page.setViewportSize({width:390,height:844});await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => { window.scrollTo(0,0); requestAnimationFrame(resolve); })));await page.screenshot({animations:'disabled',path:'output/short-notes/questions-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
await page.locator('.sn-question-row').nth(1).click();await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => { window.scrollTo(0,0); requestAnimationFrame(resolve); })));await page.screenshot({animations:'disabled',path:'output/short-notes/answer-mobile.png',fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
await page.setViewportSize({width:1440,height:1050});
await openSubject('Physiology');await page.locator('.sn-topic-card').first().waitFor();assert.equal(await page.locator('.sn-topic-card').count(),11);
await openSubject('Biochemistry');await page.locator('.sn-topic-card').first().waitFor();assert.equal(await page.locator('.sn-topic-card').count(),27);
for (const [subject, count] of [['Pathology',30],['Pharmacology',60],['Microbiology',29],['Forensic Medicine',29]]) {
 await openSubject(subject);await page.locator('.sn-topic-card').first().waitFor();
 assert.equal(await page.locator('.sn-topic-card').count(),count);
 await page.locator('.sn-topic-card').first().click();await page.locator('.sn-question-row').first().click();
 assert((await page.locator('.sn-source').innerText()).includes('Bhalani II Year Final-1'));
}
for (const [subject, count, search] of [['Community Medicine',67,'Eugenics'],['Ophthalmology',19,'Diabetic Retinopathy'],['ENT',47,'Bithermal']]) {
 await openSubject(subject);await page.locator('.sn-topic-card').first().waitFor();
 assert.equal(await page.locator('.sn-topic-card').count(),count);
 await page.getByRole('textbox',{name:'Search topics or questions'}).fill(search);
 assert.equal(await page.locator('.sn-topic-card').count(),1);
 await page.locator('.sn-topic-card').first().click();
 await page.locator('.sn-question-row').filter({hasText:search}).click();
 assert((await page.locator('.sn-source').innerText()).includes('Bhalani III year'));
 await page.setViewportSize({width:390,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({animations:'disabled',path:`output/short-notes-third-year/${subject.toLowerCase().replaceAll(' ','-')}-mobile.png`,fullPage:true});
 await page.setViewportSize({width:1440,height:1050});
}
for (const [subject, count, search] of [['General Medicine',28,'Anaphylactic Shock'],['General Surgery',57,'Crush Syndrome'],['Orthopedics',39,'Thomas Splint'],['Obstetrics and Gynaecology',63,'Caput Succedaneum'],['Pediatrics',24,'Microcephaly']]) {
 await openSubject(subject);await page.locator('.sn-topic-card').first().waitFor();
 assert.equal(await page.locator('.sn-topic-card').count(),count);
 await page.getByRole('textbox',{name:'Search topics or questions'}).fill(search);
 assert.equal(await page.locator('.sn-topic-card').count(),1);
 await page.locator('.sn-topic-card').first().click();
 await page.locator('.sn-question-row').filter({hasText:search}).click();
 assert((await page.locator('.sn-source').innerText()).includes('Bhalani Final Year'));
 await page.setViewportSize({width:390,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({animations:'disabled',path:`output/short-notes-final-year/${subject.toLowerCase().replaceAll(' ','-')}-mobile.png`,fullPage:true});
 await page.setViewportSize({width:1440,height:1050});
}
assert.deepEqual(errors,[]);console.log('PASS: all fifteen subjects; topic counts; search and filters; draft recovery; upload; review failure/retry/success; progress; desktop/mobile; source labels across all four Bhalani imports. AI responses stubbed.');
}finally{await browser.close();}})().catch(error=>{console.error(error);process.exit(1)});

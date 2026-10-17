// Real API + browser verification using isolated accounts and persistence.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { once } = require('node:events');
const assert = require('node:assert/strict');

(async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'medulla-fmge-tests-'));
  const { issueSession } = await import('../server/security.mjs');
  const { preview } = await import('vite');
  const seed = { users: [{ id: 'fmge-ui-paid', name: 'FMGE Learner', email: 'fmge-ui@example.test', medicalCollege: 'Test College' }], sessions: {}, paymentOrders: [{ orderId: 'fmge_fixture', userId: 'fmge-ui-paid', status: 'paid', paymentId: 'pay_fixture', verifiedAt: new Date().toISOString() }] };
  const token = issueSession(seed, 'fmge-ui-paid');
  await fs.writeFile(path.join(root,'users.json'),JSON.stringify(seed));
  let frontend, child, browser, backend;
  async function startBackend(origin) {
    child = spawn(process.execPath,['server.mjs'],{env:{...process.env,NODE_ENV:'test',LOAD_ENV_FILES:'false',RUNTIME_DATA_DIR:root,PORT:'0',HOST:'127.0.0.1',SUPABASE_URL:'',SUPABASE_SECRET_KEY:'',SUPABASE_SERVICE_ROLE_KEY:'',SUPABASE_SERVICE_KEY:'',SUPABASE_UPLOAD_BUCKET:'',APP_ORIGINS:origin},stdio:['ignore','pipe','pipe']});
    return new Promise((resolve,reject)=>{
      let output='';const timer=setTimeout(()=>reject(new Error(output || 'Backend startup timed out')),60000);
      child.on('error',reject);child.on('exit',code=>{clearTimeout(timer);reject(new Error(`Backend exited ${code}: ${output}`));});
      child.stderr.on('data',c=>output+=c);
      child.stdout.on('data',c=>{output+=c;const match=output.match(/listening on http:\/\/127.0.0.1:(\d+)/);if(match){clearTimeout(timer);resolve(`http://127.0.0.1:${match[1]}`);}});
    });
  }
  try {
    const origin='http://127.0.0.1:4196';
    backend=await startBackend(origin);
    frontend=await preview({build:{outDir:'.tmp/fmge-tests-build'},preview:{host:'127.0.0.1',port:4196,strictPort:true,proxy:{'/api':backend,'/uploads':backend}}});
    console.log('Isolated servers ready:',origin,backend);
    browser=await chromium.launch({headless:true,channel:'msedge'});
    console.log('Browser launched');
    const context=await browser.newContext({viewport:{width:1440,height:1000}});
    await context.addCookies([{name:'medicomm_session',value:token,url:origin,httpOnly:true,sameSite:'Lax'}]);
    const page=await context.newPage();page.setDefaultTimeout(45000);
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    let failSave=false;
    await page.route('**/api/**',async route=>{
      if(failSave && route.request().method()==='PATCH' && route.request().url().includes('/fmge-tests/')){failSave=false;return route.abort();}
      try { await route.continue(); } catch { /* The page may close during a background request. */ }
    });
    const openTests=async()=>{
      await page.locator('.shell-nav').getByRole('button',{name:'Practice',exact:true}).click();
      await page.getByRole('button',{name:/FMGE Tests/}).click();
      await page.locator('.ft-test-card').first().waitFor();
    };
    await page.goto(origin,{waitUntil:'domcontentloaded'});console.log('Frontend loaded');await openTests();console.log('Test catalog loaded');
    assert.equal(await page.locator('.ft-test-card').count(),3);
    await fs.mkdir('output/fmge-tests-ui',{recursive:true});
    await page.evaluate(()=>{document.documentElement.dataset.theme='dark';window.scrollTo(0,0);});
    await page.screenshot({path:'output/fmge-tests-ui/catalog-dark.png',fullPage:true});
    await page.getByRole('tab',{name:'Grand Tests',exact:true}).click();
    await page.getByRole('heading',{name:'GRAND TEST 1'}).waitFor();
    await page.getByRole('tab',{name:'Practice Tests',exact:true}).click();
    await page.locator('.ft-test-card').first().getByRole('button',{name:'Start test'}).click();
    await page.getByRole('button',{name:'Start Part 1',exact:true}).click();
    await page.locator('.ft-options').waitFor();
    await page.locator('.ft-option').first().click();
    await page.waitForFunction(()=>document.querySelector('.ft-option')?.getAttribute('aria-pressed')==='true');
    await page.getByRole('button',{name:'Mark for review',exact:true}).click();
    await page.getByRole('button',{name:'Marked for review',exact:true}).waitFor();
    await page.getByRole('button',{name:'Next question',exact:true}).click();
    await page.getByText('QUESTION 2 / 300',{exact:true}).waitFor();
    failSave=true;
    await page.locator('.ft-option').first().click();
    await page.getByRole('alert').waitFor();
    await page.getByRole('button',{name:'Reload saved attempt'}).click();
    await page.waitForFunction(()=>!document.querySelector('.ft-error') && !document.querySelector('.ft-option')?.disabled);
    assert.equal(await page.locator('.ft-option[aria-pressed="true"]').count(),0);
    await page.getByRole('button',{name:'Previous',exact:true}).click();
    await page.getByText('QUESTION 1 / 300',{exact:true}).waitFor();
    assert.equal(await page.locator('.ft-option[aria-pressed="true"]').count(),1);
    await page.screenshot({path:'output/fmge-tests-ui/attempt-dark.png',fullPage:true});
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>{document.documentElement.dataset.theme='light';window.scrollTo(0,0);});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.screenshot({path:'output/fmge-tests-ui/attempt-mobile.png',fullPage:true});
    await page.setViewportSize({width:1440,height:1000});
    // Restart the backend to prove attempts survive real persistence/reload.
    child.kill();await once(child,'exit');
    frontend.httpServer.closeAllConnections();await new Promise(resolve=>frontend.httpServer.close(resolve));
    backend=await startBackend(origin);
    frontend=await preview({build:{outDir:'.tmp/fmge-tests-build'},preview:{host:'127.0.0.1',port:4196,strictPort:true,proxy:{'/api':backend,'/uploads':backend}}});
    await page.reload();await openTests();
    await page.locator('.ft-test-card').first().getByRole('button',{name:'Resume',exact:true}).click();
    await page.getByRole('button',{name:'Marked for review',exact:true}).waitFor();
    assert.equal(await page.locator('.ft-option[aria-pressed="true"]').count(),1);
    await page.getByRole('button',{name:'Submit Part 1',exact:true}).click();
    await page.getByRole('dialog').getByRole('button',{name:'Submit Part 1',exact:true}).click();
    await page.getByRole('button',{name:'Start Part 2',exact:true}).click();
    await page.getByText('QUESTION 151 / 300',{exact:true}).waitFor();
    await page.getByRole('button',{name:'Submit Part 2',exact:true}).click();
    await page.getByRole('dialog').getByRole('button',{name:'Submit Part 2',exact:true}).click();
    await page.getByRole('heading',{name:'Your subject breakdown'}).waitFor();
    assert.equal(await page.locator('.ft-subject-results > div').count(),20);
    assert.equal(await page.locator('.ft-review-item').count(),300);
    await page.locator('.ft-review-item summary').first().click();
    await page.locator('.ft-explanation').first().waitFor({state:'visible'});
    await page.screenshot({path:'output/fmge-tests-ui/results-light.png',fullPage:true});
    assert.deepEqual(errors,[]);
    const persisted=JSON.parse(await fs.readFile(path.join(root,'users.json'),'utf8'));
    assert.equal(persisted.fmgeTestAttempts[0].status,'completed');
    assert.equal(Object.keys(persisted.fmgeTestAttempts[0].answers).length,1);
    console.log('PASS: real API start/save/mark/navigation, failed-save recovery, backend restart/resume, both submissions, scoring/review, tabs, and mobile layout.');
  } catch(error) { console.error('Browser check failed:',error); throw error; } finally {
    if(browser)await browser.close();
    if(child?.exitCode===null){child.kill();await once(child,'exit');}
    if(frontend){frontend.httpServer.closeAllConnections();await new Promise(resolve=>frontend.httpServer.close(resolve));}
    const resolved=path.resolve(root);
    if(!resolved.startsWith(path.resolve(os.tmpdir())+path.sep)||!path.basename(resolved).startsWith('medulla-fmge-tests-'))throw new Error('Unexpected cleanup path');
    await fs.rm(resolved,{recursive:true,force:true});
  }
})().catch(e=>{console.error(e);process.exitCode=1;});

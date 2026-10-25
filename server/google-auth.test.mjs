import test from 'node:test';
import assert from 'node:assert/strict';
import { createGoogleAuth } from './googleAuth.mjs';
import { publicGoogleConfig, discoverGoogleConfig } from './googleConfig.mjs';

const now = Date.parse('2026-10-26T06:00:00Z');
const token = 'synthetic-id-token-only-for-tests';
const request = { headers: {} };
function fixture(users = []) {
  let database = { users: structuredClone(users), sessions: {}, paymentOrders: [], emailChallenges: [] };
  const claims = { uid: 'google-uid', email: 'person@example.com', email_verified: true,
    auth_time: now / 1000, firebase: { sign_in_provider: 'google.com' } };
  const identity = { email: claims.email, emailVerified: true, displayName: 'Test Learner',
    providerData: [{ providerId: 'google.com', email: claims.email }] };
  let revoked = false, passwordCalls = 0;
  const signIn = createGoogleAuth({
    auth: { async verifyIdToken(value, checkRevoked) { assert.equal(value,token);assert.equal(checkRevoked,true);if(revoked)throw new Error('revoked');return claims; }, async getUser() { return identity; } },
    readDatabase: () => structuredClone(database), writeDatabase: async value => { database = structuredClone(value); },
    verifyPassword: async password => { passwordCalls++;return password === 'original-password'; },
    createUser: (db, profile) => ({id:'new-user',email:profile.email,name:profile.name}), now: () => now,
  });
  return { signIn, claims, identity, state:()=>database, revoke:()=>{revoked=true;}, passwordCalls:()=>passwordCalls };
}
const old = { id:'existing-id',email:'person@example.com',name:'Original name',passwordHash:'original-hash',passwordSalt:'salt',
  plan:'premium',subscriptionOrderId:'paid-order',attemptedQuestions:42,questionBookmarks:['q1'],tokens:{remaining:8} };

test('Google verified-email alone cannot silently link an existing password account', async()=>{
  const f=fixture([old]);
  assert.deepEqual(await f.signIn({idToken:token},request),{linkRequired:true,email:old.email});
  assert.deepEqual(f.state().users,[old]);assert.equal(Object.keys(f.state().sessions).length,0);
  await assert.rejects(f.signIn({idToken:token,linkPassword:'wrong'},request),{status:401});
});
test('one-time linking preserves identity, password, subscription and progress, then allows Google login', async()=>{
  const f=fixture([old]);
  const result=await f.signIn({idToken:token,linkPassword:'original-password'},request);
  for(const [key,value]of Object.entries(old))assert.deepEqual(result.user[key],value,key);
  assert.equal(result.user.googleUid,'google-uid');assert.ok(result.user.emailVerifiedAt);
  assert.equal(result.token.length,64);assert.equal(f.state().users.length,1);
  await f.signIn({idToken:token},request);
  assert.equal(f.passwordCalls(),1);assert.equal(f.state().users.length,1);
});
test('new Google users complete a profile, and the email comes only from the verified token', async()=>{
  const f=fixture();const pending=await f.signIn({idToken:token},request);
  assert.equal(pending.profileRequired,true);assert.equal(f.state().users.length,0);
  const result=await f.signIn({idToken:token,profile:{name:'New learner',email:'attacker@example.com'}},request);
  assert.equal(result.user.email,'person@example.com');assert.equal(result.user.emailVerificationSource,'google');
  assert.equal(result.user.passwordHash,undefined);assert.ok(result.user.emailVerifiedAt);
});
test('unverified, stale, non-Google, disabled and revoked identities never create sessions', async()=>{
  for(const alter of [
    f=>{f.claims.email_verified=false;},f=>{f.claims.firebase.sign_in_provider='password';},
    f=>{f.claims.auth_time-=3600;},f=>{f.identity.disabled=true;},f=>{f.identity.emailVerified=false;},
    f=>{f.identity.email='different@example.com';},f=>f.revoke(),
  ]) {const f=fixture([old]);alter(f);await assert.rejects(f.signIn({idToken:token},request),{status:401});assert.deepEqual(f.state().users,[old]);assert.equal(Object.keys(f.state().sessions).length,0);}
});
test('UID/email conflicts and duplicate accounts are not merged', async()=>{
  const f=fixture([{...old,googleUid:'different-google-uid'}]);
  await assert.rejects(f.signIn({idToken:token,linkPassword:'original-password'},request),{status:409});
  const duplicate=fixture([old,{...old,id:'other'}]);
  await assert.rejects(duplicate.signIn({idToken:token},request),{status:409});
});
test('only public, matching-project web config is returned', async()=>{
  const config={apiKey:'AIza'+'a'.repeat(35),authDomain:'fixture.firebaseapp.com',appId:'1:123:web:abc123',projectId:'fixture',privateKey:'must-not-return'};
  assert.deepEqual(Object.keys(publicGoogleConfig(config,'fixture')).sort(),['apiKey','appId','authDomain','projectId']);
  assert.throws(()=>publicGoogleConfig(config,'other'));
  const firebase={projectId:'fixture',app:{options:{credential:{getAccessToken:async()=>({access_token:'test-access-token'})}}}};
  const discovered=await discoverGoogleConfig(firebase,{},async(url,options)=>{
    assert.equal(options.headers.Authorization,'Bearer test-access-token');
    return {ok:true,json:async()=>url.endsWith('/webApps')?{apps:[{appId:config.appId}]}:config};
  });
  assert.equal(discovered.apiKey,config.apiKey);assert.equal(discovered.privateKey,undefined);
});

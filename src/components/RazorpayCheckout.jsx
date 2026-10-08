import { useEffect, useRef, useState } from 'react';
import { apiRequest } from '../lib/api';
import './checkout.css';

let checkoutScript;
export function loadRazorpayCheckout() {
  if (window.Razorpay) return Promise.resolve();
  if (checkoutScript) return checkoutScript;
  checkoutScript = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    const timer = setTimeout(() => fail(), 20000);
    function fail() { clearTimeout(timer); script.remove(); checkoutScript = null; reject(new Error('Could not load secure checkout. Check your connection and try again.')); }
    script.onload = () => { clearTimeout(timer); if (window.Razorpay) resolve(); else fail(); };
    script.onerror = fail;
    document.head.appendChild(script);
  });
  return checkoutScript;
}

export default function RazorpayCheckout({ plan, user, guest, onVerified }) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [pending, setPending] = useState(null);
  const [coupon, setCoupon] = useState('');
  const [quote, setQuote] = useState(null);
  const [couponMessage, setCouponMessage] = useState('');
  const [couponBusy, setCouponBusy] = useState(false);
  const quoteRequest = useRef(0);
  useEffect(() => { quoteRequest.current++; setQuote(null); setCouponMessage(''); setCouponBusy(false); }, [plan.id]);
  async function applyCoupon(event) {
    event.preventDefault();
    const request = ++quoteRequest.current;
    setCouponBusy(true); setCouponMessage(''); setQuote(null);
    try {
      if (!coupon.trim()) throw new Error('Enter your coupon code first.');
      const result = await apiRequest('/api/payment-quote', { method: 'POST', body: JSON.stringify({ planId: plan.id, coupon }) });
      if (request === quoteRequest.current) { setQuote(result); setCoupon(result.coupon); setCouponMessage('Coupon applied. Your total is now ₹9.'); }
    } catch (error) { if (request === quoteRequest.current) setCouponMessage(error.message); }
    finally { if (request === quoteRequest.current) setCouponBusy(false); }
  }
  const amount = quote?.amount ?? plan.amount;
  const lock = useRef(false);
  const checkout = useRef(null);
  const storageKey = `medulla-payment-verification:${user?.id}`;
  useEffect(() => {
    try { const saved = JSON.parse(sessionStorage.getItem(storageKey) || 'null'); setPending(saved); if (saved) setMessage('A previous payment needs verification. Check its status before paying again.'); } catch { /* No recoverable callback. */ }
    return () => checkout.current?.close();
  }, [storageKey]);
  function remember(value) {
    setPending(value);
    try { if (value) sessionStorage.setItem(storageKey, JSON.stringify(value)); else sessionStorage.removeItem(storageKey); } catch { /* The retry remains available in this tab. */ }
  }
  async function verify(result) {
    setBusy(true); lock.current = true;
    setMessage('Verifying your payment…');
    try {
      const data = await apiRequest('/api/verify-payment', { method: 'POST', body: JSON.stringify(result), timeoutMs: 30000 });
      if (data.paid) { remember(null); onVerified?.(data); setMessage(`${data.test_mode ? 'Test payment' : 'Payment'} confirmed. Practice is unlocked. Reference: ${data.payment_id}.`); }
      else setMessage('Payment authorized; capture is pending. Check payment status again before making another payment.');
    } catch (error) { setMessage(`${error.message} Your payment is not confirmed here. Retry verification before paying again.`); }
    finally { lock.current = false; setBusy(false); }
  }
  async function pay() {
    if (lock.current || pending || guest || couponBusy || user?.hasPracticeAccess) return;
    lock.current = true; setBusy(true); setMessage('Opening secure checkout…');
    try {
      await loadRazorpayCheckout();
      const order = await apiRequest('/api/create-order', { method: 'POST', body: JSON.stringify({ planId: plan.id, amount, currency: plan.currency, coupon: quote?.coupon || '' }), timeoutMs: 30000 });
      let completed = false;
      let failed = false;
      const modal = new window.Razorpay({
        key: order.key_id, order_id: order.order_id, amount: order.amount, currency: order.currency,
        name: 'Medulla', description: `${plan.name} — annual plan`,
        prefill: { name: user?.name, email: user?.email, contact: user?.contactNumber },
        theme: { color: '#2563eb' },
        handler: result => { completed = true; remember(result); void verify(result); },
        modal: { ondismiss: () => { if (!completed) { lock.current = false; setBusy(false); if (!failed) setMessage('Checkout cancelled. No payment was confirmed.'); } } },
      });
      modal.on('payment.failed', event => { failed = true; setMessage(event.error?.description || 'Payment failed. Please retry in checkout or close it.'); });
      checkout.current = modal;
      setMessage(order.test_mode ? 'Test mode: no real money will be collected.' : 'Complete your payment in the secure checkout window.');
      modal.open();
    } catch (error) { lock.current = false; setBusy(false); setMessage(error.message); }
  }
  return <div className="payment-summary">
    <div><span>Selected plan</span><strong>Medulla {plan.name}</strong></div>
    <div><span>Billing</span><strong>Annual · one-time payment</strong></div>
    <form className={`checkout-coupon ${quote ? 'checkout-coupon-applied' : ''}`} onSubmit={applyCoupon}>
      <label htmlFor="checkout-coupon">Have a coupon code?</label>
      <p>A little head start for your preparation.</p>
      <div className="checkout-coupon-input"><input id="checkout-coupon" autoComplete="off" maxLength={40} placeholder="Enter code" value={coupon} disabled={busy || Boolean(pending) || user?.hasPracticeAccess} onChange={event => { quoteRequest.current++; setCouponBusy(false); setCoupon(event.target.value); setQuote(null); setCouponMessage(''); }} /><button type="submit" disabled={busy || couponBusy || Boolean(pending) || user?.hasPracticeAccess}>{couponBusy ? 'Checking…' : quote ? 'Applied ✓' : 'Apply'}</button></div>
      {couponMessage && <p role="status" className="checkout-coupon-feedback">{couponMessage}</p>}
    </form>
    {quote && <div><span>Plan price</span><del>₹{plan.amount / 100}</del></div>}
    {quote && <div className="checkout-savings"><span>PRELAUNCH savings</span><strong>−₹{(plan.amount - amount) / 100}</strong></div>}
    <div className="checkout-total"><span>Total payable</span><strong>{new Intl.NumberFormat('en-IN', { style: 'currency', currency: plan.currency, maximumFractionDigits: 0 }).format(amount / 100)}</strong></div>
    <button className="button button-primary" disabled={busy || couponBusy || guest || Boolean(pending) || user?.hasPracticeAccess} onClick={pay}>{user?.hasPracticeAccess ? 'Practice unlocked ✓' : busy ? 'Processing…' : 'Pay securely with Razorpay'}</button>
    {pending && <button className="button button-secondary" disabled={busy} onClick={() => void verify(pending)}>Check payment status</button>}
    {guest && <small>Sign in to make a payment and save it to your account.</small>}
    {message && <p className="form-message" role="status">{message}</p>}
    <small>Card and UPI details are collected by Razorpay.</small>
  </div>;
}

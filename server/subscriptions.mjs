const iso = value => Number.isFinite(Date.parse(value)) ? new Date(value).toISOString() : null;

// A calendar year, including leap-day purchases (Feb 29 -> Feb 28).
export function annualExpiry(purchasedAt) {
  const offset = 330 * 60 * 1000; // Account dates use Asia/Kolkata.
  const start = new Date(new Date(purchasedAt).getTime() + offset);
  if (!Number.isFinite(start.getTime())) throw new Error('A valid purchase date is required.');
  const end = new Date(start);
  end.setUTCFullYear(start.getUTCFullYear() + 1);
  if (end.getUTCMonth() !== start.getUTCMonth()) end.setUTCDate(0);
  return new Date(end.getTime() - offset).toISOString();
}

export function paidOrderDates(order) {
  if (order.status !== 'paid' || !order.paymentId || !order.verifiedAt) return null;
  const purchasedAt = iso(order.purchasedAt) || iso(order.verifiedAt);
  if (!purchasedAt) return null;
  return { purchasedAt, expiresAt: annualExpiry(purchasedAt) };
}

export function subscriptionDetails(database, userId, now = Date.now()) {
  const user = (database.users ?? []).find(item => item.id === userId);
  if (!user) return { hasPracticeAccess: false, subscriptionStatus: 'none' };
  const terms = (database.paymentOrders ?? []).filter(order => order.userId === userId)
    .map(order => ({ order, dates: paidOrderDates(order) })).filter(item => item.dates);
  // The user copy survives loss of transient session/profile flags.
  const savedPurchase = iso(user.subscriptionPurchasedAt);
  if (savedPurchase && user.subscriptionOrderId) terms.push({
    order: { orderId: user.subscriptionOrderId, planId: user.plan || user.subscription },
    dates: { purchasedAt: savedPurchase, expiresAt: annualExpiry(savedPurchase) },
  });
  terms.sort((a, b) => b.dates.expiresAt.localeCompare(a.dates.expiresAt));
  const term = terms[0];
  if (term) return {
    hasPracticeAccess: Date.parse(term.dates.expiresAt) > now,
    subscriptionStatus: Date.parse(term.dates.expiresAt) > now ? 'active' : 'expired',
    subscriptionPurchasedAt: term.dates.purchasedAt,
    subscriptionExpiresAt: term.dates.expiresAt,
    subscriptionOrderId: term.order.orderId,
    plan: term.order.planId || user.plan || user.subscription || null,
  };
  const legacy = Boolean(user.hasPracticeAccess || user.isSubscribed || user.subscription || user.plan);
  return { hasPracticeAccess: legacy, subscriptionStatus: legacy ? 'purchase_date_required' : 'none',
    subscriptionPurchasedAt: null, subscriptionExpiresAt: null, plan: user.plan || user.subscription || null };
}

// Idempotent backfill on startup and writes; never invent dates for legacy grants.
export function reconcileSubscriptions(database) {
  let changed = false;
  const assign = (target, fields) => {
    for (const [key, value] of Object.entries(fields)) if (target[key] !== value) {
      target[key] = value; changed = true;
    }
  };
  for (const order of database.paymentOrders ?? []) {
    const dates = paidOrderDates(order);
    if (dates) assign(order, { ...dates, purchaseDateSource: order.purchaseDateSource || 'saved_verification' });
  }
  for (const user of database.users ?? []) {
    const details = subscriptionDetails(database, user.id);
    if (details.subscriptionOrderId) assign(user, {
      subscriptionPurchasedAt: details.subscriptionPurchasedAt,
      subscriptionExpiresAt: details.subscriptionExpiresAt,
      subscriptionOrderId: details.subscriptionOrderId,
    });
  }
  return changed;
}

// Amounts are in paise. The backend uses this catalog as the price authority.
export const PAYMENT_PLANS = [
  { id: 'lite', name: 'Lite', amount: 79900, discountedAmount: 6900, currency: 'INR' },
  { id: 'ultra', name: 'Ultra', amount: 119900, discountedAmount: 9900, currency: 'INR' },
  { id: 'premium', name: 'Premium', amount: 159900, discountedAmount: 14900, currency: 'INR' },
];

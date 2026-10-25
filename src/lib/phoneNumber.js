export const isValidSignupPhone = value => typeof value === 'string' && /^[0-9]{10}$/.test(value);

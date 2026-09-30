import animate from "tailwindcss-animate";

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class", '[data-theme="dark"]'],
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      keyframes: {
        'arena-float': {
          '0%, 100%': { translate: '0 0' },
          '50%': { translate: '0 -8px' },
        },
      },
      borderRadius: { xl: "0.875rem", "2xl": "1.25rem" },
      boxShadow: {
        soft: "0 1px 2px rgba(15, 23, 42, .04), 0 12px 32px rgba(15, 23, 42, .06)",
      },
    },
  },
  plugins: [animate],
};

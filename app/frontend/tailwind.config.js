// frontend/tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        'pulse-fade': 'pulse-fade 2s ease-in-out infinite',
      },
      keyframes: {
        'pulse-fade': {
          '0%, 100%': { opacity: '0.2' },
          '50%': { opacity: '0.8' },
        },
      },
    },
  },
  plugins: [],
};
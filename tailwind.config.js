module.exports = {
  content: [
    './app/templates/**/*.html',
    './app/**/*.py',
    './src/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        coral: '#FF8F8F',
        cream: '#FFF1CB',
        sky: '#C2E2FA',
        lavender: '#B7A3E3',
      },
      animation: {
        shine: 'shine 1s',
      },
      keyframes: {
        shine: {
          '100%': { left: '125%' },
        },
      },
    },
  },
  plugins: [],
};

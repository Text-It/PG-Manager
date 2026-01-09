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
        brand1: '#D61C4E',
        brand2: '#FEB139',
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

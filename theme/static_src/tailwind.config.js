// theme/static_src/tailwind.config.js

module.exports = {
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00301C',
        secondary: '#D1FB5F',
      },
      fontFamily: {
        heading: ['Roboto', 'sans-serif'],
        body: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        'theme-color1': '#001524',
        'theme-color2': '#15616d',
        'theme-color3': '#ffecd1',
        'theme-color4': '#ff7d00',
      },
      screens: {
        xs: '480px',
      },
    },
  },
  plugins: [],
};

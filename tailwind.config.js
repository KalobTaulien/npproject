/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{css,js}", /* Frontend source files */
      "./prod/index.html" /* Output index.html file to monitor */
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
    ],
  }


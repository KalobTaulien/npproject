const webpack = require('webpack');
const path = require('path');

const config = {
    entry: './src/js/index.js',
    output: {
        path: path.resolve(__dirname, 'prod'),
        filename: 'app.js'
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/, // Updated this line to include jsx
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env', '@babel/preset-react'], // Make sure to include '@babel/preset-react'
            },
          },
        },
        // Other rules...
      ],
    }
};

module.exports = config;

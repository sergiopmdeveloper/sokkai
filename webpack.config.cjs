const path = require('path');

module.exports = {
  entry: path.resolve(__dirname, 'assets', 'index.js'),
  output: {
    path: path.resolve(__dirname, 'static'),
    filename: 'bundle.js',
  },
};

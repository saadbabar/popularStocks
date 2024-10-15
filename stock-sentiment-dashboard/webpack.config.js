const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.ts', // Entry point of your application
  output: {
    filename: 'bundle.js', // Output bundle file
    path: path.resolve(__dirname, 'dist'), // Output directory
  },
  resolve: {
    extensions: ['.ts', '.js'], // File extensions to handle
  },
  module: {
    rules: [
      {
        test: /\.ts$/, // Apply ts-loader to .ts files
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },

    devServer: {
    static: path.resolve(__dirname, 'dist'),
    compress: true,
    port: 8080,
    },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html', // Template for index.html
    }),
  ],
  mode: 'development', // Set mode to development or production
};

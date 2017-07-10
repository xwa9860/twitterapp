module.exports = {
  entry: ['./client/app.js'],
  output: {
    path: __dirname + '/twitterapp/static',
    filename: 'bundle.js'
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  }
};

const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');

const config = require('../webpack.config');

new WebpackDevServer(webpack(config), {
    disableHostCheck: true,
    publicPath: config.output.publicPath,
    hot: true,
    inline: true,
    historyApiFallback: false,
    headers: {
        'Access-Control-Allow-Origin': '*',
    },
}).listen(3000, '0.0.0.0', (err) => {
    if (err) {
        throw err;
    }

    console.log('Listening at http://0.0.0.0:3000/');
});

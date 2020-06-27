const path = require('path');

const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

const devMode = process.env.NODE_ENV !== 'production';
const devModeServer = 'http://wallingfordcastle.localhost:3000';

const src = [
    path.resolve(__dirname, 'js_src'),
    'node_modules',
];

module.exports = {
    context: path.resolve(__dirname),
    devtool: devMode ? 'cheap-module-eval-source-map' : undefined,
    entry: {
        global: './js_src/entry',
    },
    mode: devMode ? 'development' : 'production',
    optimization: {
        minimize: !devMode, // true, // Always enabled to allow for splitChunks
    },
    output: {
        filename: devMode ? 'js/[name].js' : 'js/[name]-[contenthash].js',
        path: path.resolve(__dirname, 'build/bundles'),
        publicPath: devMode ? `${devModeServer}/bundles/` : undefined,
    },
    plugins: [
        new webpack.NoEmitOnErrorsPlugin(),
        // devMode ? new webpack.HotModuleReplacementPlugin() : undefined,
         new BundleTracker({ filename: 'build/webpack-stats.json' }),
    ].filter(plugin => !!plugin),
    resolve: {
        extensions: ['.js'],
        modules: src,
    },
};

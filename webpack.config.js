const path = require('path');

const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

const devMode = process.env.NODE_ENV !== 'production';
const devModeServer = 'http://localhost:8080';

const src = [
    path.resolve(__dirname, 'js_src'),
    'node_modules',
];

module.exports = {
    context: path.resolve(__dirname),
    devtool: devMode ? 'cheap-module-source-map' : false,
    entry: {
        global: './js_src/entry',
    },
    mode: devMode ? 'development' : 'production',
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
            }, {  
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
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
        new BundleTracker({
            path: path.resolve(__dirname, 'build'),
            filename: 'webpack-stats.json'
        }),
    ].filter(plugin => !!plugin),
    resolve: {
        extensions: ['.js'],
        modules: src,
    },
    devServer: {
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization",
        },
    },
};

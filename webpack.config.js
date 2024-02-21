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
    devtool: devMode ? 'cheap-module-source-map' : false,
    entry: {
        global: './js_src/entry',
    },
    mode: devMode ? 'development' : 'production',
    module: {
        rules: [
            {
                test: /\.js$/,
                use: [
                    {
                        loader: 'babel-loader',
                    },
                ],
            },
        ],
    },
    optimization: {
        minimize: !devMode, // true, // Always enabled to allow for splitChunks
    },
    output: {
        filename: devMode ? '[name].js' : '[name]-[contenthash].js',
        path: path.resolve(__dirname, 'build/bundles'),
        publicPath: devMode ? `${devModeServer}/bundles/` : undefined,
    },
    plugins: [
        new BundleTracker({
            path: path.resolve(__dirname, 'build'),
            filename: 'webpack-stats.json'
        }),
    ],
    resolve: {
        extensions: ['.js'],
        modules: src,
    },
};

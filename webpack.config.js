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
        path: path.resolve(__dirname, 'build/bundles/js/'),
        publicPath: devMode ? `${devModeServer}/bundles/js/` : undefined,
    },
    plugins: [
        new webpack.NoEmitOnErrorsPlugin(),
        new BundleTracker({ path: path.resolve(__dirname, 'build'), filename: 'webpack-stats.json' }),
    ].filter(plugin => !!plugin),
    resolve: {
        extensions: ['.js'],
        modules: src,
    },
};

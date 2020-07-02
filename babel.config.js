module.exports = function(api) {
    api.cache(() => process.env.NODE_ENV === 'production');

    return {
        plugins: [
            '@babel/plugin-proposal-class-properties',
            '@babel/plugin-proposal-function-bind',
        ],
        presets: [
            '@babel/preset-react',
        ],
    };
};

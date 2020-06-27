module.exports = function(api) {
    api.cache(() => process.env.NODE_ENV === 'production');

    return {
        plugins: [
            '@babel/plugin-proposal-class-properties',
        ],
        presets: [
            '@babel/preset-react',
        ],
    };
};

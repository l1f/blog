module.exports = {
    entry: "./app/static/js/index.ts",
    devtool: 'inline-source-map',
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        exportsFields: ['.tsx', '.ts', '.js'],
        extensions: ['.ts', '.js']
    },
    output: {
        path: __dirname + "/app/static/dist",
        filename: "[name].bundle.js",
    },
};

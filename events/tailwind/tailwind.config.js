module.exports = {
    // purge: {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        // '../../**/*.js',
        // '../../**/*.py'
    ],
    // options: {
    //     safelist: [], // Specify the classes that should not be removed by purge
    // }
    // },
    theme: {
        extend: {
            fontFamily: {
                'sans': ['YourFont', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/container-queries')
    ],
}

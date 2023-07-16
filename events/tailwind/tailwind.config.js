const colors = require('tailwindcss/colors')
module.exports = {
    // purge: {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        // '../../**/*.js',
        '../users/forms.py',
        '../../apps/event/forms.py',
        '../../apps/membership/forms.py',
        '../../apps/store/forms.py',
        '../../apps/usac/forms.py',
        "node_modules/flowbite/**/*.js"
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
            colors: {
                'bc_cyan': colors.cyan[600],
                'bc_cyan_hover': colors.cyan[800],
                'bc_orange': colors.orange[600],
                'bc_orange_hover': colors.orange[800],
                'bc_green': colors.green[600],
                'bc_green_hover': colors.green[800],
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/container-queries'),
        require('flowbite/plugin'),
    ],
}

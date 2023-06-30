# Install Tailwind

Use `nvm` to install `node` and `npm` if not already installed and manage versions

Change to events/tailwind directory
`npm install -D tailwindcss`

# Build

you can add --watch to the end of the command to have it watch for changes and rebuild automatically.

npx tailwindcss -i ./static/src/style.css -o ../static/css/project.css
npx tailwindcss -i src/input.css -o ../static/css/project.css

# from top level

npx tailwindcss -i events/tailwind/src/input.css -o events/static/css/project.css

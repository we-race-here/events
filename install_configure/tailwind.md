# Install Tailwind

npm install -D tailwindcss

# Build

npx tailwindcss -i ./static/src/style.css -o ../static/css/project.css
npx tailwindcss -i src/input.css -o ../static/css/project.css

# from top level

npx tailwindcss -i events/tailwind/src/input.css -o events/static/css/project.css

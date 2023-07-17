<script>
    // Select all elements that have a 'data-limit' attribute
    const inputs = document.querySelectorAll('[data-limit]');

    // Iterate over the selected elements
    inputs.forEach(input => {
        // Add an 'input' event listener to each element
        input.addEventListener('input', function (e) {
            const limit = e.target.getAttribute('data-limit');
            const count = e.target.value.length;
            const remaining = limit - count;
            const countId = 'count' + e.target.id.replace(/\D/g, '');  // Create countId by removing non-digit characters from input id
            document.getElementById(countId).innerText = `${count}/${limit} (Remaining: ${remaining})`;
        });
    });
</script>

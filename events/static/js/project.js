/* Project specific Javascript goes here. */

// Basic Editor
ClassicEditor
        .create(document.querySelector('.editor-basic'), {
            toolbar: ['bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote']
        })
        .catch(error => {
            console.error(error);
        });

// Full Editor
ClassicEditor
    .create(document.querySelector('.editor-full'), {
        toolbar: ['bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', 'insertTable', 'mediaEmbed']
    })
    .catch(error => {
        console.error(error);
    });

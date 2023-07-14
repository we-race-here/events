/* Project specific Javascript goes here. */

// Basic Editor
var basicEditorElement = document.querySelector('.editor-basic');
if (basicEditorElement) {
    ClassicEditor
            .create(basicEditorElement, {
                toolbar: ['bold', 'italic', 'link', 'bulletedList', 'numberedList'],
                removePlugins: ["MediaEmbedToolbar"],
            })
            .catch(error => {
                console.error(error);
            });
}

// Full Editor
var fullEditorElement = document.querySelector('.editor-full');
if (fullEditorElement) {
    ClassicEditor
        .create(fullEditorElement, {
            removePlugins: ["MediaEmbedToolbar"],

        })
        .catch(error => {
            console.error(error);
        });
}

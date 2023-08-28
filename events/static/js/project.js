/* Project specific Javascript goes here. */
// JavaScript

function showMessage(content, timeout = 3000) {
    const messageBox = document.getElementById('messageBox');
    const messageContent = document.getElementById('messageContent');
    const closeButton = document.getElementById('closeMessageBtn');

    // Update content
    messageContent.innerHTML = content;

    // Show the message
    messageBox.classList.remove('hidden');

    // Close button click event
    closeButton.onclick = function() {
      messageBox.classList.add('hidden');
    };

    // Hide the message after `timeout` milliseconds
    setTimeout(() => {
      messageBox.classList.add('hidden');
    }, timeout);
  }

  // Listen for Django messages, assuming you have Django messages in a list with class 'django-messages'
  document.addEventListener("DOMContentLoaded", function() {
    const djangoMessages = document.querySelectorAll('.django-messages li');

    djangoMessages.forEach(message => {
      const content = message.textContent;
      showMessage(content);
    });
  });

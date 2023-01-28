

function showPopupMessage() {
  // Get the message element
  var message = document.getElementById('popup-message');

  // Remove the 'hidden' class to make the message visible
  message.classList.remove('hidden');

  // Set a timeout to hide the message after 3 seconds
  setTimeout(function() {
    message.classList.add('hidden');
  }, 3000);
}

// Add an event listener to show the message when the page loads
window.addEventListener('load', showPopupMessage);

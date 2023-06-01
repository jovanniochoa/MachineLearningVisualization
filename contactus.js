document.addEventListener('DOMContentLoaded', function() {
    var contactInfoText = document.querySelector('.contact-info-text');
    var dropdownItems = document.querySelectorAll('.dropdown-menu li');

    dropdownItems.forEach(function(item) {
      item.addEventListener('click', function() {
        contactInfoText.textContent = item.textContent;
      });
    });
  });
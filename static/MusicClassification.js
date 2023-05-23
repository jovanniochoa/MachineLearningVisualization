// Handle form submission
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Create a FormData object to send the file
    var formData = new FormData();
    formData.append('file', document.getElementById('file-input').files[0]);
    
    // Make an AJAX request to the back-end
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.result) {
                document.getElementById('result').innerHTML = 'Predicted class: ' + response.result;
            } else {
                document.getElementById('result').innerHTML = 'No prediction result';
            }
        } else {
            alert('File upload failed');
        }
    };
    xhr.send(formData);
});

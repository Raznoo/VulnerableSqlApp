document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const searchQuery = document.querySelector('input[name="searchQuery"]').value;
    const formAction = event.target.action;
    
    fetch(formAction, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'searchQuery': searchQuery
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from API:', data);
        alert('Received response: ' + JSON.stringify(data));
    })
    .catch(error => console.error('Error:', error));
});

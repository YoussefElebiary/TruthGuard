// Getting the btn element
const btn = document.getElementById('cust-btn');

// Handling clicks
btn.addEventListener('click', async () => {
    // Getting the value in the textarea
    const inputText = document.getElementById('cust-text').value;
    // Getting the selected model
    const selectedModelInput = document.getElementById('selected-model').value;
    
    // Handling empty text
    if (!inputText) {
        alert('Please enter the text');
        return;
    }

    // Handling empty model selection
    if (!selectedModelInput) {
        alert('Please select a model to use');
        return;
    }

    try {
        // Requesting a response from the back-end
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `text=${encodeURIComponent(inputText)}&model=${encodeURIComponent(selectedModelInput)}`,
        });
        // Waiting for the back-end to respond
        const data = await response.json();
        // Getting the status element
        const status = document.getElementById('status');

        // Checking if the server failed
        if (data.error) {
            status.textContent = "ERROR";
            status.style.display = 'block';
            status.style.color = 'yellow';
        } else {
            status.style.display = 'block';
            if (data.prediction == 1) { // Fake
                status.style.color = 'red';
                status.textContent = 'Fake';
            }
            else if (data.prediction == 0) { // True
                status.style.color = 'green';
                status.textContent = 'True';
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
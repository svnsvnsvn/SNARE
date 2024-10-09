// JavaScript for client-side logic

document.getElementById('listing-form').onsubmit = async function(e) {
    e.preventDefault();

    // Get the URL and address values from the form
    let url = document.getElementById('url').value;
    let address = document.getElementById('address').value;

    console.log(url);

    try {
        // Show a loading state
        document.getElementById('result').innerHTML = 'Checking the listing...';

        // Send a POST request to the FastAPI backend
        let response = await fetch('http://127.0.0.1:8000/check_listing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url }) // Ensure FastAPI expects 'address', was intally body: JSON.stringify({ url, address })
        });

        console.log(response.body)

        // Check if the response is okay (status 200-299)
        if (response.ok) {
            // Parse the response JSON
            let result = await response.json();
            document.getElementById('result').innerHTML = `The listing for ${result.address} is ${result.is_suspicious ? 'suspicious' : 'not suspicious'}`;
        } else {
            // Handle non-200 responses
            document.getElementById('result').innerHTML = `Error: ${error.message}. Could not check the listing. Please try again.`;
        }
    } catch (error) {
        // Catch any network or other errors
        document.getElementById('result').innerHTML = `Error: ${error.message}. Please try again.`;
    }
};

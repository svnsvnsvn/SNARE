// JavaScript for client-side logic

document.getElementById('listing-form').onsubmit = async function(e) {
    e.preventDefault();

    let url = document.getElementById('url').value;
    let address = document.getElementById('address').value;

    let response = await fetch('/check_listing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({url, address})
    });

    let result = await response.json();
    document.getElementById('result').innerHTML = `The listing for ${result.address} is ${result.is_suspicious ? 'suspicious' : 'not suspicious'}`;
};
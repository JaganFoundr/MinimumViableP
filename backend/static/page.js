document.getElementById('investment-form').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent default form submission

  const income = document.getElementById('income').value;
  const savings = document.getElementById('savings').value;
  const riskTolerance = document.getElementById('risk-tolerance').value;
  const country = document.getElementById('country').value;

  const loading = document.getElementById('loading');
  const recommendationsDiv = document.getElementById('recommendations');

  loading.style.display = 'block'; // Show loading indicator
  recommendationsDiv.innerHTML = ''; // Clear previous recommendations

  // Make a POST request to the Flask backend
  fetch('/recommend', { // Assuming the server is running on the same origin
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Specify the content type
    },
    body: JSON.stringify({
      income,
      savings,
      risk_tolerance: riskTolerance,
      country
    }), // Send data as JSON
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json(); // Parse the response JSON
    })
    .then(data => {
      // Display the recommendations smoothly
      const recommendationsText = `Recommended investments: ${data.recommendations.join(', ')} (${data.currency})`;
      const resultItem = document.createElement('div');
      resultItem.className = 'result-item';
      resultItem.textContent = recommendationsText;

      // Append result item with a fade-in effect
      recommendationsDiv.appendChild(resultItem);
      resultItem.classList.add('fade-in');
    })
    .catch((error) => {
      console.error('Error:', error);
      const errorMessage = document.createElement('div');
      errorMessage.className = 'alert alert-danger mt-4'; // Bootstrap alert for errors
      errorMessage.textContent = 'Error: ' + error.message;
      recommendationsDiv.appendChild(errorMessage);
    })
    .finally(() => {
      loading.style.display = 'none'; // Hide loading indicator
    });
});

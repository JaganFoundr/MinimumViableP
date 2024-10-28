document.getElementById('investment-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const income = document.getElementById('income').value;
  const savings = document.getElementById('savings').value;
  const riskTolerance = document.getElementById('risk-tolerance').value;
  const country = document.getElementById('country').value;

  const loading = document.getElementById('loading');
  loading.classList.add('show');

  // Update this URL if your Flask app is hosted elsewhere
  fetch('http://localhost:5000/recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ income, savings, risk_tolerance: riskTolerance, country }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      // Display the recommendations (adjust as necessary to match your new HTML structure)
      window.location.href = `/recommendations?investment=${data.recommendations.join(', ')}&currency=${data.currency}`;
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Error: ' + error.message);
    })
    .finally(() => {
      loading.classList.remove('show');
    });
});

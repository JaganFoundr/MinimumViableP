document.getElementById('investment-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const income = document.getElementById('income').value;
  const savings = document.getElementById('savings').value;
  const riskTolerance = document.getElementById('risk-tolerance').value;
  const country = document.getElementById('country').value;

  const loading = document.getElementById('loading');
  loading.classList.add('show');

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
      // Display the recommendations
      document.getElementById('recommendation').innerText = 'Recommended investments: ' + data.recommendations.join(', ') + ' (' + data.currency + ')';
      document.getElementById('recommendation').classList.add('show');
    })
    .catch((error) => {
      document.getElementById('recommendation').innerText = 'Error: ' + error.message;
      document.getElementById('recommendation').classList.add('alert-danger', 'show');
    })
    .finally(() => {
      loading.classList.remove('show');
    });
});

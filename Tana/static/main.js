document.addEventListener('DOMContentLoaded', function() {
  // Assuming you have a function that fetches the offices
  fetchOffices();
});

function fetchOffices() {
  // This is a placeholder. Replace it with your actual API endpoint
  fetch('/api/get_offices')
    .then(response => response.json())
    .then(data => {
      const dropdownMenu = document.getElementById('officeDropdownMenu');
      dropdownMenu.innerHTML = ''; // Clear loading text

      data.forEach(office => {
        const item = document.createElement('a');
        item.className = 'dropdown-item';
        item.href = office.link; // Adjust link if necessary
        item.innerText = office.name; // Replace with the actual name of the office
        dropdownMenu.appendChild(item);
      });
    })
    .catch(error => console.error('Error fetching offices:', error));
}


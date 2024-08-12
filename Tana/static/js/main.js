// Fetch office names and populate the dropdown
async function fetchOfficeNames() {
    try {
      const response = await fetch('/offices_list');
      const officeNames = await response.json();
      const officeDropdownMenu = document.getElementById('officeDropdownMenu');
      officeDropdownMenu.innerHTML = ''; // Clear loading text
      officeNames.forEach((officeName) => {
        const anchor = document.createElement('a');
        anchor.className = 'dropdown-item';
        anchor.href = `/office/${officeName}`;
        anchor.textContent = officeName;
        officeDropdownMenu.appendChild(anchor);
      });
    } catch (error) {
      console.error('Error fetching office names:', error);
      const officeDropdownMenu = document.getElementById('officeDropdownMenu');
      officeDropdownMenu.innerHTML = '<a class="dropdown-item" href="#">Error loading offices</a>';
    }
  }
  
  // Call the function to populate the dropdown menu when the page loads
  document.addEventListener('DOMContentLoaded', fetchOfficeNames);
  
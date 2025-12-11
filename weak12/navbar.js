function toggleMenu() {
    const nav = document.querySelector('.navbar');
    nav.classList.toggle('hidden');
}

function toggleNeon() {
    const navbar = document.getElementById('navbar');
    const button = document.getElementById('toggleNeonBtn');
    const body = document.body;
    const table = document.getElementById('componentTable');
    
    navbar.classList.toggle('depressed');
    button.classList.toggle('depressed');
    body.classList.toggle('depressed');
    table.classList.toggle('depressed');
    
    // Update button text
    if (button.classList.contains('depressed')) {
        button.textContent = 'Toggled Depression';
    } else {
        button.textContent = 'Toggled Neon';
    }
}

function sortByPrice() {
    const table = document.getElementById('componentTable');
    const rows = Array.from(table.querySelectorAll('tr')).slice(1);
    
    rows.sort((a, b) => {
        const priceA = parseInt(a.cells[1].textContent);
        const priceB = parseInt(b.cells[1].textContent);
        return priceA - priceB;
    });
    
    rows.forEach(row => table.appendChild(row));
}

function sortByNameRating() {
    const table = document.getElementById('componentTable');
    const rows = Array.from(table.querySelectorAll('tr')).slice(1);
    
    rows.sort((a, b) => {
        const nameA = a.cells[0].textContent;
        const nameB = b.cells[0].textContent;
        return nameA.localeCompare(nameB);
    });
    
    rows.forEach(row => table.appendChild(row));
}
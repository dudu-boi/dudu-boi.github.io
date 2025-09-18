let isGreen = false;

// Toggle text colour
function changeTextColour() {
    const table = document.getElementById("bookTable");
    table.style.color = isGreen ? "black" : "green";
    isGreen = !isGreen;
}

// Show/Hide nav menu
function toggleMenu() {
    const nav = document.getElementById("mainNav");
    nav.style.display = nav.style.display === "none" ? "block" : "none";
}

// Sort rows by price
function sortByPrice() {
    const table = document.getElementById("bookTable");
    const rows = Array.from(table.rows).slice(1); // skip header

    rows.sort((a, b) => {
        const priceA = parseFloat(a.cells[2].innerText);
        const priceB = parseFloat(b.cells[2].innerText);
        return priceA - priceB;
    });

    rows.forEach(row => table.appendChild(row)); // Re-add rows in sorted order
}

// Validate form input
function validateForm(title, author, price) {
    if (!title || !author || price === "") {
        alert("Please fill in all required fields.");
        return false;
    }

    if (!/^[a-zA-Z\s]+$/.test(title) || !/^[a-zA-Z\s]+$/.test(author)) {
        alert("Title and author must contain only letters and spaces.");
        return false;
    }

    const numericPrice = parseFloat(price);
    if (isNaN(numericPrice) || numericPrice < 0) {
        alert("Price must be a positive number.");
        return false;
    }

    return true;
}

// Hook form submission
document.getElementById("bookForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const author = document.getElementById("author").value.trim();
    const price = document.getElementById("price").value.trim();

    if (!validateForm(title, author, price)) {
        return;
    }

    const table = document.getElementById("bookTable");
    const newRow = table.insertRow();
    newRow.insertCell(0).innerText = title;
    newRow.insertCell(1).innerText = author;
    newRow.insertCell(2).innerText = parseFloat(price).toFixed(2); // format to 2 decimal places

    document.getElementById("bookForm").reset();
});

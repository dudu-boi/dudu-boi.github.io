// Flag to toggle text colour
let isRed = false;

// Change the text colour of the component table
function changeTextColour() {
    const table = document.getElementById("componentTable");
    table.style.color = isRed ? "black" : "red";
    isRed = !isRed;
}

// Sort the table by price (ascending)
function sortByPrice() {
    const table = document.getElementById("componentTable");
    const rows = Array.from(table.rows).slice(1); // skip header row

    // Convert the second column (price) to integer and sort
    rows.sort((a, b) => {
        const priceA = parseInt(a.cells[1].innerText, 10);
        const priceB = parseInt(b.cells[1].innerText, 10);
        return priceA - priceB;
    });

    // Append sorted rows back into the table
    rows.forEach(row => table.appendChild(row));
}

// Show or hide the navigation menu
function toggleMenu() {
    const nav = document.getElementById("mainNav");
    if (nav.style.display === "none") {
        nav.style.display = "block";
    } else {
        nav.style.display = "none";
    }
}

// Validate the contact form before submission
function validateForm() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();

    if (name === "" || email === "" || message === "") {
        alert("Please fill in all required fields.");
        return false;
    }

    alert("Message sent successfully!");
    return true;
}

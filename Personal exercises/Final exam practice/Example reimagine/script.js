function toggleMenu() {
  const nav = document.getElementById("mainNav");
  nav.style.display = nav.style.display === "none" ? "block" : "none";
}

function sortByGrade() {
  const table = document.getElementById("studentTable");
  const rows = Array.from(table.rows).slice(1); // skip header

  rows.sort((a, b) => {
    const gradeA = parseFloat(a.cells[2].innerText);
    const gradeB = parseFloat(b.cells[2].innerText);
    return gradeA - gradeB;
  });

  rows.forEach(row => table.appendChild(row)); // append in sorted order
}

function validateForm(name, subject, grade) {
  if (!name || !subject || grade === "") {
    alert("Please fill in all required fields.");
    return false;
  }

  if (!/^[a-zA-Z\s]+$/.test(name) || !/^[a-zA-Z\s]+$/.test(subject)) {
    alert("Name and subject must contain only letters and spaces.");
    return false;
  }

  const numericGrade = parseFloat(grade);
  if (isNaN(numericGrade) || numericGrade < 0 || numericGrade > 10) {
    alert("Grade must be a number between 0 and 10.");
    return false;
  }

  return true;
}

document.getElementById("studentForm").addEventListener("submit", function(event) {
  event.preventDefault();

  const name = document.getElementById("name").value.trim();
  const subject = document.getElementById("subject").value.trim();
  const grade = document.getElementById("grade").value.trim();

  if (!validateForm(name, subject, grade)) {
    return;
  }

  const table = document.getElementById("studentTable");
  const newRow = table.insertRow();
  newRow.insertCell(0).innerText = name;
  newRow.insertCell(1).innerText = subject;
  newRow.insertCell(2).innerText = grade;

  document.getElementById("studentForm").reset();
});

// Exercise 1: Add two numbers
function exercise02() {
    var txta = prompt("Enter number A");
    var txtb = prompt("Enter number B");

    if (txta == null || txta.trim() === "" || isNaN(txta)) {
        alert("Number A is formatted incorrectly");
    } else if (txtb == null || txtb.trim() === "" || isNaN(txtb)) {
        alert("Number B is formatted incorrectly");
    } else {
        var result = parseFloat(txta) + parseFloat(txtb);
        alert("Result:\n" + txta + " + " + txtb + " = " + result);
    }
}

// Exercise 2: Check if a number is even or odd
function exercise03() {
    var txta = prompt("Enter any integer");

    if (txta == null || txta.trim() === "" || isNaN(txta)) {
        document.write("<font color='red'>You must enter a number</font>");
    } else if (parseInt(txta) % 2 === 0) {
        document.write("<font color='green'><b>" + txta + " is an even number</b></font>");
    } else {
        document.write("<font color='blue'><i>" + txta + " is an odd number</i></font>");
    }
}

// Call the functions
exercise02();
exercise03();
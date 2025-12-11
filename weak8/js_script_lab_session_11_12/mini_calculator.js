function calculate() {
    const a = document.frmCal.txta.value.trim();
    const b = document.frmCal.txtb.value.trim();
    const op = document.frmCal.slto.value;
    const resultField = document.frmCal.txtr;

    if (a === "" || b === "") {
        alert("⚠️ Both inputs are required. Math refuses to operate on spiritual emptiness.");
        return;
    }

    const numA = parseInt(a);
    const numB = parseInt(b);

    if (isNaN(numA) || isNaN(numB)) {
        alert("⚠️ Numbers only, dear traveler. No hieroglyphs.");
        return;
    }

    let result;

    // helper: list common factors
    function commonFactors(x, y) {
        const limit = Math.min(Math.abs(x), Math.abs(y));
        const list = [];
        for (let i = 1; i <= limit; i++) {
            if (x % i === 0 && y % i === 0) list.push(i);
        }
        return list.join(", ");
    }

    // helper: list common multiples up to a reasonable cutoff
    function commonMultiples(x, y) {
        const cap = 20 * Math.max(Math.abs(x), Math.abs(y)); // prevent infinity
        const list = [];
        for (let i = 1; i <= cap; i++) {
            if (i % x === 0 && i % b === 0) list.push(i);
            if (list.length >= 15) break; // don’t produce a novel
        }
        return list.join(", ");
    }

    // --- operation switch ---
    switch (op) {
        case "+":
            result = numA + numB;
            break;

        case "-":
            result = numA - numB;
            break;

        case "*":
            result = numA * numB;
            break;

        case "/":
            if (numB === 0) {
                alert("🛑 Division by zero is forbidden by mathematics and several religions.");
                return;
            }
            result = numA / numB;
            break;

        case "%":
            if (numB === 0) {
                alert("🛑 Modulo by zero? A crime.");
                return;
            }
            result = numA % numB;
            break;

        case "^":
            result = Math.pow(numA, numB);
            break;

        case "cm": // common multiples listing
            result = commonMultiples(numA, numB);
            break;

        case "cf": // common factors listing
            result = commonFactors(numA, numB);
            break;

        default:
            alert("⚠️ Unknown operator. The machine spirit is displeased.");
            return;
    }

    resultField.value = result;
}

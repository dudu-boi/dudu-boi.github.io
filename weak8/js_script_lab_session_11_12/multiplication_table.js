function display() {
    const a = document.f.a;
    const txt = document.getElementById("view_area").contentWindow;

    // This line correctly erases the *previous* result
    txt.document.body.innerHTML = "";

    if(a.value == "" || isNaN(a.value)) {
        txt.document.write("<span style='color:red'>Please enter a valid number.</span>");
    } else {
        txt.document.write("<b>Multiplication table " + a.value + ":</b><br/>");
        
        for (let i = 1; i <= 10; i++) {
            txt.document.write(a.value + " x " + i + " = " + (i * a.value) + "<br/>");
        }
    }
}
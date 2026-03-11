/**
 * Validador de contraseñas – Frontend
 * La petición se hace a /api/validar, que Nginx reenviará al backend.
 */

function validar() {
    const password = document.getElementById("password").value;

    fetch("/api/validar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
    })
        .then((res) => res.json())
        .then((data) => {
            const barra = document.getElementById("barra");
            const nivelTexto = document.getElementById("nivel");
            const erroresDiv = document.getElementById("errores");

            nivelTexto.innerText = data.nivel;
            erroresDiv.innerHTML = "";

            if (data.nivel === "Fuerte") {
                barra.style.width = "100%";
                barra.style.backgroundColor = "#2ecc71";
            } else if (data.nivel === "Media") {
                barra.style.width = "50%";
                barra.style.backgroundColor = "#f1c40f";
            } else {
                barra.style.width = "20%";
                barra.style.backgroundColor = "#e74c3c";
            }

            if (data.errores.length > 0) {
                erroresDiv.innerHTML =
                    "<ul>" +
                    data.errores.map((e) => `<li>${e}</li>`).join("") +
                    "</ul>";
            }
        });
}

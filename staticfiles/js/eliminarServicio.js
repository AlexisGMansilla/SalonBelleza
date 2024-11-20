document.addEventListener("DOMContentLoaded", () => {
    const confirmModal = document.getElementById("confirmModal");
    const successModal = document.getElementById("successModal");
    const servicioNombre = document.getElementById("servicioNombre");
    const servicioEliminado = document.getElementById("servicioEliminado");
    const cancelarEliminar = document.getElementById("cancelarEliminar");
    const confirmarEliminar = document.getElementById("confirmarEliminar");
    const cerrarModal = document.getElementById("cerrarModal");
    let eliminarUrl;

    document.querySelectorAll(".eliminar-button").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            eliminarUrl = button.getAttribute("href");
            const nombre = button.closest("tr").querySelector("td:nth-child(2)").textContent;
            servicioNombre.textContent = nombre;
            confirmModal.style.display = "flex";
        });
    });

    cancelarEliminar.addEventListener("click", () => {
        confirmModal.style.display = "none";
    });

    confirmarEliminar.addEventListener("click", () => {
        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]');
        if (!csrfToken) {
            console.error("CSRF token no encontrado.");
            alert("Error: CSRF token no disponible.");
            return;
        }

        fetch(eliminarUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken.value,
            },
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error en la solicitud");
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    confirmModal.style.display = "none";
                    servicioEliminado.textContent = servicioNombre.textContent;
                    successModal.style.display = "flex";

                    // Eliminar la fila sin recargar la página
                    document.querySelector(`a[href="${eliminarUrl}"]`).closest("tr").remove();
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Ha ocurrido un error al intentar eliminar el servicio.");
            });
    });

    cerrarModal.addEventListener("click", () => {
        successModal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === confirmModal) confirmModal.style.display = "none";
        if (e.target === successModal) successModal.style.display = "none";
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const confirmModal = document.getElementById("confirmModal");
    const successModal = document.getElementById("successModal");
    const turnoDetalle = document.getElementById("turnoDetalle");
    const cancelarEliminar = document.getElementById("cancelarEliminar");
    const confirmarEliminar = document.getElementById("confirmarEliminar");
    const cerrarModal = document.getElementById("cerrarModal");
    let eliminarUrl;

    // Manejador de los botones "Eliminar"
    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            eliminarUrl = button.getAttribute("href");
            const clienteDetalle = button.closest("tr").querySelector("td:nth-child(3)").textContent;
            turnoDetalle.textContent = clienteDetalle;
            confirmModal.style.display = "flex";
        });
    });

    // Cancelar eliminación
    cancelarEliminar.addEventListener("click", () => {
        confirmModal.style.display = "none";
    });

    // Confirmar eliminación
    confirmarEliminar.addEventListener("click", () => {
        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

        fetch(eliminarUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error en la solicitud");
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    confirmModal.style.display = "none";
                    successModal.style.display = "flex";

                    // Elimina la fila correspondiente
                    document.querySelector(`a[href="${eliminarUrl}"]`).closest("tr").remove();
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Ha ocurrido un error al intentar eliminar el turno.");
            });
    });

    // Cerrar modal de éxito
    cerrarModal.addEventListener("click", () => {
        successModal.style.display = "none";
    });

    // Cerrar modales al hacer clic fuera
    window.addEventListener("click", (e) => {
        if (e.target === confirmModal) confirmModal.style.display = "none";
        if (e.target === successModal) successModal.style.display = "none";
    });
});
// Detectar el clic en el botón "Aceptar"
document.getElementById('cerrarModal').addEventListener('click', function () {
    // Cierra el modal (opcional, si es necesario ocultarlo)
    document.getElementById('successModal').style.display = 'none';
    // Recarga la página
    window.location.reload();
});

document.addEventListener("DOMContentLoaded", function () {
    if (typeof $ === "undefined") {
        console.error("jQuery no está definido. Asegúrate de cargar jQuery antes de Select2.");
        return;
    }

    console.log("Inicializando Select2...");
    const selectElement = $("#id_servicios");
    if (selectElement.length > 0) {
        selectElement.select2({
            placeholder: "Selecciona uno o más servicios",
            allowClear: true,
            maximumSelectionLength: 3,
            language: {
                noResults: function () {
                    return "No se encontraron resultados";
                },
                maximumSelected: function () {
                    return "Solo puedes seleccionar hasta 3 servicios";
                },
            },
        });
        console.log("Select2 inicializado correctamente.");
    } else {
        console.error("Elemento select no encontrado.");
    }
});

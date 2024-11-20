document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const selectedDay = urlParams.get('day'); // Obtiene el día de la URL

    // Ocultar todas las pestañas inicialmente
    document.querySelectorAll('.tab-panel').forEach(function(panel) {
        panel.classList.add('hidden');
    });

    if (selectedDay) {
        // Activa la pestaña del día seleccionado
        const targetTab = document.querySelector(`a[href="#tab-${selectedDay}"]`);
        const targetPanel = document.querySelector(`#tab-${selectedDay}`);

        if (targetTab && targetPanel) {
            document.querySelectorAll('.tab-item').forEach(function(tab) {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-panel').forEach(function(panel) {
                panel.classList.remove('active');
            });

            targetTab.parentElement.classList.add('active');
            targetPanel.classList.add('active');
        }
    } else {
        // Si no hay `day` en la URL, activa la primera pestaña por defecto
        document.querySelector('.tab-item').classList.add('active');
        document.querySelector('.tab-panel').classList.add('active');
    }

    // Mostrar todas las pestañas después de seleccionar la correcta
    document.querySelectorAll('.tab-panel').forEach(function(panel) {
        panel.classList.remove('hidden');
    });
});

// Permitir cambiar de pestañas
document.querySelectorAll('.tab-list a').forEach(function(tabLink) {
    tabLink.addEventListener('click', function(event) {
        event.preventDefault();

        // Remover clase 'active' de todos los tab items y ocultar paneles
        document.querySelectorAll('.tab-item').forEach(function(tab) {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-panel').forEach(function(panel) {
            panel.classList.remove('active');
        });

        // Activar pestaña y panel correspondiente
        this.parentElement.classList.add('active');
        const targetPanel = document.querySelector(this.getAttribute('href'));
        targetPanel.classList.add('active');
    });
});

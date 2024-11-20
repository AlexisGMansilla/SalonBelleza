// Obtener la URL desde el meta tag
const urlEnviarFecha = document.querySelector('meta[name="url-enviar-fecha"]').getAttribute('content');

// Deshabilitar domingos en el selector de fecha
document.getElementById('id_fechaTurno').addEventListener('change', function () {
    const selectedDate = new Date(this.value);
    const dayOfWeek = selectedDate.getUTCDay();

    if (dayOfWeek === 0) {
        alert('No se pueden seleccionar turnos los domingos.');
        this.value = ''; // Limpiar la fecha seleccionada
    } else {
        enviarFechaSeleccionada(this.value); // Enviar la fecha seleccionada al servidor
    }
});

// Asegurar que la fecha mínima es el día actual
document.addEventListener('DOMContentLoaded', function () {
    const fechaInput = document.getElementById('id_fechaTurno');
    const today = new Date().toISOString().split('T')[0];
    fechaInput.setAttribute('min', today); // Establecer la fecha mínima como hoy
});

// Función para enviar la fecha seleccionada al servidor
function enviarFechaSeleccionada(selectedDate) {
    console.log("Fecha seleccionada antes de enviar:", selectedDate);

    // Crear el cuerpo de la solicitud
    const formData = new FormData();
    formData.append('fechaTurno', selectedDate);

    // Enviar la solicitud al servidor
    fetch(urlEnviarFecha, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(), // Asegurar que se incluye el token CSRF
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        console.log('Opciones de hora recibidas:', data.opciones_horas);

        // Actualizar las opciones en el campo "horaTurno"
        const horaSelect = document.getElementById('id_horaTurno');
        horaSelect.innerHTML = ''; // Limpiar opciones previas

        if (data.opciones_horas && Array.isArray(data.opciones_horas)) {
            data.opciones_horas.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion[0];
                optionElement.textContent = opcion[1];
                horaSelect.appendChild(optionElement);
            });
        } else {
            console.error('Formato de opciones_horas inesperado:', data.opciones_horas);
        }
    })
    .catch(error => console.error('Error al enviar la fecha:', error));
}

// Función para obtener el token CSRF desde el meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function goBack() {
    const previousUrl = document.referrer; // Obtiene la URL anterior
    if (previousUrl) {
        window.location.href = previousUrl; // Navega hacia la URL anterior
    } else {
        window.location.href = '/'; // Si no hay referrer, redirige a la página principal (o a otra URL predeterminada)
    }
}
    // Deshabilitar domingos
    document.getElementById('id_fechaTurno').addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        const dayOfWeek = selectedDate.getUTCDay();

        if (dayOfWeek === 0) {
            alert('No se pueden seleccionar turnos los domingos.');
            this.value = ''; // Limpiar fecha seleccionada
        }
    });

    document.addEventListener('DOMContentLoaded', function() {
        const fechaInput = document.getElementById('id_fechaTurno');
        const today = new Date().toISOString().split('T')[0];

        fechaInput.setAttribute('min', today);
    });

    document.getElementById('id_fechaTurno').addEventListener('change', function() {
        const selectedDate = this.value;
        
        // Crear un formulario temporal para enviar solo la fecha
        const formData = new FormData();
        formData.append('fechaTurno', selectedDate);  // Donde selectedDate es el valor de la fecha
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');  // Incluye el token CSRF

        fetch('{% url "Turnos:enviar_fecha" %}', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            console.log('Opciones de hora recibidas:', data.opciones_horas);  // Manejar las opciones de hora
    
            // Ejemplo de cómo podrías actualizar un select con las opciones de hora
            const horaSelect = document.getElementById('id_horaTurno');
            horaSelect.innerHTML = '';  // Limpia las opciones existentes
    
            // Agregar las nuevas opciones de horas
            data.opciones_horas.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion[0];  // El valor de la opción
                optionElement.textContent = opcion[1];  // El texto que se mostrará
                horaSelect.appendChild(optionElement);
            });
        })
        .catch(error => console.error('Error al enviar la fecha:', error));
    });
document.addEventListener('DOMContentLoaded', function() {
    function updateTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0'); // Añade un 0 si es necesario
        const minutes = now.getMinutes().toString().padStart(2, '0'); // Añade un 0 si es necesario
        const seconds = now.getSeconds().toString().padStart(2, '0'); // Añade un 0 si es necesario
        const timeString = `${hours}:${minutes}:${seconds}`;
        
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = `Hora actual: ${timeString}`;
        }
    }

    setInterval(updateTime, 1000);
    updateTime(); 
});
function generateCalendar(month, year) {
    const calendarDays = document.getElementById('calendarDays');
    const monthYear = document.getElementById('monthYear');
    calendarDays.innerHTML = '';


    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    monthYear.textContent = `${months[month]} ${year}`;


    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();


    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.classList.add('empty-day');
        calendarDays.appendChild(emptyDay);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayButton = document.createElement('button');
        dayButton.classList.add('day');
        dayButton.textContent = `${day}`;


        const today = new Date();
        if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
            dayButton.classList.add('selected');
        }

        calendarDays.appendChild(dayButton);
    }
}

const today = new Date();
generateCalendar(today.getMonth(), today.getFullYear());
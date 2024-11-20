document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("demandaSemanalChart").getContext("2d");

    const demandaSemanal = JSON.parse(ctx.canvas.dataset.demandaSemanal);
    const diasSemana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab"]; // Excluye "Dom"

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: diasSemana,
            datasets: [
                {
                    label: "Turnos Confirmados",
                    data: demandaSemanal.slice(0, 6), // Toma solo los datos de lunes a sábado
                    backgroundColor: "rgba(219, 53, 69, 1)",
                    borderColor: "rgba(211, 47, 47, 1)",
                    borderWidth: 1,
                    borderRadius: 10,
                    barPercentage: 0.6,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Turnos: ${context.raw}`;
                        },
                    },
                },
            },
            layout: {
                padding: {
                    top: 10,
                    bottom: 10,
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 2 },
                    grid: { color: "rgba(211, 211, 211, 0.3)" },
                },
                x: {
                    grid: { display: false },
                },
            },
        },
    });
});

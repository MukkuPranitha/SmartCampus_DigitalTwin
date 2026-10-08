const API_URL = "https://smart-campus-backend-nvv6.onrender.com";
// Production backend

// ==========================================
// MAIN AI PREDICTION
// ==========================================

async function predictElectricity() {

    const buildingType =
        document.getElementById("buildingType").value;

    const data = {

        Building_Type: buildingType,

        Hour: 14,

        Occupancy:
            Number(document.getElementById("occupancy").value),

        Temperature:
            Number(document.getElementById("temperature").value),

        Humidity:
            Number(document.getElementById("humidity").value),

        Lighting_Usage:
            Number(document.getElementById("lighting").value),

        AC_Usage:
            Number(document.getElementById("ac").value),

        Computer_Usage:
            Number(document.getElementById("computer").value),

        Water_Consumption:
            Number(document.getElementById("water").value),

        Waste_Generated:
            Number(document.getElementById("waste").value),

        Year: 2026,
        Month: 10,
        Day: 7,
        DayOfWeek: 2
    };


    try {

        const response = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        if (!response.ok) {
            throw new Error("Prediction request failed");
        }


        const result = await response.json();

        const prediction =
            Number(result.predicted_electricity);


        // Main prediction card
        document.getElementById(
            "predictionValue"
        ).textContent =
            prediction.toFixed(2) + " kWh";


        // Store current prediction for What-If comparison
        const currentPrediction =
            document.getElementById("currentPrediction");

        if (currentPrediction) {

            currentPrediction.textContent =
                prediction.toFixed(2) + " kWh";
        }


        // Update dashboard cards
        document.getElementById(
            "occupancyValue"
        ).textContent =
            data.Occupancy;


        document.getElementById(
            "temperatureValue"
        ).textContent =
            data.Temperature;


        document.getElementById(
            "humidityValue"
        ).textContent =
            data.Humidity;


        // Reset comparison
        const predictionChange =
            document.getElementById("predictionChange");

        if (predictionChange) {

            predictionChange.textContent = "--";
        }

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not connect to the backend. Make sure FastAPI is running."
        );
    }
}



// ==========================================
// WHAT-IF SIMULATION
// ==========================================

async function updateSimulation() {

    const occupancy =
        Number(
            document.getElementById("simOccupancy").value
        );

    const ac =
        Number(
            document.getElementById("simAC").value
        );


    // Update slider values on screen
    document.getElementById(
        "simOccupancyValue"
    ).textContent =
        occupancy + "%";


    document.getElementById(
        "simACValue"
    ).textContent =
        ac + "%";


    const data = {

        Building_Type:
            document.getElementById("buildingType").value,

        Hour: 14,

        Occupancy: occupancy,

        Temperature:
            Number(
                document.getElementById("temperature").value
            ),

        Humidity:
            Number(
                document.getElementById("humidity").value
            ),

        Lighting_Usage:
            Number(
                document.getElementById("lighting").value
            ),

        AC_Usage: ac,

        Computer_Usage:
            Number(
                document.getElementById("computer").value
            ),

        Water_Consumption:
            Number(
                document.getElementById("water").value
            ),

        Waste_Generated:
            Number(
                document.getElementById("waste").value
            ),

        Year: 2026,
        Month: 10,
        Day: 7,
        DayOfWeek: 2
    };


    try {

        const response = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        if (!response.ok) {
            throw new Error("Simulation request failed");
        }


        const result = await response.json();


        const simulated =
            Number(result.predicted_electricity);


        // Show simulated prediction
        document.getElementById(
            "simulationPrediction"
        ).textContent =
            simulated.toFixed(2) + " kWh";


        // Get current prediction
        const predictionElement =
            document.getElementById("predictionValue");


        if (!predictionElement) {
            return;
        }


        const current =
            Number(
                predictionElement.textContent
                    .replace(" kWh", "")
                    .trim()
            );


        // Calculate difference
        if (!isNaN(current)) {

            const difference =
                simulated - current;


            const changeElement =
                document.getElementById(
                    "predictionChange"
                );


            if (changeElement) {

                changeElement.textContent =
                    (difference >= 0 ? "+" : "") +
                    difference.toFixed(2) +
                    " kWh";
            }
        }

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "simulationPrediction"
        ).textContent =
            "Error";

        const changeElement =
            document.getElementById(
                "predictionChange"
            );

        if (changeElement) {

            changeElement.textContent =
                "--";
        }
    }
}



// ==========================================
// ELECTRICITY TREND CHART
// ==========================================

async function loadTrend() {

    try {

        const response =
            await fetch(
                `${API_URL}/trend`
            );


        if (!response.ok) {
            throw new Error(
                "Trend request failed"
            );
        }


        const data =
            await response.json();


        const canvas =
            document.getElementById(
                "trendChart"
            );


        if (!canvas) {
            return;
        }


        const ctx =
            canvas.getContext("2d");


        new Chart(ctx, {

            type: "line",

            data: {

                labels:
                    data.dates,

                datasets: [{

                    label:
                        "Electricity Consumption",

                    data:
                        data.electricity,

                    tension:
                        0.3,

                    fill:
                        false,

                    pointRadius:
                        2,

                    borderWidth:
                        2
                }]
            },


            options: {

                responsive:
                    true,

                maintainAspectRatio:
                    false,


                interaction: {

                    mode:
                        "index",

                    intersect:
                        false
                },


                plugins: {

                    legend: {

                        display:
                            true
                    }
                },


                scales: {

                    y: {

                        title: {

                            display:
                                true,

                            text:
                                "Electricity Consumption (kWh)"
                        }
                    },


                    x: {

                        ticks: {

                            maxTicksLimit:
                                12
                        }
                    }
                }
            }
        });

    }

    catch (error) {

        console.error(
            "Could not load trend:",
            error
        );
    }
}



// ==========================================
// START TREND CHART
// ==========================================

loadTrend();
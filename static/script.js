document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const jsonData = {};

    formData.forEach((value, key) => {
        if (key === "Cabin" && value.trim() === "") {
            jsonData[key] = "Desconocido";
        } else if (key === "Ticket") {
            jsonData[key] = value.trim(); // SIEMPRE string
        } else {
            jsonData[key] = isNaN(value) || value.trim() === "" ? value : Number(value);
        }
    });

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonData)
    });

    const result = await response.json();

    // Muestra TODO el resultado formateado
    //document.getElementById("result").innerText = JSON.stringify(result, null, 2);

    // O si solo quieres la predicción:
   // ✅ Obtiene SOLO la predicción [0]
    const predictionValue = result.prediction[0];

    // ✅ Interpreta la predicción
    const resText = predictionValue === 1 ? "✅ ¡Sobrevivió!" : "❌ No sobrevivió...";

    // ✅ Muestra SOLO el mensaje interpretado
    document.getElementById("result").innerText = resText;

});


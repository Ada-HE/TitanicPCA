document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const jsonData = {};

    formData.forEach((value, key) => {
        // Convierte strings numéricos a número si es necesario
        jsonData[key] = isNaN(value) || value.trim() === "" ? value : Number(value);
    });
    console.log("Datos enviados al back:", jsonData);

    // ✅ Conversión forzada a string para los campos categóricos
    jsonData["Sex"] = String(jsonData["Sex"]);
    jsonData["Embarked"] = String(jsonData["Embarked"]);
    jsonData["Cabin"] = String(jsonData["Cabin"]);
    jsonData["Ticket"] = String(jsonData["Ticket"]);
    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonData)
    });

    const result = await response.json();
    const resText = result.prediction === 1 ? "Survived" : "Not survived...";
    document.getElementById("result").innerText = resText;
});

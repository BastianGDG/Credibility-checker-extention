document.getElementById("checkBtn").addEventListener("click", function() {
    const text = document.getElementById("selectedText").value;
    const resultDiv = document.getElementById("result");
    if (text.trim() === "") {
      resultDiv.textContent = "Ingen tekst markeret";
      return;
    }
    // Her integreres din logik til at tjekke tekstens kildeunderstøttelse, fx via API-kald
    resultDiv.textContent = "Teksten er understøttet af kilder."; 
  });

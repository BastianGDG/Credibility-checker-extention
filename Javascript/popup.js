chrome.storage.local.get("selectedText", (data) => {
  try {
    const selectedTextEl = document.getElementById("selectedText");
    const resultsContainer = document.getElementById("results");
    const loader = document.getElementById("loader");

    if (data.selectedText) {
      selectedTextEl.textContent = data.selectedText;

      // Vis loader
      loader.style.display = "block";

      fetch("http://localhost:5000/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: data.selectedText })
      })
      .then(res => res.json())
      .then(results => {
        console.log("Modtaget fra Python:", results);

        // Skjul loader
        loader.style.display = "none";

        resultsContainer.innerHTML = ""; // reset

        results.forEach(entry => {
          const div = document.createElement("div");
          div.innerHTML = `
            <p><strong>URL:</strong> <a href="${entry.url}" target="_blank">${entry.url}</a></p>
            <p><strong>Domæne:</strong> ${entry.domain}</p>
            <p><strong>AI vurdering:</strong> ${entry.verdict}</p>
            <hr/>
          `;
          resultsContainer.appendChild(div);
        });
      })
      .catch(err => {
        console.error("Fejl ved fetch til Python:", err);
        loader.style.display = "none"; // Skjul loader ved fejl
      });
    } else {
      selectedTextEl.textContent = "Ingen tekst fundet.";
    }
  } catch (err) {
    console.error("Fejl i popup.js:", err);
  }
});
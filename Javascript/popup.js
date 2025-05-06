chrome.storage.local.get("selectedText", (data) => {
  try {
    const selectedTextEl = document.getElementById("selectedText");
    const resultsContainer = document.getElementById("results");
    const loader = document.getElementById("loader");

    if (data.selectedText) {
      selectedTextEl.textContent = data.selectedText;
      loader.style.display = "block";

      fetch("http://localhost:5000/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: data.selectedText })
      })
      .then(res => res.json())
      .then(response => {
        console.log("Modtaget fra Python:", response);
        loader.style.display = "none";
        resultsContainer.innerHTML = "";
        
        if (response && typeof response.support_percentage !== 'undefined') {
          // Add support percentage
          const percentageDiv = document.createElement("div");
          percentageDiv.innerHTML = `<p><strong>Support Percentage:</strong> ${response.support_percentage}%</p><hr/>`;
          resultsContainer.appendChild(percentageDiv);
          
          // Add individual results
          if (response.results && Array.isArray(response.results)) {
            response.results.forEach(entry => {
              if (entry.url && entry.domain && entry.verdict) {
                const div = document.createElement("div");
                div.innerHTML = `
                  <p><strong>URL:</strong> <a href="${entry.url}" target="_blank">${entry.url}</a></p>
                  <p><strong>Domæne:</strong> ${entry.domain}</p>
                  <p><strong>AI vurdering:</strong> ${entry.verdict}</p>
                  <hr/>
                `;
                resultsContainer.appendChild(div);
              }
            });
          }
        } else {
          resultsContainer.innerHTML = "<p>Ingen resultater fundet</p>";
        }
      })
      .catch(err => {
        console.error("Fejl ved fetch til Python:", err);
        loader.style.display = "none";
        resultsContainer.innerHTML = "<p>Der opstod en fejl under behandlingen</p>";
      });
    } else {
      selectedTextEl.textContent = "Ingen tekst fundet.";
    }
  } catch (err) {
    console.error("Fejl i popup.js:", err);
  }
});
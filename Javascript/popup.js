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
          const percentage = response.support_percentage.toFixed(2);
          let color;
          if (percentage <= 33) {
            color = "red";
          } else if (percentage <= 66) {
            color = "yellow";
          } else {
            color = "green";
          }
          
          const percentageDiv = document.createElement("div");
          percentageDiv.innerHTML = `
            <div class="percentage-container">
              <div id="percentage" data-color="${color}">
                ${percentage}%
              </div>
              <div class="percentage-label">troværdighed</div>
            </div>
          `;
          resultsContainer.appendChild(percentageDiv);
          
          if (response.results && Array.isArray(response.results)) {
            const sourcesDiv = document.createElement("div");
            sourcesDiv.className = "sources-container";
            sourcesDiv.innerHTML = "<h2>Kilder</h2>";
            
            response.results.forEach(entry => {
              if (entry.url && entry.domain && entry.verdict) {
                const sourceCard = document.createElement("div");
                sourceCard.className = "source-card";
                sourceCard.innerHTML = `
                  <div class="source-header">
                    <span class="domain-badge">${entry.domain}</span>
                    <span class="verdict-badge ${entry.verdict.toLowerCase()}">${entry.verdict}</span>
                  </div>
                  <a href="${entry.url}" target="_blank" class="source-link">${new URL(entry.url).pathname.substring(0, 50)}${new URL(entry.url).pathname.length > 50 ? '...' : ''}</a>
                `;
                sourcesDiv.appendChild(sourceCard);
              }
            });
            resultsContainer.appendChild(sourcesDiv);
          }
        } else {
          resultsContainer.innerHTML = "<p class='no-results'>Ingen resultater fundet</p>";
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
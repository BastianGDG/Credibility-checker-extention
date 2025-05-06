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

          if (response.using_non_whitelisted) {
            const warningDiv = document.createElement("div");
            warningDiv.className = "warning-message";
            warningDiv.innerHTML = "⚠️ Bemærk: Beregningen er baseret på ikke-hvidlistede kilder, da ingen troværdige kilder blev fundet";
            resultsContainer.appendChild(warningDiv);
          }
          
          if (response.results && Array.isArray(response.results)) {
            // Separator for whitelisted sources
            const whitelistedSources = response.results.filter(entry => entry.whitelisted);
            if (whitelistedSources.length > 0) {
              const whitelistedDiv = document.createElement("div");
              whitelistedDiv.className = "sources-container";
              whitelistedDiv.innerHTML = "<h2>Troværdige Kilder</h2>";
              
              whitelistedSources.forEach(entry => createSourceCard(entry, whitelistedDiv));
              resultsContainer.appendChild(whitelistedDiv);
            }

            // Separator for non-whitelisted sources
            const nonWhitelistedSources = response.results.filter(entry => !entry.whitelisted);
            if (nonWhitelistedSources.length > 0) {
              const nonWhitelistedDiv = document.createElement("div");
              nonWhitelistedDiv.className = "sources-container";
              nonWhitelistedDiv.innerHTML = "<h2>Andre Kilder</h2>";
              
              nonWhitelistedSources.forEach(entry => createSourceCard(entry, nonWhitelistedDiv));
              resultsContainer.appendChild(nonWhitelistedDiv);
            }
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

function createSourceCard(entry, container) {
  if (entry.url) {
    const sourceCard = document.createElement("div");
    sourceCard.className = "source-card";
    
    // Use the whitelisted domain if available, otherwise try to extract domain from URL
    let displayDomain = entry.domain || 'Unknown Domain';
    if (!entry.whitelisted) {
      try {
        displayDomain = new URL(entry.url).hostname;
      } catch (e) {
        displayDomain = entry.url.split('/')[2] || 'Unknown Domain';
      }
    }

    sourceCard.innerHTML = `
      <div class="source-header">
        <span class="domain-badge ${entry.whitelisted ? 'whitelisted' : 'non-whitelisted'}">${displayDomain}</span>
        <span class="verdict-badge ${entry.verdict.toLowerCase()}">${entry.verdict}</span>
      </div>
      <a href="${entry.url}" target="_blank" class="source-link">${entry.url}</a>
    `;
    container.appendChild(sourceCard);
  }
}
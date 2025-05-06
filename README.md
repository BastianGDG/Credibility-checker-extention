# Credibility Checker

![Credibility Checker](https://img.shields.io/badge/Version-1.0-blue.svg) ![Manifest Version](https://img.shields.io/badge/Manifest%20Version-3-green.svg)

Credibility Checker is a browser extension designed to evaluate the credibility of selected text by analyzing sources using AI and Google search. It categorizes sources as whitelisted (trusted) or non-whitelisted and provides a credibility score.

---

## Features

- **Credibility Score**: Calculates the percentage of sources supporting the selected text.
- **Whitelisted Sources**: Highlights trusted sources from a predefined whitelist.
- **Modern UI**: Displays results in a clean and user-friendly interface.
- **AI Integration**: Uses AI to analyze the content of sources.

---

## Installation

### Prerequisites

- **Python 3.11+**: Ensure Python is installed on your system.
- **Google Chrome**: The extension is designed for Chrome.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/credibility-checker.git
   ```

2. Navigate to the project directory:
   ```bash
   cd credibility-checker
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`.
   - Enable **Developer Mode**.
   - Click **Load unpacked** and select the `Javascript` folder.

5. Start the Python server:
   ```bash
   python run.bat
   ```

---

## Usage

1. Highlight text on any webpage.
2. Right-click and select **🔍 Tjek Kilder** from the context menu.
3. View the credibility score and source analysis in the popup.

---

## File Structure

```
credibility-checker/
├── Javascript/
│   ├── background.js
│   ├── manifest.json
│   ├── popup.css
│   ├── popup.html
│   └── popup.js
├── Python/
│   ├── main.py
│   ├── reliable_site_scraper.py
│   ├── Server.py
│   ├── whitelist.txt
│   └── scraper_modules/
│       ├── domain_trimmer.py
│       └── webScraping.py
├── requirements.txt
├── run.bat
└── README.md
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Flask**: For the backend server.
- **BeautifulSoup**: For web scraping.
- **Google GenAI**: For AI-based content analysis.
- **Shields.io**: For the badges.

---

## Credits

Special thanks to the contributors who made this project possible:

- [@BertramAakjaer](https://github.com/BertramAakjaer)
- [@BastianGDG](https://github.com/BastianGDG)
- [@06Nicolaj](https://github.com/06Nicolaj)
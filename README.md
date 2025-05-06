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
- **Google Chrome / Firefox**: The extension is designed for Chrome and Firefox.
- **Google AI API Key**: Required for AI analysis of sources.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/BastianGDG/Credibility-checker-extention.git
   ```

2. Navigate to the project directory:
   ```bash
   cd credibility-checker
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   - Go to https://makersuite.google.com/app/apikey to get your Google AI API key
   - Create a `.env` file in the `Python` directory
   - Add your API key to the `.env` file:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

5. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`.
   - Enable **Developer Mode**.
   - Click **Load unpacked** and select the `Javascript` folder (or the main extension folder if manifest is at root for Chrome).

6. Load the extension in Firefox:
   - Open Firefox and navigate to `about:debugging#/runtime/this-firefox`.
   - Click **Load Temporary Add-on...**.
   - Select the `manifest.json` file inside the `Firefox` folder.

7. Start the Python server:
   ```bash
   ./run.bat
   ```

---

## Usage

1. Highlight text on any webpage.
2. Right-click and select **🔍 Tjek Kilder** from the context menu.
3. View the credibility score and source analysis in the popup.

---

## Creators

The creators of the project:

- [@BertramAakjaer](https://github.com/BertramAakjaer)
- [@BastianGDG](https://github.com/BastianGDG)
- [@06Nicolaj](https://github.com/06Nicolaj)

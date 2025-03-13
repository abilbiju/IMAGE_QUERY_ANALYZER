# Image Analysis App

This project is a Flask application that allows users to upload images for analysis. It utilizes the OpenAI API to identify objects and entities within the images, providing detailed information in a structured JSON format. The application also supports user queries about the analyzed images.

## Features

- Upload images for analysis.
- Identify objects and entities in images with detailed features.
- Respond to user queries about the analyzed images.
- User-friendly interface with dynamic result display.

## Project Structure

```
image-analysis-app
├── app.py                  # Main entry point of the Flask application
├── templates               # HTML templates for the application
│   ├── index.html         # Form for image upload
│   └── result.html        # Displays analysis results
├── static                  # Static files (CSS, JS)
│   ├── css
│   │   └── style.css       # Styles for the application
│   └── js
│       └── main.js         # Client-side functionality
├── utils                   # Utility functions for image analysis and query processing
│   ├── __init__.py         # Marks the utils directory as a Python package
│   ├── image_analyzer.py   # Functions for image analysis using OpenAI API
│   └── query_processor.py   # Functions for processing user queries
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API keys, config)
├── .gitignore              # Files and directories to ignore in Git
└── README.md               # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd image-analysis-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Upload an image using the provided form.

4. View the analysis results on the results page.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
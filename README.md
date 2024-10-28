
# Daily Imbalance Cost Report

## Overview

The **Daily Imbalance Cost Report** project retrieves and processes data from the Elexon Insights API to generate a comprehensive report on system imbalance costs and prices. This project includes functionality for data fetching, processing, and visualization, providing users with an efficient way to analyze and report imbalance costs.

## Table of Contents

- Features
- Installation
- Usage
- Project Structure
- Testing
- Contributing
- License

## Features

- Fetch data from the Elexon Insights API.
- Calculate absolute volumes, imbalance costs, and other key metrics.
- Generate visualizations for better data analysis.
- Easy to extend with additional calculation or visualization features.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

``` 
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. Create a virtual environment:

```Python
python -m venv venv
```

3. Activate the virtual environment:

  - On Windows:

    ```
    venv\Scripts\activate
    ```

  - On macOS/Linux:

    ```
    source venv/bin/activate
    ```

4. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Running the Application: To run the application and generate the report, execute:

  ```
  python src/main.py
  ```

2. Accessing the Visualization: If using Dash for visualizations, start the server:

  ```
  python src/app.py
  ```
  
  Then navigate to http://127.0.0.1:8050 in your web browser.

## Project Structure

project/
│
├── assets/
│   └── style.css
│
├── src/
│   ├── components/
│   │   ├── layout.py
│   │   ├── line_chart.py
│   │   └── ids.py
│   │
│   └── data/
│       ├── fetcher.py
│       └── loader.py
│
├── tests/
│   └── test_calculations.py
│
├── requirements.txt
└── README.md

## Testing

This project includes unit tests to ensure the accuracy of calculations. To run the tests, use the following command:

  ```
  pytest
  ```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:

  ```
  git checkout -b feature/YourFeature
  ```

3. Commit your changes:

````
git commit -m "Add your feature description"
````

4. Push to the branch:

  ```
  git push origin feature/YourFeature
  ```

5. Create a pull request.


## License

This project is licensed under the MIT License. See the LICENSE file for details.


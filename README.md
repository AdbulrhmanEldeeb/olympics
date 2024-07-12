# Olympics Analysis App

This is a Streamlit web application for analyzing historical Olympics data. The app provides various insights and visualizations based on the data from the Kaggle Olympics dataset.

## Features

- **Medal Tally:** View the medal tally for different years and countries.
- **Overall Analysis:** Get overall statistics and trends in the Olympics.
- **Country-wise Analysis:** Analyze the performance of specific countries over the years.
- **Athlete-wise Analysis:** Explore data about athletes, including age distributions and participation trends.

## Dataset

The dataset used in this project is from Kaggle:
[120 Years of Olympic History: Athletes and Results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AdbulrhmanEldeeb/olympics.git
    cd olympics
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Download the dataset from Kaggle and place the `athlete_events.csv` and `noc_regions.csv` files in the root directory of the project.

## Usage

Run the Streamlit app:
  
    ```bash
    streamlit run app.py
## File Structure

- olympics/
  - app.py                # The main file for the Streamlit app.
  - helper.py             # Contains helper functions for data processing and visualization.
  - preprocessor.py       # Contains preprocessing functions for the dataset.
  - athlete_events.csv    # Dataset containing information about athletes and events.
  - noc_regions.csv       # Dataset containing information about NOC regions.

## Deployment
The app is deployed at [Olympics Analysis App](https://olympics-analysis-04.onrender.com/)








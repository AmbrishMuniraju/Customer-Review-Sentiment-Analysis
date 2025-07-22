# Customer Review Sentiment & Emotion Analysis

This project applies Natural Language Processing (NLP) to analyze customer reviews for two brands, focusing on sentiment analysis and emotion detection. [cite_start]The goal is to gain deep insights into customer perceptions and provide actionable recommendations for improving customer satisfaction[cite: 1013, 1019]. [cite_start]The project follows the CRISP-DM framework[cite: 1018].

## Key Features & Approach

* [cite_start]**Text Pre-processing:** Implemented a full NLP pipeline including text cleaning, normalization, tokenization, stop-word removal, and lemmatization to prepare the review data for analysis[cite: 1037, 1040, 1041, 1042].
* [cite_start]**Sentiment Analysis:** Used TextBlob to calculate sentiment polarity and classify reviews as positive, negative, or neutral[cite: 1481, 1483].
* [cite_start]**Emotion Prediction:** A Logistic Regression model was trained to predict specific emotions (e.g., joy, fear, surprise) for reviews that were previously unlabeled, enriching the dataset[cite: 1302, 1306].

## Key Visualization & Result

The analysis revealed distinct emotional profiles for each brand. Brand "H\_" was associated with more positive emotions like **joy** and **surprise**, which correlated with higher average star ratings. [cite_start]In contrast, Brand "Z\_" had a higher incidence of **sadness** and **fear**, indicating areas for improvement[cite: 1115, 1116, 1118].

![Emotion Distribution by Brand](visualizations/brand_emotion_distribution.png)

## Tech Stack
* Python
* Pandas & NumPy
* NLTK & TextBlob (for NLP tasks)
* Scikit-learn (for modeling)
* Matplotlib & Seaborn (for visualization)

## Data Availability
[cite_start]The original dataset (`A_II_Emotion_Data_Student_Copy_Final.xlsx`) is proprietary and not included in this repository[cite: 1385]. [cite_start]It contained customer reviews, star ratings, brand names, and some pre-labeled emotions[cite: 1020].

## Project Structure
-   **/report:** Contains the final project report (`Data Mining_A2.pdf`).
-   **/scripts:** Includes the Python script (`sentiment_analysis.py`) for the NLP pipeline and modeling.
-   **/visualizations:** Contains charts and plots generated during the analysis.

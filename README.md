# Introduction
Based on the framework of the paper, I mainly realized the contents of three modules. The following is a brief introduction of each folder:
- Data: This folder includes three original data sets (Data_labels, Data_performance and Data_tweets) and one processed data set (Data_merge).
- Web crawler: Twitter web crawler based on selenium and requests library. It can crawl tweets corresponding to the corresponding user id (file name) and the corresponding date of the csv file in the folder and save them.
- Sentiment classification model: Emotion classification model of tweets based on FastText. Training or prediction can be realized according to the adjustment of parameters.
- Prediction model of NBA game results: This module includes preprocessing of data and modeling and performance comparison of different supervised machine learning algorithms (KNN, Logistic Regression, SVM, XGBoost).

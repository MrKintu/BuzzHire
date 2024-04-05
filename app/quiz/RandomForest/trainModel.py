import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


if __name__ == "__main__":
    # Load data
    data = pd.read_csv(f'{BASE_DIR}\\RandomForest\\dataset.csv')
    X = data.drop(columns=['Personality'])
    y = data['Personality']

    # Splitting the training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=109)

    # Preprocess data
    label_encoder = LabelEncoder()

    question_train = pd.DataFrame()
    question_train["Question"] = label_encoder.fit_transform(X_train["Question"])
    question_train = question_train.reset_index(drop=True)
    X_train = X_train.drop(columns=["Question", "Age", "Gender"])
    X_train = X_train.reset_index(drop=True)
    X_train = pd.concat([question_train, X_train], axis=1)

    question_test = pd.DataFrame()
    question_test["Question"] = label_encoder.fit_transform(X_test["Question"])
    question_test = question_test.reset_index(drop=True)
    X_test = X_test.drop(columns=["Question", "Age", "Gender"])
    X_test = X_test.reset_index(drop=True)
    X_test = pd.concat([question_test, X_test], axis=1)

    # Train RandomForestClassifier
    rf_model = RandomForestClassifier(n_estimators=5)

    random_forest_path = f'{BASE_DIR}\\RandomForest\\random_forest.pkl'
    rf_model.fit(X_train, y_train)
    with open(random_forest_path, 'wb') as file:
        pickle.dump(rf_model, file)
    print(f"New Random Forest model trained and saved at {random_forest_path}.")

    # Get SVM predictions and evaluate the SVM model
    rf_predictions_train = rf_model.predict(X_train)
    rf_predictions_test = rf_model.predict(X_test)
    print("Random Forest Model Evaluation.")
    print(f'Training Accuracy: {accuracy_score(y_train, rf_predictions_train) * 100:.5f}%')
    print(f'Validation Accuracy: {accuracy_score(y_test, rf_predictions_test) * 100:.5f}%')

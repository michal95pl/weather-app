from sklearn.model_selection import train_test_split

import Dataset


if __name__ == "__main__":
    dataset = Dataset.Dataset()
    data = dataset.get_data()

    data = data.drop(["Date", "Location"], axis=1)

    #delete all row with null
    data = data.dropna()

    x = data.drop("RainToday", axis=1)
    y = data["RainToday"]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()

    model.fit(X_train, y_train)

    print(model.score(X_test, y_test))


    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import f1_score

    y_pred = model.predict(X_test)

    print(confusion_matrix(y_test, y_pred))
    print("F1-score:", f1_score(y_test, y_pred))
    print("Accuracy:", model.score(X_test, y_test))

    # save model
    import joblib
    joblib.dump(model, "../WeatherModel.pkl")



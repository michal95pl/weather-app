from sklearn.model_selection import train_test_split

from Dataset import Dataset
from Model import Model

from time import sleep

from statistics import median

if __name__ == "__main__":
    dataset = Dataset()
    dataset.show_correlation()

    F1_scores = []

    for location in dataset.get_locations():

        data = dataset.get_data_by_location(location)

        data = data.drop(["Date"], axis=1)
        data = data.drop(["Location"], axis=1)

        print(f"Location: {location}:")

        x = data.drop("RainToday", axis=1)
        y = data["RainToday"]

        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        model = Model()
        model.fit(X_train, y_train)
        model.show_statistics(X_test, y_test, location)

        F1_scores.append(model.get_F1_score(X_test, y_test))

        model.save_model(f"../models/{location}.pkl")

        print("\n\n\n")

        sleep(0.5)

    print("F1-score median:", median(F1_scores))



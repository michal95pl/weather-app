from sklearn.model_selection import train_test_split

from Dataset import Dataset
from Model import Model

if __name__ == "__main__":
    dataset = Dataset()
    dataset.show_correlation()

    data = dataset.get_data()

    data = data.drop(["Date", "Location"], axis=1)

    x = data.drop("RainToday", axis=1)
    y = data["RainToday"]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = Model()
    model.fit(X_train, y_train)
    model.show_statistics(X_test, y_test)

    model.save_model("../model.pkl")



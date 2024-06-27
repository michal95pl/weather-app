from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
import joblib
from random import randint


class Model:
    def __init__(self):
        self.__model = RandomForestClassifier()

    def fit(self, x, y):
        self.__model.fit(x, y)

    @staticmethod
    def show_plot(cm, title):
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", xticklabels=["Rainy", "No Rainy"], yticklabels=["Rainy", "No Rainy"])
        plt.xlabel("Truth")
        plt.ylabel("Predicted")
        plt.title(title)
        plt.show()

    def show_statistics(self, x, y, city_name):
        y_pred = self.__model.predict(x)

        cm = confusion_matrix(1 - y, 1 - y_pred, labels=[0, 1])

        if randint(0, 5) == 0:
            Model.show_plot(cm, city_name)

        print("Recall:", cm[0][0] / (cm[0][0] + cm[1][0]))
        print("Precision:", cm[0][0] / (cm[0][0] + cm[0][1]))
        print("F1-score:", f1_score(y, y_pred))
        print("Accuracy:", self.__model.score(x, y))

    def get_F1_score(self, x, y):
        y_pred = self.__model.predict(x)
        return f1_score(y, y_pred)

    def save_model(self, path):
        joblib.dump(self.__model, path)

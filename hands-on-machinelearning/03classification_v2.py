from sklearn import clone
import matplotlib

import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata

mnist = fetch_mldata("MNIST original", data_home='./mnist_dataset/')

X, y = mnist['data'], mnist['target']

some_digit = X[36000]
some_digit_image = some_digit.reshape(28, 28)

print(y[36000])  # 라벨값 확인.

# 셔플해보자.
import numpy as np

X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
shuffle_index = np.random.permutation(60000)
X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]

y_train_5 = (y_train == 5)  # True for all 5s, False for all other digits.
y_test_5 = (y_test == 5)
print('y_train_5', y_train_5)

# 훈련시킴
from sklearn.linear_model import SGDClassifier

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_5)

from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict

# cross_val_score 확인.
print('cross_val_score(sgd_clf,X_train, y_train_5, cv=3, scoring="accuracy"):',
      cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy"))

from sklearn.base import BaseEstimator
class Never5Classifier(BaseEstimator):
    def fit(self, X, y=None):
        pass

    def predict(self, X):
        return np.zeros((len(X), 1), dtype=bool)

never_5 = Never5Classifier()
print('cross_val_score(sgd_clf,X_train, y_train_5, cv=3, scoring="accuracy"):',
      cross_val_score(never_5, X_train, y_train_5, cv=3, scoring="accuracy"))

from sklearn.metrics import precision_recall_curve, confusion_matrix, f1_score

y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=5)

print('y_train_pred', type(y_train_pred))
# confusion matrix 확인해보자. (TP,TN, FP,FN)
print(confusion_matrix(y_train_5, y_train_pred))
skfolds = StratifiedKFold(n_splits=3, random_state=42)
y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3, method="decision_function")
precisions, recalls, thresholds = precision_recall_curve(y_train_5, y_scores)

print(precisions)
print(recalls)
print(thresholds)


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    print('len', len(thresholds), len(precisions), len(recalls))
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="upper left")
    plt.ylim([0, 1])


plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
plt.show()

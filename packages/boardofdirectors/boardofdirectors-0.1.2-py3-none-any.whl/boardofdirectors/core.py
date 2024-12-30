

class Libraries:
    def __init__(self):
        # Store the list of imports as a class attribute
        self.imports = [
            "import pandas as pd",
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "from sklearn.tree import plot_tree",
            "from sklearn.linear_model import LinearRegression",
            "from sklearn.tree import DecisionTreeRegressor",
            "from sklearn.ensemble import RandomForestRegressor",
            "from sklearn.svm import SVR",
            "from sklearn.neighbors import KNeighborsRegressor",
            "from sklearn.linear_model import LogisticRegression",
            "from sklearn.tree import DecisionTreeClassifier",
            "from sklearn.ensemble import RandomForestClassifier",
            "from sklearn.svm import SVC",
            "from sklearn.neighbors import KNeighborsClassifier",
            "from sklearn.naive_bayes import GaussianNB",
            "from sklearn.cluster import KMeans",
            "from sklearn.preprocessing import LabelEncoder",
            "from sklearn.preprocessing import StandardScaler",
            "from sklearn.preprocessing import MinMaxScaler",
            "from sklearn.decomposition import PCA",
            "from sklearn.model_selection import train_test_split",
            "from sklearn import metrics",
            "from sklearn.metrics import root_mean_squared_error, mean_absolute_error"
        ]
    
    def __repr__(self):
        # Return the imports as a formatted string when printed
        return "\n".join(self.imports)
    
class LabelEncoding:
    def __init__(self):
        # Store the code as a class attribute
        self.code = """
label_encoder = LabelEncoder()

columns = df.select_dtypes(object).columns

for col in columns:
    df[col] = label_encoder.fit_transform(df[col])

df.head()
        """
    
    def __repr__(self):
        # Return the code as a formatted string when printed
        return self.code
    
class Regression:
    def __init__(self):
        # Store the code as a class attribute
        self.code = """

logistic_regression = LogisticRegression()
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
svm = SVC()
knn = KNeighborsClassifier()
nb = GaussianNB()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

linear_regression.fit(x_train, y_train)
decision_tree.fit(x_train, y_train)
random_forest.fit(x_train, y_train)
svm.fit(x_train, y_train)
knn.fit(x_train, y_train)

y_pred_linear_regression = linear_regression.predict(x_test)
y_pred_decision_tree = decision_tree.predict(x_test)
y_pred_random_forest = random_forest.predict(x_test)
y_pred_svm = svm.predict(x_test)
y_pred_knn = knn.predict(x_test)

print("Linear Regression MAE: ", metrics.mean_absolute_error(y_test, y_pred_linear_regression))
print("Decision Tree MAE: ", metrics.mean_absolute_error(y_test, y_pred_decision_tree))
print("Random Forest MAE: ", metrics.mean_absolute_error(y_test, y_pred_random_forest))
print("SVM MAE: ", metrics.mean_absolute_error(y_test, y_pred_svm))
print("KNN MAE: ", metrics.mean_absolute_error(y_test, y_pred_knn))

print("Linear Regression MSE: ", metrics.mean_squared_error(y_test, y_pred_linear_regression))
print("Decision Tree MSE: ", metrics.mean_squared_error(y_test, y_pred_decision_tree))
print("Random Forest MSE: ", metrics.mean_squared_error(y_test, y_pred_random_forest))
print("SVM MSE: ", metrics.mean_squared_error(y_test, y_pred_svm))
print("KNN MSE: ", metrics.mean_squared_error(y_test, y_pred_knn))

print("Linear Regression RMSE: ", metrics.root_mean_squared_error(y_test, y_pred_linear_regression))
print("Decision Tree RMSE: ", metrics.root_mean_squared_error(y_test, y_pred_decision_tree))
print("Random Forest RMSE: ", metrics.root_mean_squared_error(y_test, y_pred_random_forest))
print("SVM RMSE: ", metrics.root_mean_squared_error(y_test, y_pred_svm))
print("KNN RMSE: ", metrics.root_mean_squared_error(y_test, y_pred_knn))

print("Linear Regression R-sq: ", metrics.r2_score(y_test, y_pred_linear_regression))
print("Decision Tree R-sq: ", metrics.r2_score(y_test, y_pred_decision_tree))
print("Random Forest R-sq: ", metrics.r2_score(y_test, y_pred_random_forest))
print("SVM R-sq: ", metrics.r2_score(y_test, y_pred_svm))
print("KNN R-sq: ", metrics.r2_score(y_test, y_pred_knn))
        """
    
    def __repr__(self):
        # Return the code as a formatted string when printed
        return self.code
    
    
class Classification:
    def __init__(self):
        # Store the code as a class attribute
        self.code = """

logistic_regression = LogisticRegression()
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
svm = SVC()
knn = KNeighborsClassifier()
nb = GaussianNB()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

logistic_regression.fit(x_train, y_train)
decision_tree.fit(x_train, y_train)
random_forest.fit(x_train, y_train)
svm.fit(x_train, y_train)
knn.fit(x_train, y_train)
nb.fit(x_train, y_train)

y_pred_logistic_regression = logistic_regression.predict(x_test)
y_pred_decision_tree = decision_tree.predict(x_test)
y_pred_random_forest = random_forest.predict(x_test)
y_pred_svm = svm.predict(x_test)
y_pred_knn = knn.predict(x_test)
y_pred_nb = nb.predict(x_test)

print("\nLogistic Regression Classification Report: \n", metrics.classification_report(y_test, y_pred_logistic_regression))
print("\n\nDecision Classification Report: \n", metrics.classification_report(y_test, y_pred_decision_tree))
print("\n\nRandom Forest Classification Report: \n", metrics.classification_report(y_test, y_pred_random_forest))
print("\n\nSVM Classification Report: \n", metrics.classification_report(y_test, y_pred_svm))
print("\n\nKNN Classification Report: \n", metrics.classification_report(y_test, y_pred_knn))
print("\n\nNavie Bayes Classification Report: \n", metrics.classification_report(y_test, y_pred_nb))
    
print("\nLogistic Regression Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_pred_logistic_regression))
print("\n\nDecision Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_pred_decision_tree))
print("\n\nRandom Forest Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_pred_random_forest))
print("\n\nSVM Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_pred_svm))
print("\n\nKNN Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_pred_knn))
print("\n\nNavie Bayes Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_pred_nb))    

print("\nLogistic Regression Accuracy Score: \n", metrics.accuracy_score(y_test, y_pred_logistic_regression))
print("\n\nDecision Accuracy Score: \n", metrics.accuracy_score(y_test, y_pred_decision_tree))
print("\n\nRandom Forest Accuracy Score: \n", metrics.accuracy_score(y_test, y_pred_random_forest))
print("\n\nSVM Accuracy Score: \n", metrics.accuracy_score(y_test, y_pred_svm))
print("\n\nKNN Accuracy Score: \n", metrics.accuracy_score(y_test, y_pred_knn))
print("\n\nNavie Bayes Accuracy Score: \n", metrics.accuracy_score(y_test, y_pred_nb))
        
        """
    
    def __repr__(self):
        # Return the code as a formatted string when printed
        return self.code
    
class Kmeans:
    def __init__(self):
        # Store the code as a class attribute
        self.code = """
kmeans = KMeans(n_clusters=4, random_state=0) 
kmeans.fit(x)

kmeans.cluster_centers_


from sklearn.metrics import adjusted_rand_score

ari_score = adjusted_rand_score(y, kmeans.labels_)
print("Adjusted Rand Index:", ari_score)

cs = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    kmeans.fit(x)
    cs.append(kmeans.inertia_)
plt.plot(range(1, 11), cs)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('CS')
plt.show()

from sklearn.datasets import make_blobs

x, y = make_blobs(centers=4, random_state=42)

cluster_numbers = [4]

for n_clusters in cluster_numbers:
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(x)
    labels = kmeans.labels_

    pca = PCA(n_components=2)
    x_pca = pca.fit_transform(x)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=labels, cmap='viridis', s=50)
    
    centers = pca.transform(kmeans.cluster_centers_)
    
    plt.scatter(centers[:, 0], centers[:, 1], marker='X', color='red', s=200, label='Centroids')
    
    plt.title(f'K-means Clustering (n_clusters={n_clusters})')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.colorbar(label='Cluster')
    plt.legend()
    plt.show()
        """
    
    def __repr__(self):
        # Return the code as a formatted string when printed
        return self.code
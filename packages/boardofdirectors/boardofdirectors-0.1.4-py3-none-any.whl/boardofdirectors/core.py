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

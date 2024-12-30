from sklearn import tree
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.metrics import confusion_matrix, accuracy_score


def program1(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    plt.figure(figsize=(8, 6))
    tree.plot_tree(classifier, filled=True)
    plt.show()

def program2(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    plt.figure(figsize=(8, 6))

    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=data["Wine"].unique(),
                yticklabels=data["Wine"].unique())
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix (Accuracy: {accuracy:.2f})")
    plt.show()

def program3(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    x_set, y_set = x_train, y_train
    cmap = ListedColormap(('red', 'green'))

    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j  # Use the colormap correctly
        )
    plt.title('K-NN Algorithm (Training set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()

    x_set, y_set = x_test, y_test
    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j  # Use the colormap correctly
        )
    plt.title('K-NN Algorithm (Test set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()

def program4(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    cmap = ListedColormap(['red', 'green'])

    x_set, y_set = x_train, y_train
    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j
        )
    plt.title('SVM classifier (Training set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()

    # Test set visualization
    x_set, y_set = x_test, y_test
    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j
        )
    plt.title('SVM classifier (Test set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()

def program5(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    plt.scatter(x_train, y_train, color="green")
    plt.plot(x_train, x_pred, color="red")
    plt.title("Salary vs Experience (Training Dataset)")
    plt.xlabel("Years of Experience")
    plt.ylabel("Salary(In Rupees)")
    plt.show()

    plt.scatter(x_test, y_test, color="blue")
    plt.plot(x_train, x_pred, color="red")
    plt.title("Salary vs Experience (Test Dataset)")
    plt.xlabel("Years of Experience")
    plt.ylabel("Salary(In Rupees)")
    plt.show()

def program6(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    cmap = ListedColormap(['purple', 'green'])

    # Training set visualization
    x_set, y_set = x_train, y_train
    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j  # Correct color mapping using cmap
        )
    plt.title('Random Forest Algorithm (Training set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()

    # Test set visualization
    x_set, y_set = x_test, y_test
    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j  # Correct color mapping using cmap
        )
    plt.title('Random Forest Algorithm (Test set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()

def program7(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    plt.plot(range(1, 11), wcss_list)
    plt.title('The Elobw Method Graph')
    plt.xlabel('Number of clusters(k)')
    plt.ylabel('wcss_list')
    plt.show()
    print()
    plt.scatter(data[y_pred == 0, 0], data[y_pred == 0, 1], s=100, c='blue', label='Cluster 1')  # for first cluster
    plt.scatter(data[y_pred == 1, 0], data[y_pred == 1, 1], s=100, c='green', label='Cluster 2')  # for second cluster
    plt.scatter(data[y_pred == 2, 0], data[y_pred == 2, 1], s=100, c='red', label='Cluster 3')  # for third cluster
    plt.scatter(data[y_pred == 3, 0], data[y_pred == 3, 1], s=100, c='cyan', label='Cluster 4')  # for fourth cluster
    plt.scatter(data[y_pred == 4, 0], data[y_pred == 4, 1], s=100, c='magenta', label='Cluster 5')  # for fifth cluster
    plt.scatter(classifier.cluster_centers_[:, 0], classifier.cluster_centers_[:, 1], s=300, c='yellow', label='Centroid')
    plt.title('Clusters of customers')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.show()

def program8(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    plt.scatter(data[y_pred == 0, 0], data[y_pred == 0, 1], s=100, c='blue', label='Cluster 1')
    plt.scatter(data[y_pred == 1, 0], data[y_pred == 1, 1], s=100, c='green', label='Cluster 2')
    plt.scatter(data[y_pred == 2, 0], data[y_pred == 2, 1], s=100, c='red', label='Cluster 3')
    plt.scatter(data[y_pred == 3, 0], data[y_pred == 3, 1], s=100, c='cyan', label='Cluster 4')
    plt.scatter(data[y_pred == 4, 0], data[y_pred == 4, 1], s=100, c='magenta', label='Cluster 5')
    plt.title('Clusters of customers')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.show()

def program9(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, wcss_list=None):
    labeling = classifier.labels_

    colours1 = {}
    colours1[0] = 'r'
    colours1[1] = 'g'
    colours1[2] = 'b'
    colours1[3] = 'c'
    colours1[4] = 'y'
    colours1[5] = 'm'
    colours1[-1] = 'k'
    cvec = [colours1[label] for label in labeling]
    colors = ['r', 'g', 'b', 'c', 'y', 'm', 'k']
    r = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[0])
    g = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[1])
    b = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[2])
    c = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[3])
    y = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[4])
    m = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[5])
    k = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[6])
    plt.figure(figsize=(9, 9))
    plt.scatter(data['C1'], data['C2'], c=cvec)
    plt.legend((r, g, b, c, y, m, k),
                ('Label M.0', 'Label M.1', 'Label M.2', 'Label M.3', 'Label M.4', 'Label M.5', 'Label M.-1'),
                scatterpoints=1, loc='upper left', ncol=3, fontsize=10)
    plt.show()

def program10(data=None, classifier=None, x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None, y_pred=None, x_validate=None, y_validate=None, wcss_list=None, errors=None):
    plt.figure(1)
    plt.scatter(x_train, y_train, c='blue', label='train')
    plt.scatter(x_validate, y_validate, c='pink', label='validation')
    plt.legend()
    plt.show()

    plt.plot(errors, label='MLP Function Approximation')
    plt.xlabel('epochs')
    plt.ylabel('cost')
    plt.legend()
    plt.show()
# HierarTree

HierarTree is a Python package for building and utilizing hierarchical decision tree classifiers. It is designed to handle datasets with hierarchical labels, providing robust classification and interpretability.

## Features

- Train hierarchical decision trees tailored for data with nested labels.
- Support for both decision tree and random forest models.
- Implements advanced scoring metrics for hierarchical data, including hierarchical accuracy and Brier scores.
- Visualize decision trees with detailed information on splits and classification metrics.
- Flexible configuration with options for maximum depth, minimum samples per leaf, and more.

## Installation

You can install HierarTree by cloning this repository and running:

```bash
pip install .
```

### Requirements

- Python >= 3.6
- numpy
- pandas
- matplotlib
- joblib
- sklearn

## Usage

### Basic Example

```python
from HierarTree import HierarchicalLabelDecisionTreeClassifier

# Example hierarchical label structure
hierarchy = {
    "Animal": {
        "Mammal": ["Dog", "Cat"],
        "Bird": ["Sparrow", "Pigeon"]
    }
}

# Initialize the classifier
classifier = HierarchicalLabelDecisionTreeClassifier(hierarchy=hierarchy)

# Training data
data = [
    {"feature1": 1.2, "feature2": 3.4, "label": ["Animal", "Mammal", "Dog"]},
    {"feature1": 2.3, "feature2": 1.4, "label": ["Animal", "Bird", "Sparrow"]},
]

# Fit the model
classifier.fit(data, response="label")

# Predictions
samples = [
    {"feature1": 1.5, "feature2": 3.2},
    {"feature1": 2.0, "feature2": 1.2},
]

predictions = classifier.predict(samples)
print(predictions)
```

## API Reference

### `HierarchicalLabelDecisionTreeClassifier`

#### Initialization
```python
HierarchicalLabelDecisionTreeClassifier(
    hierarchy,
    max_features=None,
    random_state=None,
    min_samples_leaf=1,
    min_samples_split=2,
    max_class_proportion=1,
    max_leaf_nodes=None,
    max_depth=None,
    no_values_iter=None,
    secondary_score='accuracy'
)
```
- `hierarchy`: Dictionary defining the hierarchical label structure.
- `max_features`: Number of features to consider for splits.
- `min_samples_leaf`: Minimum samples required to form a leaf node.
- `max_depth`: Maximum depth of the tree.

#### Methods
- `fit(data, response)`: Train the model.
- `predict(samples)`: Predict labels for given samples.
- `predict_terminal_probabilities(samples)`: Get probability distributions at terminal nodes.
- `plot_tree(node)`: Visualize the decision tree.

### `HierarchicalLabelRandomForestClassifier`

Provides ensemble learning with multiple hierarchical decision trees.

#### Initialization
```python
HierarchicalLabelRandomForestClassifier(
    hierarchy,
    n_trees=100,
    max_features='sqrt',
    random_state=None,
    min_samples_leaf=1,
    min_samples_split=2,
    max_class_proportion=1,
    max_leaf_nodes=None,
    max_depth=None,
    no_values_iter=None,
    secondary_score='accuracy'
)
```
- `n_trees`: Number of trees in the forest.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

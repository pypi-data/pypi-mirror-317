import math
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from collections import Counter
import pandas as pd
from joblib import Parallel, delayed
import numpy as np
from sklearn.utils import resample

class Node:
    def __init__(self, data, is_leaf=False, label=None):
        self.data = data  # Records at this node
        self.is_leaf = is_leaf  # Whether the node is a stop node
        self.label = label  # Concept label if it's a leaf
        self.children = []  # Child nodes
        self.split_attribute = None  # Attribute used for splitting
        self.split_threshold = None  # Threshold for numerical splits

class HierarchicalLabelDecisionTreeClassifier:
    def __init__(self, hierarchy, max_features=None, random_state=None, min_samples_leaf=1, min_samples_split=2, max_class_proportion=1, max_leaf_nodes=None, max_depth=None, no_values_iter=None, secondary_score='accuracy'):
        """
        Initialize the classifier.

        Args:
            hierarchy (dict): The hierarchy defining the levels and labels.
            max_class_proportion (float): Threshold for majority class proportion.
            max_features (int): 1 <= max_features <= data.shape[1] - 1. Randomly selects max_features to train the HLC on using random_state.
            random_state (int): Random state used to select feature subset of size max_features.
            min_samples_leaf (int): Threshold for minimum number of samples required to be in a leaf node.
            min_samples_split (int or float): Threshold for number of samples to split an internal node. If int, it represents the mimimum number of samples needed to split an internal node. If float, it represents the minimum proportion of samples needed to split an internal node.
            max_leaf_nodes (int): Threshold for maximum number of leaf nodes.
            max_leaf_nodes (int): Threshold for maximum depth of the Decision Tree.
            max_depth (int): The maximum depth of the Decision Tree.
            no_values_iter (int): The number of values for each non-categorical attribute to iterate through. Default None in which case each unique value is iterated through. 
            secondary_score (str): Either 'accuracy' or 'precision'. When determining leaf labels, we select the label with the highest score = accuracy x precision. In the case of a tie, we select the label with the higher accuracy or precision depending on the setting on this argument.
        """
        self.tree = None  # Root of the tree
        self.hierarchy = hierarchy
        self.h = self._compute_depth(hierarchy)# Number of levels in the hierarchy
        keys = hierarchy.keys()
        assert len(keys) == 1
        self.root = list(keys)[0] 
        self.max_class_proportion = max_class_proportion
        self.max_features = max_features
        self.random_state = random_state
        self.min_samples_leaf = min_samples_leaf
        assert type(min_samples_split) == int or type(min_samples_split) == float
        self.min_samples_split = min_samples_split
        self.max_leaf_nodes = max_leaf_nodes
        self.no_leaf_nodes = 0
        self.max_depth = max_depth
        self.entropy_cache = {}
        self.no_values_iter = no_values_iter
        assert secondary_score.lower() in ['accuracy', 'precision']
        self.secondary_score = secondary_score.lower()
        self.feature_importances_ = {}
        self.feature_split_counts_ = {}

    def fit(self, data, response):
        """
        Build the hierarchical classifier using the given training data.
        
        Args:
            data (list in dictionary records format or pandas dataframe): Training data records.
            response (str): Label corresponding to the response variable in data.
        """
        self.response = response
        if self.max_features is not None:
            def random_subset_numpy(input_list, n, random_state=None):
                rng = np.random.default_rng(seed=random_state)
                return list(rng.choice(input_list, size=n, replace=False))
            
            if type(data) == list:
                data = pd.DataFrame(data)
                features = [i for i in data.columns if i != self.response]
                subset = random_subset(features, self.max_features, self.random_state)
                data = data[subset + [self.response]]
        
        if type(data) == pd.core.frame.DataFrame:
            data = data.to_dict('records')
            
        if type(self.min_samples_split) == float:
            self.min_samples_split = np.ceil(self.min_samples_split * len(data))
        self.attributes = self._get_attributes(data)
        self.tree = Node(data)
        self._build_tree(self.tree)
        
        for i in self.feature_importances_.keys():
            self.feature_importances_[i] /= self.feature_split_counts_[i]

    def _build_tree(self, node, depth=0):
        """
        Recursively build the tree starting from the given node.

        Args:
            node (Node): Current node to process.
        """
        
        if self._can_stop(node, depth):
            # Mark node as stop and assign a concept label
            node.is_leaf = True
            node.label, node.level = self._determine_label(node)
            self.no_leaf_nodes += 1
            return
        
        best_info_gain = float('-inf')
        best_split = None
        best_attribute = None
        best_threshold = None

        # Evaluate splits for each attribute
        
        best_info_gain, best_attribute, best_split, best_threshold = self._evaluate_all_splits_parallel(node)
        if best_attribute in self.feature_importances_.keys():
            self.feature_importances_[best_attribute] += best_info_gain
            self.feature_split_counts_[best_attribute] += 1
        else:
            self.feature_importances_[best_attribute] = best_info_gain
            self.feature_split_counts_[best_attribute] = 1

        if best_split:
            # Partition node based on the best split
            node.split_attribute = best_attribute
            node.split_threshold = best_threshold
            node.children = []
            for subset in best_split:
                child_node = Node(subset)
                self._build_tree(child_node, depth=depth+1)
                node.children.append(child_node)

    def _can_stop(self, node, depth=0):
        """
        Test if the current node can be stopped.

        Args:
            node (Node): Node to test.

        Returns:
            bool: Whether the node is a stop node.
        """
        if self.max_leaf_nodes is not None and self.no_leaf_nodes >= self.max_leaf_nodes:
            return True
        
        if self.max_depth is not None and depth >= self.max_depth:
            return True
        
        # Check if the no. samples per split is below the threshold
        if len(node.data) <= self.min_samples_split:
            return True
        
        # Check if the majority class proportion exceeds the threshold
        labels = [record[self.response][-1] for record in node.data]
        majority_label = max(set(labels), key=labels.count)
        majority_proportion = labels.count(majority_label) / len(labels)

        if majority_proportion >= self.max_class_proportion:
            return True

        # Check if all attributes have been used in the path
        used_attributes = set()
        current_node = node
        while current_node:
            if current_node.split_attribute:
                used_attributes.add(current_node.split_attribute)
            current_node = current_node.parent if hasattr(current_node, 'parent') else None

        if len(used_attributes) == len(self.attributes):
            return True


        def evaluate_attribute(attribute):
            splits = self._evaluate_splits(node, attribute)
            for split_info in splits:
                info_gain = self._hierarchical_information_gain(node, split_info)
                if info_gain > 0:
                    return True  # Found a positive gain, no need to check further
            return False

        # Parallelize across attributes
        results = Parallel(n_jobs=-1)(
            delayed(evaluate_attribute)(attribute) for attribute in self.attributes
        )

        # If any attribute has a positive gain, we do not stop
        has_positive_gain = any(results)

        if not has_positive_gain:
            return True

        return False
    
    def _determine_label(self, node):
        """
        Determine the concept label for a stop node using the given metrics and algorithm.
    
        Args:
            node (Node): Node to label.
    
        Returns:
            Any: Concept label for the node.
        """
        data = node.data
        S_b = self._smallest_subtree(data)  # Get the smallest subtree
        D_vb = len(data)
        scores = []
        original_hierarchy = self.hierarchy

        for level in range(1, self.h + 1):
            labels = self._get_level(original_hierarchy, target_level=level)
            prec_ij = math.log(level + 1, self.h)
            for label in labels:
                D_vb_ij = sum(1 for record in data if record[self.response][level-1] == label)
                acc_ij = D_vb_ij / D_vb
                score_ij = acc_ij * prec_ij
                scores.append((score_ij, acc_ij, prec_ij, label, level))
        if self.secondary_score == 'accuracy':
            # Sort by score (descending) and accuracy (descending)
            scores.sort(key=lambda x: (-x[0], -x[1]))
        else:
            # Sort by score (descending) and precision (descending)
            scores.sort(key=lambda x: (-x[0], -x[2]))
        # Assign the top concept label
        node.score = scores[0][0]
        node.accuracy = scores[0][1]
        return (scores[0][3], scores[0][4]) if scores else (None, None)
    

    def _get_attributes(self, data):
        """
        Get all attributes available in the dataset.

        Args:
            data (list): Dataset.

        Returns:
            list: List of attribute names.
        """
        return [i for i in list(data[0].keys()) if i != self.response] if data else []
    
    def _evaluate_splits(self, node, attribute):
        """
        Evaluate all possible splits for a given attribute.

        Args:
            node (Node): Node to split.
            attribute (str): Attribute name.

        Returns:
            list: List of possible splits with thresholds (if applicable).
        """
        values = [record[attribute] for record in node.data]
        unique_values = sorted(set(values))
        splits = []
        
        if not all(isinstance(v, (int,float)) for v in unique_values):
            # Categorical attribute: evaluate splits for each unique value
            for value in unique_values:
                split = [
                    [record for record in node.data if record[attribute] == value],
                    [record for record in node.data if record[attribute] != value]
                ]
                smallest = min([len(rec) for rec in split])
                if smallest < self.min_samples_leaf:
                    continue
                splits.append({"split": split, "threshold": value})
        
        else:
            # Numerical attribute: evaluate all possible thresholds
            if self.no_values_iter is not None:
                thresholds = list(set(np.percentile(values, np.linspace(0, 100, self.no_values_iter + 1))))
            else:
                thresholds = unique_values
                
            for i in range(len(thresholds) - 1):
                threshold = (thresholds[i] + thresholds[i + 1]) / 2
                split = [
                    [record for record in node.data if record[attribute] <= threshold],
                    [record for record in node.data if record[attribute] > threshold]
                ]
                smallest = min([len(rec) for rec in split])
                if smallest < self.min_samples_leaf:
                    continue
                splits.append({"split": split, "threshold": threshold})
                
        return splits

    def _evaluate_splits_parallel(self, node, attribute):
        splits = self._evaluate_splits(node, attribute)
        gains = Parallel(n_jobs=-1)(delayed(self._hierarchical_information_gain)(node, split_info) for split_info in splits)
        return gains, splits
    
    def _evaluate_all_splits_parallel(self, node):
        attributes = self.attributes
        results = Parallel(n_jobs=-1)(
            delayed(self._evaluate_splits_parallel)(node, attribute) for attribute in attributes
        )

        # Flatten results
        best_info_gain = float('-inf')
        best_split = None
        best_attribute = None
        best_threshold = None

        for attribute, (gains, splits) in zip(attributes, results):
            for info_gain, split_info in zip(gains, splits):
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    best_attribute = attribute
                    best_split = split_info["split"]
                    best_threshold = split_info.get("threshold")

        return best_info_gain, best_attribute, best_split, best_threshold
    
    def _hierarchical_entropy(self, node):
        """
        Compute the hierarchical entropy for the given node.
    
        Args:
            node (Node): Node to compute entropy for.
    
        Returns:
            float: Hierarchical entropy.
        """
        data = node.data
        D_vb = len(data)
        original_hierarchy = self.hierarchy
        k = self.h - self._compute_depth(self._smallest_subtree(data)) + 2
        entropy = 0
        if D_vb > 0:
            for level in range(k, self.h + 1):
                labels = self._get_level(original_hierarchy, target_level=level)
                w_i = 0 if level <= 1 else (self.h - level + 1) * 2 / (self.h * (self.h - 1))
                for label in labels:
                    D_vb_ij = sum(1 for record in data if record[self.response][level-1] == label)
                    p_ij = D_vb_ij / D_vb
                    if p_ij > 0:
                        contribution = -p_ij * math.log2(p_ij) * w_i
                        entropy += contribution
            return entropy

    def _compute_depth(self, subtree):
        """
        Compute the depth of the subtree.

        Args:
            subtree (dict): Subtree of the hierarchy.

        Returns:
            int: Depth of the subtree.
        """
        if not isinstance(subtree, dict):
            return 1  # Leaf node
        return 1 + max(self._compute_depth(child) for child in subtree.values())
    
    def _get_level(self, data, target_level, current_level=1):
        """
        Traverses a hierarchical dictionary and returns all keys or items at the specified level.

        Args:
            data (dict): The hierarchical dictionary to traverse.
            target_level (int): The level to retrieve (1-indexed).
            current_level (int): The current level in the traversal (default is 1).

        Returns:
            list: A list of keys or items at the target level.
        """
        result = []

        # Base case: If the current level matches the target level
        if current_level == target_level:
            if isinstance(data, dict):
                result.extend(data.keys())
            elif isinstance(data, list):
                result.extend(data)
            return result

        # Recursive case: Traverse deeper into the dictionary
        if isinstance(data, dict):
            for key, value in data.items():
                result.extend(self._get_level(value, target_level, current_level + 1))
        return result
    
    def _hierarchical_information_gain(self, node, split_info):
        parent_entropy = getattr(node, "cached_entropy", None)
        if parent_entropy is None:
            parent_entropy = self._hierarchical_entropy(node)
            node.cached_entropy = parent_entropy

        D_vb = len(node.data)
        child_entropies = 0

        for subset in split_info["split"]:
            D_vx = len(subset)
            if D_vx == 0:
                continue

            child_entropy = self._hierarchical_entropy_cached(subset)
            child_entropies += (D_vx / D_vb) * child_entropy

        return parent_entropy - child_entropies

    def _hierarchical_entropy_cached(self, subset):
        # Use a memoized function or cache results to avoid redundant entropy calculations
        subset_hash = hash(frozenset(tuple(record.items()) for record in subset))
        if subset_hash in self.entropy_cache:
            return self.entropy_cache[subset_hash]
        entropy = self._hierarchical_entropy(Node(subset))
        self.entropy_cache[subset_hash] = entropy
        return entropy


    def _smallest_subtree(self, data):
        """
        Find the smallest subtree covering all labels in the data.

        Args:
            data (list): Dataset.

        Returns:
            dict: Subtree covering all labels in the data.
        """
        labels = set(record[self.response][-1] for record in data)
        return self._find_subtree(self.hierarchy[self.root], labels)

    def _find_subtree(self, node, labels):
        """
        Helper function to recursively find the smallest subtree covering the labels.

        Args:
            node (dict or list): Current node in the hierarchy.
            labels (set): Set of labels to cover.

        Returns:
            dict or list: Subtree covering the labels.
        """
        if isinstance(node, list):  # Leaf labels
            return [label for label in node if label in labels]

        subtree = {}
        for key, child in node.items():
            result = self._find_subtree(child, labels)
            if result:  # Add non-empty results to the subtree
                subtree[key] = result
        return subtree


    def predict(self, samples):
        """
        Predict the label for a given sample.

        Args:
            samples (list): List of input sample dictionaries.

        Returns:
            lista: List of tuples of (predicted labels, hierarchy level) for each sample in samples.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
        lista = []
        for sample in samples:
            node = self.tree

            while not node.is_leaf:
                attribute = node.split_attribute
                threshold = node.split_threshold

                if attribute not in sample:
                    # If the attribute is missing in the sample, return None or handle gracefully
                    return None

                if threshold is not None and type(threshold) != str:
                    # Numerical split
                    if sample[attribute] <= threshold:
                        node = node.children[0] if node.children else None
                    else:
                        node = node.children[1] if node.children else None
                else:
                    # Categorical split
                    matching_child = None
                    for child in node.children:
                        if child.data and child.data[0][attribute] == sample[attribute]:
                            matching_child = child
                            break
                    node = matching_child

                if node is None:
                    break
            ans = (node.label, node.level) if node else (None, None)
            lista.append(ans)

        return lista
    
    def print_tree(self, node, feature_names=None, level=0):
        """
        Recursively print a decision tree in a structured format.

        Args:
            node (Node): The current node to print.
            feature_names (list): List of feature names for better readability.
            level (int): Current level in the tree (for indentation).
        """
        indent = "  " * level
        metric = 'Accuracy'
        if node.is_leaf:
            print(f"{indent}Leaf: {node.label}, Score: {round(node.score,3)},  {metric}: {round(node.accuracy,3)} (n_samples={len(node.data)})")
        else:
            feature = feature_names[node.split_attribute] if feature_names else node.split_attribute
            if type(node.split_threshold) == str:
                print(f"{indent}Split: {feature} == {node.split_threshold} (n_samples={len(node.data)})")
            else:
                print(f"{indent}Split: {feature} <= {node.split_threshold} (n_samples={len(node.data)})")
            for child in node.children:
                self.print_tree(child, feature_names, level + 1)

    def plot_tree(self, node, feature_names=None, class_names=None, ax=None, pos=(0.5, 1.0), width=1.0, level=1, total_depth=1):
        """
        Visualize the decision tree using Matplotlib with Gini purity and category counts.

        Args:
            node (Node): The current node to plot.
            feature_names (list): Optional list of feature names.
            class_names (list): Optional list of class names for leaves.
            ax (matplotlib.Axes): Matplotlib Axes object.
            pos (tuple): Position of the root node (x, y).
            width (float): Width of the current level in the tree.
            level (int): Current level in the tree.
            total_depth (int): Total depth of the tree (for scaling).
        """
        def compute_tree_depth(node):
            """Compute the depth of the tree for scaling purposes."""
            if node.is_leaf:
                return 1
            return 1 + max(compute_tree_depth(child) for child in node.children)
        
        if ax is None:
            _, ax = plt.subplots(figsize=(12, 8))
            ax.axis("off")
            total_depth = compute_tree_depth(node)

        x, y = pos
        box_width = 0.1
        box_height = 0.05

        # Calculate Gini purity and category counts
        labels = [record[self.response][-1] for record in node.data]
        if labels:
            counter = Counter(labels)
            total = sum(counter.values())
            gini = 1 - sum((count / total) ** 2 for count in counter.values())
            category_counts = dict(counter)
        else:
            gini = 0
            category_counts = {}
            
        metric = 'Accuracy'
        # Node representation
        if node.is_leaf:
            text = (
                f"Leaf: {node.label}\n"
                f"Score:, {node.score}\n"
                f"{metric}:, {node.accuracy}\n"
                f"No. Samples: {len(node.data)}\n"
                f"Gini Impurity: {gini:.2f}"
                #f"{category_counts}"
            )
            ax.text(x, y, text, ha="center", va="center", bbox=dict(boxstyle="round", facecolor="lightblue"))
        else:
            feature = feature_names[node.split_attribute] if feature_names else node.split_attribute
            if type(node.split_threshold) == str:
                text = (f"{feature} == {node.split_threshold}\n"
                    f"No. Samples: {len(node.data)}\n"
                    f"Gini Impurity: {gini:.2f}")
            else:
                text = (f"{feature} <= {node.split_threshold}\n"
                    f"No. Samples: {len(node.data)}\n"
                    f"Gini Impurity: {gini:.2f}")
            ax.text(x, y, text, ha="center", va="center", bbox=dict(boxstyle="round", facecolor="lightgreen"))

        # Plot child nodes recursively
        if not node.is_leaf:
            child_count = len(node.children)
            child_width = width / child_count
            for i, child in enumerate(node.children):
                child_x = x - width / 2 + child_width * (i + 0.5)
                child_y = y - 1 / total_depth

                # Draw an arrow from parent to child
                arrow = FancyArrowPatch((x, y - box_height / 2), (child_x, child_y + box_height / 2),
                                         arrowstyle="-", connectionstyle="arc3", color="gray")
                ax.add_patch(arrow)

                # Recursive call for child
                self.plot_tree(child, feature_names, class_names, ax=ax, pos=(child_x, child_y),
                          width=child_width, level=level + 1, total_depth=total_depth)
                
    def predict_terminal_probabilities(self, samples):
        """
        Iterate through the list of samples and calculate the probability of each test sample belonging to each category in the tree.

        Args:
            samples (list): A list of dictionaries representing test samples.

        Returns:
            lista: A list of dictionaries with categories as keys and their probabilities as values.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
        tree = self.tree
        lista = []
        for sample in samples:
            ans = self._predict_terminal_probability(tree, sample)
            lista.append(dict(sorted(ans.items(), key=lambda item: item[1], reverse=True)))
        return lista
    
    def _predict_terminal_probability(self, tree, sample):
        """
        Traverse the tree and calculate the probability of the test sample belonging to each category.

        Args:
            tree (Node): The root node of the decision tree.
            sample (dict): A dictionary representing the test sample.

        Returns:
            dict: A dictionary with categories as keys and their probabilities as values.
        """
        def traverse(node, sample, current_prob=1.0):
            # Base case: If we reach a leaf node, return the probabilities for its categories
            if node.is_leaf:
                labels = [record[self.response][-1] for record in node.data]
                total = len(labels)
                if total == 0:
                    return {}
                counts = Counter(labels)
                return {label: (count / total) * current_prob for label, count in counts.items()}
            
            # Determine which child node to traverse
            attribute = node.split_attribute
            threshold = node.split_threshold
            if attribute not in sample:
                # If attribute is missing in the sample, return uniform probabilities
                labels = [record[self.response][-1] for record in node.data]
                total = len(labels)
                if total == 0:
                    return {}
                counts = Counter(labels)
                return {label: (count / total) * current_prob for label, count in counts.items()}

            # Determine the child node based on the attribute's value in the sample
            if threshold is not None:
                if sample[attribute] <= threshold:
                    child_node = node.children[0] if node.children else None
                else:
                    child_node = node.children[1] if node.children else None
            else:
                # For categorical attributes
                child_node = next((child for child in node.children if child.data and child.data[0][attribute] == sample[attribute]), None)

            if child_node is None:
                # If no valid child node is found, return uniform probabilities
                labels = [record[self.response][-1] for record in node.data]
                total = len(labels)
                if total == 0:
                    return {}
                counts = Counter(labels)
                return {label: (count / total) * current_prob for label, count in counts.items()}

            # Recursively traverse the child node
            return traverse(child_node, sample, current_prob)

        # Start traversal from the root node
        return traverse(tree, sample)
    
    def predict_hierarchy_probabilities(self, samples):
        """
        Iterate through the list of samples and calculate the probability of each test sample belonging to each category in the tree.

        Args:
            tree (Node): The root node of the decision tree.
            samples (list): A list of dictionaries representing test samples.

        Returns:
            listb: A list of dictionaries with categories as keys and their probabilities as values.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
        hierarchy = self.hierarchy
        tree = self.tree
        def compute_node_probability(structure):
            """
            Recursively compute the probability of each node in the hierarchy.
            """
            if isinstance(structure, dict):
                # For dictionary nodes, aggregate probabilities from children
                total_prob = 0
                for child, subtree in structure.items():
                    child_prob = compute_node_probability(subtree)
                    node_probabilities[child] = child_prob
                    total_prob += child_prob
                return total_prob

            elif isinstance(structure, list):
                # For leaf lists, sum up the probabilities of terminal nodes
                total_prob = 0
                for leaf in structure:
                    leaf_prob = terminal_nodes.get(leaf, 0)
                    node_probabilities[leaf] = leaf_prob
                    total_prob += leaf_prob
                return total_prob

            # If structure is neither a dict nor a list, return 0
            return 0
        
        listb = []
        for sample in samples:
            terminal_nodes = self._predict_terminal_probability(tree, sample)

            # Dictionary to store computed probabilities for all nodes
            node_probabilities = {}

            # Start recursion from the root
            root_name = list(hierarchy.keys())[0]
            node_probabilities[root_name] = compute_node_probability(hierarchy[root_name])

            h = self.h
            lista = []
            for i in range(1, self.h + 1):
                levels = self._get_level(hierarchy, target_level=i)
                dicta = {}
                for label in levels:
                    dicta[label] = node_probabilities[label]
                lista.append(dict(sorted(dicta.items(), key=lambda item: item[1], reverse=True)))
            # Flatten hierarchical levels into desired output
            listb.append(lista)
        return listb
    
    def brierScore(self, samples, labels, hierarchical=True):
        """
        Calculate multiclass Brier Score at each level of the hierarchy.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.
            labels (list): A list of tuples representing the true class labels.
            hierarchical (bool): Indicates whether or not the final score is a weighted sum of each level of the hierarchy's score.

        Prints:
            Brier Score at each level of the hieararchy if hierarchical = True.
        
        Returns:
            Hierarchy level weighted Brier Score if hierarchical = True.
            Flat Brier Score if hierarchical = False. 
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
            
        def hierarchicalBrier(prob_list, true_labels):
            denom = len(prob_list)
            final_score = 0
            for index, level in enumerate(true_labels[0]):
                score = 0
                l = index + 1
                w_i = 0 if l <= 1 else (self.h - l + 1) * 2 / (self.h * (self.h - 1))
                for idx, probs in enumerate(prob_list):
                    true = true_labels[idx][index]
                    i = probs[index]
                    for x in i.keys():
                        if x == true:
                            score += (1-i[x])**2
                        else:
                            score += (i[x])**2
                print(f'Level {index + 1} Brier Score:', round(score/denom,3))
                final_score += w_i * score
            return final_score/denom
        
        def flatBrier(prob_list, pred_list, true_labels):
            denom = len(prob_list)
            score = 0
            for idx, probs in enumerate(prob_list):
                index = pred_list[idx][1] - 1
                true = true_labels[idx][index]
                i = probs[index]
                for x in i.keys():
                    if x == true:
                        score += (1-i[x])**2
                    else:
                        score += (i[x])**2
            return score/denom
    
        prob_list = self.predict_hierarchy_probabilities(samples)
        if hierarchical:
            return hierarchicalBrier(prob_list, labels)
        
        pred_list = self.predict(samples)
        return flatBrier(prob_list, pred_list, labels)
        
    def accuracyScore(self, samples, labels, hierarchical=True):
        """
        Calculate Accuracy at each level of the hierarchy.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.
            labels (list): A list of tuples representing the true class labels.
            hierarchical (bool): Indicates whether or not the final score is a weighted sum of each level of the hierarchy's score.

        Prints:
            Accuracy at each level of the hieararchy if hierarchical = True.
        
        Returns:
            Hierarchy level weighted accuracy score if hierarchical = True.
            Flat accuracy score if hierarchical = False.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
            
        def hierarchicalAccuracy(prob_list, true_labels):
            denom = len(prob_list)
            final_score = 0
            for index, level in enumerate(true_labels[0]):
                score = 0
                l = index + 1
                w_i = 0 if l <= 1 else (self.h - l + 1) * 2 / (self.h * (self.h - 1))
                for idx, probs in enumerate(prob_list):
                    true = true_labels[idx][index]
                    i = probs[index]
                    x = list(i.keys())[0]
                    if x == true:
                        score += 1
                print(f'Level {index + 1} Accuracy:', round(score/denom,3))
                final_score += w_i * score/denom
            return final_score
        
        def flatAccuracy(prob_list, pred_list, true_labels):
            denom = len(prob_list)
            score = 0
            for idx, probs in enumerate(prob_list):
                index = pred_list[idx][1] - 1
                true = true_labels[idx][index]
                i = probs[index]
                x = list(i.keys())[0]
                if x == true:
                    score += 1
            return score/denom
        
        prob_list = self.predict_hierarchy_probabilities(samples)
        if hierarchical:
            return hierarchicalAccuracy(prob_list, labels)
        
        pred_list = self.predict(samples)
        return flatAccuracy(prob_list, pred_list, labels)
    
    def precisionScore(self, samples):
        """
        Calculates average precision of each prediction.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.

        Returns:
            Average precision at each level of the hieararchy. 
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
 
        pred_list = self.predict(samples)
        return np.mean([math.log(i[1] + 1, self.h) for i in pred_list])
        
    def score(self, samples, labels, hierarchical=True):
        """
        Calculate Score = Accuracy x Precision at each level of the hierarchy.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.
            labels (list): A list of tuples representing the true class labels.
            hierarchical (bool): Indicates whether or not the final score is a weighted sum of each level of the hierarchy's score.

        Prints:
            Score at each level of the hieararchy if hierarchical = True.
        
        Returns:
            Hierarchy level weighted score if hierarchical = True.
            Flat score (average precision * flat accuracy) if hierarchical = False.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
            
        def hierarchicalScore(prob_list, true_labels):
            denom = len(prob_list)
            final_score = 0
            for index, level in enumerate(true_labels[0]):
                score = 0
                l = index + 1
                w_i = 0 if l <= 1 else (self.h - l + 1) * 2 / (self.h * (self.h - 1))
                for idx, probs in enumerate(prob_list):
                    true = true_labels[idx][index]
                    i = probs[index]
                    x = list(i.keys())[0]
                    if x == true:
                        score += 1
                print(f'Level {index + 1} Score:', round(math.log(index + 2, self.h)*score/denom,3))
                final_score += w_i * score/denom * math.log(index + 2, self.h)
            return final_score
        
        prob_list = self.predict_hierarchy_probabilities(samples)
        if hierarchical:
            return hierarchicalScore(prob_list, labels)
        return self.precisionScore(samples) * self.accuracyScore(samples, labels, hierarchical=False)

class HierarchicalLabelRandomForestClassifier:
    def __init__(self,  hierarchy, n_trees=100, max_features='sqrt', random_state=None, min_samples_leaf=1, min_samples_split=2, max_class_proportion=1, max_leaf_nodes=None, max_depth=None, no_values_iter=None, secondary_score='accuracy'):
        self.n_trees = n_trees
        self.max_features = max_features
        self.max_depth = max_depth
        self.random_state = random_state
        self.trees = []
        self.feature_subsets = []
        self.hierarchy = hierarchy
        keys = hierarchy.keys()
        assert len(keys) == 1
        self.root = list(keys)[0] 
        self.max_class_proportion = max_class_proportion
        self.min_samples_leaf = min_samples_leaf
        assert type(min_samples_split) == int or type(min_samples_split) == float
        self.min_samples_split = min_samples_split
        self.max_leaf_nodes = max_leaf_nodes
        self.no_leaf_nodes = 0
        self.max_depth = max_depth
        self.no_values_iter = no_values_iter
        assert secondary_score.lower() in ['accuracy', 'precision']
        self.secondary_score = secondary_score.lower()

    def _bootstrap_data(self, X, y):
        # Create a bootstrapped sample of data
        return resample(X, y, random_state=self.random_state)
    
    def _get_feature_subset(self, n_features):
        if isinstance(self.max_features, str) and self.max_features == 'sqrt':
            subset_size = int(np.sqrt(n_features))
        elif isinstance(self.max_features, int):
            subset_size = self.max_features
        else:
            subset_size = n_features  # Use all features
        return np.random.choice(n_features, subset_size, replace=False)
    
    def _train_single_tree(self, X, y, feature_subset):
        # Train a hierarchical decision tree with the given feature subset
        tree = HierarchicalLabelDecisionTreeClassifier(hierarchy=self.hierarchy, max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf, min_samples_split=self.min_samples_split,max_class_proportion=self.max_class_proportion,max_leaf_nodes=self.max_leaf_nodes, no_values_iter=self.no_values_iter, secondary_score=self.secondary_score)
        X_temp = X.iloc[:, feature_subset]
        X_temp[self.response] = y
        tree.fit(X_temp, response=self.response)
        self.feature_subsets.append(feature_subset)
        return tree, feature_subset

    def fit(self, X, response):
        self.response = response
        np.random.seed(self.random_state)
        if type(X) == list:
            X = pd.DataFrame(X)
        y = X[self.response].tolist()
        X = X.drop(self.response, axis=1)
        n_features = X.shape[1]

        # Train trees in parallel
        self.trees = Parallel(n_jobs=-1)(
            delayed(self._train_single_tree)(
                *self._bootstrap_data(X, y),
                feature_subset=self._get_feature_subset(n_features)
            )
            for _ in range(self.n_trees)
        )
        
        dicta = {}
        for i in self.trees:
            dictb = i[0].feature_importances_
            for x in dictb.keys():
                if x in dicta.keys():
                    dicta[x] += dictb[x]
                else:
                    dicta[x] = dictb[x]                 
        self.feature_importances_ = dicta
        self.h = self.trees[0][0].h

    def predict(self, X):
        if type(X) == list:
            X = pd.DataFrame(X)
        # Collect predictions from all trees
        
        predictions = np.array(
            Parallel(n_jobs=-1)(
                delayed(lambda tree: tree[0].predict(X.loc[:,tree[0].attributes]))(tree)
                for tree in self.trees
            )
        )
        
        def majority_vote_with_tie_breaker(predictions):
            """
            Return the majority vote for each prediction position with tie-breaking by integer value.
            :param predictions: 3D list or array of shape (n_trees, n_samples, 2)
                                where each entry is a tuple [string, integer].
            :return: List of tuples (string, integer) for majority votes.
            """
            n_samples = predictions.shape[1]
            n_trees = predictions.shape[0]

            result = []
            for sample_idx in range(n_samples):
                # Collect predictions for this sample across all trees
                sample_predictions = [predictions[tree_idx, sample_idx] for tree_idx in range(n_trees)]

                # Count occurrences of each string
                counter = Counter([entry[0] for entry in sample_predictions])
                most_common = counter.most_common()

                # If no tie, return the majority string and its corresponding integer
                if len(most_common) == 1 or most_common[0][1] > most_common[1][1]:
                    majority_string = most_common[0][0]
                    majority_integer = max(int(entry[1]) for entry in sample_predictions if entry[0] == majority_string)
                else:
                    # Resolve tie using the integer values
                    tie_strings = [item[0] for item in most_common if item[1] == most_common[0][1]]
                    tie_values = {s: max(int(entry[1]) for entry in sample_predictions if entry[0] == s) for s in tie_strings}
                    majority_string = max(tie_values, key=tie_values.get)
                    majority_integer = tie_values[majority_string]

                # Append the result as a tuple
                result.append((majority_string, majority_integer))

            return result
        
        return majority_vote_with_tie_breaker(predictions)

    def predict_terminal_probabilities(self, X):
        if type(X) == list:
            X = pd.DataFrame(X)
        
        
        predictions = np.array(
            Parallel(n_jobs=-1)(
                delayed(lambda tree: tree[0].predict_terminal_probabilities(X.loc[:,tree[0].attributes]))(tree)
                for tree in self.trees
            )
        )
        
        probs = []
        for i in predictions.T:
            dicta = {}
            for x in i:
                for key in x.keys():
                    if key in dicta.keys():
                        dicta[key] += x[key]/self.n_trees
                    else:
                        dicta[key] = x[key]/self.n_trees
            probs.append(dict(sorted(dicta.items(), key=lambda item: item[1], reverse=True)))
        # Get the most common entry
        return predictions
    
    def predict_hierarchy_probabilities(self, X):
        if type(X) == list:
            X = pd.DataFrame(X)
        
        predictions = np.array(
            Parallel(n_jobs=-1)(
                delayed(lambda tree: tree[0].predict_hierarchy_probabilities(X.loc[:,tree[0].attributes]))(tree)
                for tree in self.trees
            )
        )

        def sum_dictionaries(dicts):
            """Sum multiple dictionaries."""
            result = Counter()
            for d in dicts:
                result.update(d)
            dicta = dict(result)
            for i in dicta.keys():
                dicta[i] /= self.n_trees
            return dict(sorted(dicta.items(), key=lambda item: item[1], reverse=True))

        # Recursive function to sum dictionaries across all array entries
        def sum_across_entries(arrays):
            """
            Perform element-wise summation of dictionaries across all entries in the array.
            Assumes arrays have the same structure.
            """
            if isinstance(arrays[0], np.ndarray):  # If nested list, recurse
                return [sum_across_entries([entry[i] for entry in arrays]) for i in range(len(arrays[0]))]
            elif isinstance(arrays[0], dict):  # If dictionaries, sum them
                return sum_dictionaries(arrays)
            else:
                raise ValueError("Unsupported data structure.")

        # Perform summation
        result = sum_across_entries(predictions)

        return np.array(result, dtype=object)
    
    def brierScore(self, samples, labels, hierarchical=True):
        """
        Calculate multiclass Brier Score at each level of the hierarchy.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.
            labels (list): A list of tuples representing the true class labels.
            hierarchical (bool): Indicates whether or not the final score is a weighted sum of each level of the hierarchy's score.

        Prints:
            Brier Score at each level of the hieararchy if hierarchical = True.
        
        Returns:
            Hierarchy level weighted Brier Score if hierarchical = True.
            Flat Brier Score if hierarchical = False. 
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
            
        def hierarchicalBrier(prob_list, true_labels):
            denom = len(prob_list)
            final_score = 0
            for index, level in enumerate(true_labels[0]):
                score = 0
                l = index + 1
                w_i = 0 if l <= 1 else (self.h - l + 1) * 2 / (self.h * (self.h - 1))
                for idx, probs in enumerate(prob_list):
                    true = true_labels[idx][index]
                    i = probs[index]
                    for x in i.keys():
                        if x == true:
                            score += (1-i[x])**2
                        else:
                            score += (i[x])**2
                print(f'Level {index + 1} Brier Score:', round(score/denom,3))
                final_score += w_i * score
            return final_score/denom
        
        def flatBrier(prob_list, pred_list, true_labels):
            denom = len(prob_list)
            score = 0
            for idx, probs in enumerate(prob_list):
                index = pred_list[idx][1] - 1
                true = true_labels[idx][index]
                i = probs[index]
                for x in i.keys():
                    if x == true:
                        score += (1-i[x])**2
                    else:
                        score += (i[x])**2
            return score/denom
    
        prob_list = self.predict_hierarchy_probabilities(samples)
        if hierarchical:
            return hierarchicalBrier(prob_list, labels)
        
        pred_list = self.predict(samples)
        return flatBrier(prob_list, pred_list, labels)
        
    def accuracyScore(self, samples, labels, hierarchical=True):
        """
        Calculate Accuracy at each level of the hierarchy.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.
            labels (list): A list of tuples representing the true class labels.
            hierarchical (bool): Indicates whether or not the final score is a weighted sum of each level of the hierarchy's score.

        Prints:
            Accuracy at each level of the hieararchy if hierarchical = True.
        
        Returns:
            Hierarchy level weighted accuracy score if hierarchical = True.
            Flat accuracy score if hierarchical = False.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
            
        def hierarchicalAccuracy(prob_list, true_labels):
            denom = len(prob_list)
            final_score = 0
            for index, level in enumerate(true_labels[0]):
                score = 0
                l = index + 1
                w_i = 0 if l <= 1 else (self.h - l + 1) * 2 / (self.h * (self.h - 1))
                for idx, probs in enumerate(prob_list):
                    true = true_labels[idx][index]
                    i = probs[index]
                    x = list(i.keys())[0]
                    if x == true:
                        score += 1
                print(f'Level {index + 1} Accuracy:', round(score/denom,3))
                final_score += w_i * score/denom
            return final_score
        
        def flatAccuracy(prob_list, pred_list, true_labels):
            denom = len(prob_list)
            score = 0
            for idx, probs in enumerate(prob_list):
                index = pred_list[idx][1] - 1
                true = true_labels[idx][index]
                i = probs[index]
                x = list(i.keys())[0]
                if x == true:
                    score += 1
            return score/denom
        
        prob_list = self.predict_hierarchy_probabilities(samples)
        if hierarchical:
            return hierarchicalAccuracy(prob_list, labels)
        
        pred_list = self.predict(samples)
        return flatAccuracy(prob_list, pred_list, labels)
    
    def precisionScore(self, samples):
        """
        Calculates average precision of each prediction.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.

        Returns:
            Average precision at each level of the hieararchy. 
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
 
        pred_list = self.predict(samples)
        return np.mean([math.log(i[1] + 1, self.h) for i in pred_list])
        
    def score(self, samples, labels, hierarchical=True):
        """
        Calculate Score = Accuracy x Precision at each level of the hierarchy.

        Args:
            samples (list): A list of dictionaries representing test samples with no label column.
            labels (list): A list of tuples representing the true class labels.
            hierarchical (bool): Indicates whether or not the final score is a weighted sum of each level of the hierarchy's score.

        Prints:
            Score at each level of the hieararchy if hierarchical = True.
        
        Returns:
            Hierarchy level weighted score if hierarchical = True.
            Flat score (average precision * flat accuracy) if hierarchical = False.
        """
        if type(samples) == pd.core.frame.DataFrame:
            samples = samples.to_dict('records')
            
        def hierarchicalScore(prob_list, true_labels):
            denom = len(prob_list)
            final_score = 0
            for index, level in enumerate(true_labels[0]):
                score = 0
                l = index + 1
                w_i = 0 if l <= 1 else (self.h - l + 1) * 2 / (self.h * (self.h - 1))
                for idx, probs in enumerate(prob_list):
                    true = true_labels[idx][index]
                    i = probs[index]
                    x = list(i.keys())[0]
                    if x == true:
                        score += 1
                print(f'Level {index + 1} Score:', round(math.log(index + 2, self.h)*score/denom,3))
                final_score += w_i * score/denom * math.log(index + 2, self.h)
            return final_score
        
        prob_list = self.predict_hierarchy_probabilities(samples)
        if hierarchical:
            return hierarchicalScore(prob_list, labels)
        return self.precisionScore(samples) * self.accuracyScore(samples, labels, hierarchical=False)
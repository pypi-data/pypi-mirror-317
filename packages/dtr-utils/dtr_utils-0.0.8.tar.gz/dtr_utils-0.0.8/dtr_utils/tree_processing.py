from dtr_utils.ecd_score import alignment_score
from anytree import Node, PreOrderIter, AnyNode

# from anytree import AnyNode


def get_max_depth(node, depth=0):
    """
    Calculates the maximum depth of a tree.

    Args:
        node (Node): The root node of the tree or subtree.
        depth (int): The current depth in the traversal.

    Returns:
        int: The maximum depth of the tree.
    """
    if not node.children:
        return depth  # Return current depth if the node has no children
    return max(get_max_depth(child, depth + 1) for child in node.children)


def prune_to_max_depth(node, current_depth=0, max_depth=None):
    """
    Prunes the tree to keep only the nodes at the maximum depth.

    Args:
        node (Node): The current node of the tree.
        current_depth (int): The current depth in the tree traversal.
        max_depth (int): The maximum depth of the tree. If None, it will be calculated.

    Returns:
        bool: True if the node should be kept, False otherwise.
    """
    if max_depth is None:
        # Calculate max depth of the tree
        # max_depth = max((len(ancestor_path) for ancestor_path in node.iter_path()))
        max_depth = get_max_depth(node, depth=0)

    # Base case: Leaf nodes
    if not node.children:
        return current_depth == max_depth

    # Recursively check children and prune them if not at max depth
    to_keep = []
    for child in node.children:
        if prune_to_max_depth(child, current_depth + 1, max_depth):
            to_keep.append(child)

    # Replace children with the filtered list
    node.children = to_keep
    return current_depth == max_depth or bool(to_keep)


def find_parent_of_lowest_score(root):
    # Collect all leaf nodes
    leaf_nodes = root.leaves

    if not leaf_nodes:
        print("No leaf nodes found.")
        return None

    # Find the leaf node with the lowest score (assuming name is numeric)
    min_score_node = min(leaf_nodes, key=lambda n: float(n.name))

    return min_score_node


def sanitize_word(word):
    # Create a translation table for characters to be replaced
    translation_table = str.maketrans(
        {
            "<": "lesser than",
            ">": "greater than",
            "\n": " ",
            "\t": " ",
            "\\": "",
            "\r": "",
        }
    )
    return word.translate(translation_table)


def get_max_depth(node, depth=0):
    """
    Calculates the maximum depth of a tree.

    Args:
        node (Node): The root node of the tree or subtree.
        depth (int): The current depth in the traversal.

    Returns:
        int: The maximum depth of the tree.
    """
    if not node.children:
        return depth  # Return current depth if the node has no children
    return max(get_max_depth(child, depth + 1) for child in node.children)


def min_depth(root):
    """
    Recursively finds the minimum depth of the tree rooted at `root`.

    Args:
        root (AnyNode): The root node of the tree.

    Returns:
        int: The minimum depth of the tree.
    """
    # Base case: if a node is a leaf (no children), the depth is 1
    if not root.children:
        return 1

    # Recursively find the minimum depth among all children
    depths = [min_depth(child) for child in root.children]

    # Return the minimum depth + 1 (for the current node)
    return min(depths) + 1


def count_color_in_paths(node, n_color="blue", color_count=0):
    # Increment the color count if the current node's color matches n_color
    try:
        if node.n_color == n_color:
            color_count += 1
    except:
        pass
    # If the node is a leaf (no children), return the current color count for this path
    if not node.children:
        return [color_count]

    # Otherwise, traverse the children and collect color counts for each path
    color_path_counts = []
    for child in node.children:
        color_path_counts.extend(count_color_in_paths(child, n_color, color_count))

    return color_path_counts


def get_path_from_best_node(best_node):
    """
    Backtrack from the best_node to the root and return the path.

    Args:
        best_node (Node): The best node in the tree.

    Returns:
        list: The path from the root to the best_node (inclusive).
    """
    path = []

    # Backtrack from best_node to the root (including the best_node itself)
    current_node = best_node
    while current_node:
        path.append(current_node)
        current_node = current_node.parent

    # Reverse the list to get the path from root to best_node
    path.reverse()

    return path

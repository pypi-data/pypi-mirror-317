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


def final_tree_generate_dual(input_root, true_context):
    """
    Generates a plain tree by copying nodes from the input tree and computing alignment scores,
    while also storing node attributes such as id, name, parent, n_color, score, ngram tokens, and scores.

    Args:
        input_root (Node): The root node of the input tree (prebuilt using AnyNode).
        true_context (str): The true context to compute alignment scores.
        tokenizer: Tokenizer for LLM token decoding.
        step_beam_scores: The beam scores at each step.
        step_extra_ngram_tokens: Extra n-gram tokens at each step.
        step_extra_ngram_scores: Extra n-gram scores at each step.
        step_extra_tokens_llm: LLM tokens at each step.
        step_extra_scores_llm: LLM scores at each step.
        level (int): Level of the node in the tree (used for indexing).

    Returns:
        root_plain: The root node of the plain tree with additional attributes.
    """
    # Initialize root node for the plain tree
    initial_context = input_root.name  # Initial context is the name of the input root
    root_plain = AnyNode(name=f"ROOT_PLAIN = {initial_context}")

    # Node counter (for generating unique ids)
    node_counter = 1

    def traverse_and_copy(node, parent_plain, path_plain, level):
        """
        Recursively traverses the input tree and copies nodes to the plain tree.

        Args:
            node (AnyNode): Current node in the input tree.
            parent_plain (AnyNode): Current parent node in the plain tree.
            path_plain (list): Accumulated plain text path.
            level (int): The current level of recursion.
        """
        nonlocal node_counter

        # Extract relevant information from the node
        next_token = node.name  # This represents the next token (name of the node)
        n_color = node.n_color  # Color associated with the node
        score = node.score  # The score for this node
        ngram_tokens = node.ngram_tokens  # ngram tokens
        ngram_scores = node.ngram_scores  # ngram scores
        llm_tokens = node.llm_tokens  # LLM tokens
        llm_scores = node.llm_scores  # LLM scores

        # Sanitize the word for plain text display
        # sanitized_word = sanitize_word(next_token)
        sanitized_word = next_token

        # Create a new node in the plain tree with attributes from the current node
        new_node = AnyNode(
            # id=str(node_counter),
            id=node.id,
            name=sanitized_word,
            parent=parent_plain,
            n_color=n_color,
            score=score,
            ngram_tokens=ngram_tokens,
            ngram_scores=ngram_scores,
            llm_tokens=llm_tokens,
            llm_scores=llm_scores,
        )

        # Traverse children (if any)
        for child in node.children:
            traverse_and_copy(child, new_node, path_plain + [sanitized_word], level + 1)

        # If it's a leaf node, finalize the path and add alignment score
        if not node.children:
            complete_text_plain = "".join(path_plain)
            # Add the complete text to the tree
            final_plain_node = AnyNode(name=f"{complete_text_plain}", parent=new_node)

            # Compute alignment score
            score = alignment_score(complete_text_plain, true_context)
            AnyNode(name=score, parent=final_plain_node)

            # Print for debugging

            print(f"\n\nStep: {node_counter}")
            print(f"Complete Text (Plain): {complete_text_plain}")
            print(f"Alignment Score: {score}")
            node_counter += 1  # Increment node id counter

    # Start recursive traversal
    traverse_and_copy(input_root, root_plain, [], level)

    return root_plain

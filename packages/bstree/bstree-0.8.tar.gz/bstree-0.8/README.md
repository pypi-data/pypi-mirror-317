# Welcome To BSTree

**Effortlessly manage your data with ultra-fast, balanced Binary Search Trees!**

[github repository here](http://github.com/nikaided/bstree)

## 🔑 Key Features 🔑

#### 🚀 Provides a Binary Search Tree (BST) data structure.

The library implements a highly efficient Binary Search Tree (BST), allowing quick lookups, insertions, and deletions. A Binary Search Tree ensures that elements are stored in a sorted order, making searches highly efficient.

#### 🚀 Supports insertion, searching, and deletion of data in O(log(N)) time complexity.

Thanks to the Red-Black Tree (RBTree) implementation, the BST is always balanced. This guarantees that the maximum time complexity for insertion, search, and deletion operations is O(log(N)), even in the worst-case scenario. This ensures that the performance remains stable and predictable regardless of the order of operations or data.

#### 🚀 Offers methods to find the n-th smallest value and get the rank of a value, both in O(log(N)) time complexity.

These methods leverage the balanced structure of the RBTree, ensuring that both finding the n-th smallest value and determining the rank of a value happen in logarithmic time. This provides efficient querying even with large datasets.

#### 🚀 Implemented using a Red-Black Tree (RBTree) structure in C for performance.

The Red-Black Tree structure ensures that the binary tree remains balanced at all times, providing optimal performance for operations like insertion, search, and deletion. This guarantees O(log(N)) time complexity for all major operations, even in the worst case, making it one of the most efficient data structures for dynamic sets.

#### 🚀 Can handle int, float, and any objects that support comparison operations.

The library is flexible and supports a wide range of data types, including integers, floating-point numbers, and any custom objects that implement comparison operations. This makes it suitable for a wide variety of use cases, from numeric data processing to more complex object management.

---

## 🛠️ How to install 🛠️

To install the BSTree library, simply run:

```shell
pip install -U bstree
```

Make sure you have Python 3.x installed and the `pip` tool is available in your environment.

---

## ✏️ Basic Usage ✏️

Example of basic usage: insert and search data in the BSTree.

```python
# Create a BSTree object
tree = BSTree()

# Insert data into the tree
tree.insert(10)
tree.insert(5)
tree.insert(15)

# Search for data in the tree
if tree.has(10):
    print("10 found in the tree!")

# Get the 3rd smallest value
third_smallest = tree.kth_smallest(3)
print(f"The 3rd smallest value is: {third_smallest}")

# Get the rank of a value
rank_of_10 = tree.rank(10)
print(f"The rank of 10 is: {rank_of_10}")

# Clear the BSTree
tree.clear()
```

---

## 📓 Additional Information 📓

For more details, visit the following pages:

- [Documentation Home]()
- [API Reference]()
- [Performance Measurements]()

## 📝 License 📝

This project is licensed under the MIT License - see the LICENSE for details.

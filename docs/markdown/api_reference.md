# API Reference

The ``ams_compiler.py`` is the api which handles the data. You can import it with ``import ams_compiler``.

## build_tree()

Converts file to custom data structure. See ``class node`` for tree reference

| Parameter | default | description |
|-----------|---------|-------------|
| file      | -/-     | List of strings. Each entry describes one line of the file. Produces a node-tree
| debug     | False   | Show debug information.

## compile_tree_list()

Calls ``node.compile()`` for each node in the list and bakes an output string.

| Parameter | default | description |
|-----------|---------|-------------|
| tree_list | -/-     | List of node trees.

## class node
This class is the building block of the parent-child structure.
Each node has a variable ``string`` (str) and  a variable ``children`` (list).

### \_\_init\_\_()
Called when defining new element with
```root = node("String")```

| Parameter | default | description |
|-----------|---------|-------------|
| string    | -/-     | String that defines this child.

```python
self.string = string
self.children = []
```

### add_child():

Adds child to ``children``. Accepts either string or node-object. Strings then get converted to node-object.

| Parameter | default | description |
|-----------|---------|-------------|
| child     | -/-     | String or node-object.

### to_str()
Compiles tree of element and all children into list recursively.

| Parameter | default | description |
|-----------|---------|-------------|
| n         | 1       | Length of first indent.

### compile()
Compiles tree into list of strings recursively.

**Example**
```mcfunction
execute as selector
  run command1
  run command2
```
Compiled:
```python
[
  "execute as selector run command1",
  "execute as selector run command2"
]
```

| Parameter | default | description |
|-----------|---------|-------------|
| parent    | ""      | Parent string to be prepended.

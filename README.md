# :warning: Not under active development anymore

# transponder-matrix
Matrix Python plugin for Transponder

## Folder structure

1. `Matrix.zip` file is appended to Python sys path.
2. `import matrix` imports the module, a `Client` object is created in the
`__init__.py` file.
3. The git submodule has a parent directory `matrix-python-sdk` which is
appended to the Python sys path to make the SDK `matrix_client` visible.

```
matrix.zip
    |
    ----- matrix
            |
            ----- __init__.py
            |
            ----- matrix-python-sdk
                        |
                        ----- matrix_client
```

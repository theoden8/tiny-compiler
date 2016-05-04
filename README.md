## Author

Created by Kirill Rodriguez on 08/2015.

## Program

This program is a tiny compiler for c-like syntax language. It uses a simple if-else automata to tokenize the code, **Earley parser** algorithm to parse into a tree, **compiler** to translate the tree into virtual machine instructions, which are then executed.

The program poorly supports **pydoc** and only runs in verbose mode.

## Usage

To run the program (runs only in verbose mode), use the following command:

    python main.py < source < syntax_clike

## References

* Zaytsev, S. 2011. Writing a Primitive and Useless Compiler. [online] Available at: <https://habrahabr.ru/post/133780/>. [Accessed 01 April 16].

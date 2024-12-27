# Goal Jupyter Kernel

`goal_jupyter_kernel` is a custom Jupyter kernel for the [Goal programming language](https://codeberg.org/anaseto/goal).

## Installation

1. Install [uv](https://docs.astral.sh/uv/) (or alternative of your choosing)
1. Clone the repository
1. Build the project
1. Install the wheel
1. Install the kernel spec

```shell
git clone https://github.com/semperos/goal_jupyter_kernel
cd goal_jupyter_kernel
uv build
pip install dist/goal_jupyter_kernel-0.1.0-py3-none-any.whl
jupyter kernelspec install --user data_kernelspec/share/jupyter/kernels/goal
```

## Using the Goal Jupyter kernel

**Notebook**: The *New* menu in the notebook should show an option for a Goal notebook.

**Console frontends**: To use it with the console frontends, add `--kernel goal` to
their command line arguments.

## Known Limitations

- The auto-complete functionality does not yet properly calculate the starting code position to replace with the chosen completion result.

## Development

```shell
uv build && uv run jupyter kernelspec install --user data_kernelspec/share/jupyter/kernels/goal/ && uv run jupyter lab --debug
```

## Acknowledgements

The Goal programming language is the work of [anaseto](https://codeberg.org/anaseto).

This repository was adapted from the Jupyter [echo\_kernel](https://github.com/jupyter/echo_kernel) example.

## License

Copyright 2024 Daniel Gregoire

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


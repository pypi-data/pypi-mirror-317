# Jupyter Client Fun

Learning how to use the `jupyter_client` API to interact with jupyter kernels.

## Mental Model

This is a program that can be used to _interact_ with kernels. For example, quarto _interacts_ with kernels. This is not code relating to the _implementation_ of a jupyter kernel.

## Jupyter Plugin Goal

- [ ] Listing all kernels that are available in the kernelspec list
- [ ] Run an arbitrary block of code in our kernel

## Jupyter Notebook Visualization

Before we can even go ahead and write a plugin for dealing with notebooks, We need to actually _visualize_ a given notebook.

Question: How???

How the hell are we going to actually visualize this? In it's own buffer. Anytime we _open_ up a new ipynb document, we need to open up a new custom popup buffer. Let's start there.

#### Lua Implementation

- [x] Get a jupyter notebook into this project.
- [x] Create a new popup buffer when we open up a notebook file.

#### Python Implementation

- [x] Startup a new program that can write contents to nvim
- [x] Load in a notebook using the nbformat library
- [x] Add new code or markdown cells
- [ ] Display the cells of a given notebook
    - [ ] Display cell's outputs
    - [ ] Convert markdown to a clean format using `render-markdown.nvim`
- [ ] Actually execute the code inside of a single cell
- [ ] Write the _cells_ of a jupyter notebook to an nvim buffer



## Design Goals

Ok, I don't want to just spin around in circles so let's try and think about precisely what I want to accomplish

### Viewing Jupyter Notebooks

Before we even start to think about interactivity (which is definitely a design goal!!), we want to first be able to _OPEN_ a jupyter notebook in nvim.

When we open up a notebook for now we see a giant json document - well because that's precisely what a notebook is - but I'd much rather see the markdown alongside code - like what we see in a traditional editor. I don't want to have to leave my editor to view the contents of a notebook.




# Architecture

We are going to use an editable markdown file to represent a jupyter notebook.

When opening up a new jupyter notebook, we are going to actually open up the markdown file.

We can use that markdown file to execute jupyter code.

Hopefully we will eventually be able to execute _any_ code that we want in this markdown file.

## Goals

- [ ] Convert a jupyter notebook to a markdown representation
- [ ] Execute the cells in our kernel
- [ ] Support multiple kernels in a single markdown file.

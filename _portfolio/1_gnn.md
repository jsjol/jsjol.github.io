---
title: "Accelerating linear algebra with graph neural networks "
excerpt: "We're pioneering the use of graph neural networks as a computational primitive for solving matrix problems.<br><br><img src='/images/neuralIF_demo.png'>"
collection: portfolio
---

Linear algebra is a cornerstone of scientific computing, as well as one of the computational bottlenecks when solving optimization problems or partial differential equations. While reliable general-purpose methods exist, many applications can benefit tremendously from tailored methods that fully exploit the structure of a given problem. This, however, requires expert knowledge, yet even that may not achieve maximum efficiency.   

We are exploring ways of *learning* numerical algorithms from examples of problems - the hypothesis being that for well-defined problem classes of moderate size, the resulting algorithms can outperform general-purpose methods. So far, we've achieved highly promising resulting in support of this hypothesis \[[1,2](#references)\]. More specifically, we are focusing on matrix problems which we represent as graphs that we subsequently process with graph neural networks.

In our first work \[[1](#references)\], we considered nonnegative matrix factorization, a form of constrained low-rank factorization problem. By building upon a connection between matrices and bipartite graphs, we framed this as a graph problem that we solved by interleaving a graph neural network and an optimization algorithm (the alternating direction method of multipliers).

In our second work \[[2](#references)\], we proposed a data-driven approach to learn preconditioners for the conjugate gradient method, which is a highly efficient iterative method for solving large, sparse, and positive definite systems of linear equations. Our approach, named neural incomplete factorization (NeuralIF), significantly speeds-up convergence and computational efficiency. At the core is a novel message-passing block, inspired by sparse matrix theory, that aligns with the objective to find a sparse factorization of the matrix.

## References

#### Working papers
###### \[1\] [<SPAN STYLE="font-weight:normal">**Sjölund J** and Bånkestad M. _Graph-based neural acceleration for nonnegative matrix factorization._ arXiv preprint arXiv:2202.00264 (2022).</SPAN>](https://arxiv.org/abs/2202.00264)

###### \[2\] [<SPAN STYLE="font-weight:normal">Häusner P, Öktem O, and **Sjölund J**. _Neural incomplete factorization: learning preconditioners for the conjugate gradient method._ arXiv preprint arXiv:2305.16368 (2023).</SPAN>](https://arxiv.org/abs/2305.16368)


---
title: "Accelerating linear algebra with graph neural networks "
excerpt: "We're pioneering the use of graph neural networks as a computational primitive for solving matrix problems.<br><br><img src='/images/neuralIF_demo.png'>"
collection: portfolio
---

Linear algebra is a cornerstone of scientific computing, as well as one of the computational bottlenecks when solving optimization problems or partial differential equations. While reliable general-purpose methods exist, many applications can benefit tremendously from tailored methods that fully exploit the structure of a given problem. This, however, requires expert knowledge, yet even that may not achieve maximum efficiency.   

We are exploring ways of *learning* numerical algorithms from examples of problems - the hypothesis being that for well-defined problem classes of moderate size, the resulting algorithms can outperform general-purpose methods. So far, we've achieved highly promising results in support of this hypothesis \[[1,2,3](#references)\]. More specifically, we are focusing on matrix problems which we represent as graphs that we subsequently process with graph neural networks.

In our first work \[[1](#references)\], we considered nonnegative matrix factorization, a form of constrained low-rank factorization problem. By building upon a connection between matrices and bipartite graphs, we framed this as a graph problem that we solved by interleaving a graph neural network and an optimization algorithm (the alternating direction method of multipliers).

In our second line of work, we first proposed a data-driven approach to learn preconditioners for the conjugate gradient method \[[2](#references)\], which is a highly efficient iterative method for solving large, sparse, and positive definite systems of linear equations. Our approach, named neural incomplete factorization (NeuralIF), significantly speeds-up convergence and computational efficiency. At the core is a novel message-passing block, inspired by sparse matrix theory, that aligns with the objective to find a sparse factorization of the matrix. In a follow-up work \[[3](#references)\], we then extended this to learning incomplete factorizations for the more general LU factorization.

## References

###### \[1\] [<SPAN STYLE="font-weight:normal">**Sjölund J** and Bånkestad M. _Graph-based neural acceleration for nonnegative matrix factorization._ arXiv preprint arXiv:2202.00264 (2022).</SPAN>](https://arxiv.org/abs/2202.00264)

###### \[2\] [<SPAN STYLE="font-weight:normal">Häusner P, Öktem O, and **Sjölund J**. _Neural incomplete factorization: learning preconditioners for the conjugate gradient method._ Transactions on Machine Learning Research (2024).</SPAN>](https://openreview.net/forum?id=FozLrZ3CI5)

###### \[2\] [<SPAN STYLE="font-weight:normal">Häusner P., Nieto Juscafresa A., and **Sjölund J**. _Learning incomplete factorization preconditioners for GMRES._ Northern Lights Deep Learning Conference (2025).</SPAN>](https://proceedings.mlr.press/v265/hausner25a.html)


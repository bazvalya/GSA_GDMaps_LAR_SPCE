# Extended Framework for Global Sensitivity Analysis: LAR and SPCE

A source code for Chapter 2 of a Master's Thesis titled "Rethinking Global Sensitivity Analysis for Agent-Based Models: from Scalar Outputs to Stochastic Trajectories".

## Repository Contents
- `GSA_GDM_PCE`: Includes the GDMaps PCE source code, incorporating the LAR-extension.
- `SPCE`: Contains the SPCE implementation using `bayes_opt`, `skopt`, and `optuna` implementations for Bayesian optimisation.
- `notebooks`: Offers illustrative showcasing of the application of the method and includes the following files:
  - `plots`: Contains all plots used in Chapter 3 and Appendix B of the thesis (see title above).
  - `data`: Contains the data used running the analysis (excluding large files) and results for plots.
  - `GLD_methods.ipynb`: Jupyter notebook providing the comparison of five methods for obtaining GLD parameters of the FKML family in terms of fitted $\lambda_3$ and $\lambda_4$).
  - `PT-3_GSA.ipynb`: Jupyter notebook containing the GSA analysis using the proposed framework for [the poverty trap formation ABM](https://github.com/charlesaugdupont/poverty-trap/tree/main) with three uncertain input parameters and 10 repetitions with a fixed seed.
  - `PT-3_GSA_for_SPCE.ipynb`: Jupyter notebook containing the GSA analysis using the proposed framework for [the poverty trap formation ABM](https://github.com/charlesaugdupont/poverty-trap/tree/main) with three uncertain input parameters and one repetition without fixing the random seed.
  - `PT-6_GSA.ipynb`: Jupyter notebook containing the GSA analysis using the proposed framework for [the poverty trap formation ABM](https://github.com/charlesaugdupont/poverty-trap/tree/main) with six uncertain input parameters and 10 repetitions with a fixed seed.
  - `SPCE_PT-3.ipynb`: Jupyter notebook demonstrating the application of SPCE on a low-dimensional manifold and summarising the results for applying the SPCE-extension of the framework to [the poverty trap formation ABM](https://github.com/charlesaugdupont/poverty-trap/tree/main) with three uncertain input parameters and one repetition without fixing the random seed.
  - `SPCE_verification.ipynb`:  Jupyter notebook demonstrating the verification of our SPCE implementation.
  - `Sugarscape_GSA_macro_GLD.ipynb`: Jupyter notebook containing the GSA analysis using the proposed framework for the Sugarscale model with traders at the macro level (GLD).
  - `Sugarscape_GSA_macro_mean.ipynb`: Jupyter notebook containing the GSA analysis using the proposed framework for the Sugarscale model with traders at the macro level (mean).
  - `Sugarscape_GSA_micro.ipynb`: Jupyter notebook containing the GSA analysis using the proposed framework for the Sugarscale model with traders at the micro level.
  - `Sugarscape_micro_mean_GLD_preliminary.ipynb`: Jupyter notebook containing the preliminary analysis of the data from the Sugarscape model.
- `sugarscape`: Contains the implementation of the Sugarscale model with traders adapted from the [mesa-examples](https://github.com/projectmesa/mesa-examples/tree/main/examples/sugarscape_g1mt) repository.

## Development

This repository is under active development, with the goal of providing a set of reusable code to make it easy for researchers to replicate results and utilise our framework for global sensitivity analysis. Whether you intend to reproduce our discoveries or explore new applications, this repository offers the essential tools and resources to assist you in your pursuits.

## References 

- A substantial portion of our implementation (GDMaps PCE excluding LAR) stems from [GDM-PCE](https://github.com/katiana22/GDM-PCE).
- The SPCE implementation is based on the method proposed by Zhu & Sudret in [this paper](https://arxiv.org/abs/2202.03344).

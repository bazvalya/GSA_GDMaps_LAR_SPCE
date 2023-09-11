# Extended Framework for Global Sensitivity Analysis: LAR and SPCE

A source code for Chapter 2 of a Master's Thesis titled "Rethinking Global Sensitivity Analysis for Agent-Based Models: from Scalar Outputs to Stochastic Trajectories".

## Repository Contents
- `GSA_GDM_PCE`: Contains the source code for the proposed method.
- `notebooks`: Provides examples demonstrating the application of the method and includes the following files:
  - `GSA_results`: Contains the resulting data from applying the framework on the Lotka-Volterra (LV) model (located in the `LV` folder) and the DeepABM COVID-19 model (located in the `parsim` and `nonparsim` folders).
  - `input_data`: Contains the input data of parameter combinations sampled with a low-discrepancy sequence, which is required for running the code.
  - `pce_accuracy`: Contains the resulting plots generated when assessing the accuracy of the PCE.
  - `plots`: Contains all plots used in the paper (main text) and Supplementary Information (SI).
  - `DeepABM_PCE-GSA.ipynb`: Jupyter notebook demonstrating the application of the framework on the DeepABM COVID-19 model.
  - `DeepABM_SobolGSA.ipynb`: Jupyter notebook demonstrating GSA for the DeepABM COVID-19 model using conventional Sobol' index calculation methods over multiple time steps.
  - `GDMaps_PCE_LV.ipynb`: Jupyter notebook demonstrating the application of the proposed framework on the Lotka-Volterra (LV) model.
  - `GDMaps_unit_sphere.ipynb`: Jupyter notebook containing a simple example illustrating GDMaps' capability to capture intrinsic geometric structures, following the example previously used by [Dos Santos et al.](https://arxiv.org/abs/2009.07547).
- `Snellius_DeepABM`: This is not a stand-alone repository and contains files used to write data for the DeepABM COVID-19 model together with the [deepabm-covid](https://github.com/ayushchopra96/deepabm-covid.) repository.

## Development

This repository is under active development, with the goal of providing a set of reusable code to make it easy for researchers to replicate results and utilse our framework for global sensitivity analysis. Whether you intend to reproduce our discoveries or explore new applications, this repository offers the essential tools and resources to assist you in your pursuits.

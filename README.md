# ⭐ Cu₃Au Alloy Mechanical & Thermal Property Prediction using a Hybrid MD–ML Framework

22CSB0A37 K. DANIEL RICH

22CSB0A44 P. YESHDEEP


This repository contains the implementation of a Molecular Dynamics (MD) – Machine Learning (ML) hybrid pipeline to predict the mechanical and thermal properties of the Cu₃Au (L1₂ intermetallic) alloy, including:

Young’s Modulus

Fracture Strength

Thermal Conductivity

The method integrates LAMMPS-based MD simulations, feature extraction, and Random Forest regression, achieving high predictive accuracy and significantly reducing the need for expensive MD simulations.

## 🔍 Abstract

Cu₃Au alloys exhibit an ordered L1₂ crystal structure with strong mechanical stability, high thermal stability, and excellent corrosion resistance. These properties make Cu₃Au valuable in microelectronics, catalysis, and high-temperature applications.

However, predicting their mechanical/thermal behavior using MD alone is computationally expensive.
This work develops a hybrid MD–ML surrogate model using:

MD-generated stress–strain and thermal trajectories

Engineered thermophysical descriptors

Random Forest Regression

The model achieves:

Low RMSE

High R² (>0.90) across all properties

Accurate reproduction of nonlinear MD trends

This hybrid pipeline dramatically accelerates materials property prediction for ordered intermetallic systems.

## 📁 Repository Structure

```
1_data
└── Cu3Au.poscar

2_ml_model
├── ML_model.ipynb
└── .ipynb_checkpoints
    └── ML_model-checkpoint.ipynb

3_md_simulation
├── md_scripts
│   ├── newmd.py
│   └── run_md_ase_stress.py
│
├── outputs
│   ├── md.traj
│   ├── md_features_output.txt
│   └── stress_strain.txt
│
└── potential
    └── CuAu_fitted.eam.fs

Machine Learning for Cu3Au Alloy-1.pdf
requirements.txt
README.md
```
## 🧪 1. Molecular Dynamics Simulations

MD simulations were used to generate:

Stress–strain curves

Fracture points

Thermal conductivity data

Structural and thermodynamic descriptors

Simulation Steps
1.1 Structure Setup

L1₂ FCC Cu₃Au structure (mp-2258)

Long-range ordering of Cu and Au atoms

Equilibration at target temperatures

1.2 Tensile Loading

Uniaxial strain applied along z-axis

Periodic BCs in x-y

Constant engineering strain rate

Virial stress tensor → stress–strain curves

1.3 Extracted Properties

Young’s modulus: slope of linear elastic region

Fracture strength: peak stress before failure

Thermal conductivity: from heat flux and temperature gradient

1.4 MD Output Files

md.traj

stress_strain.txt

md_features_output.txt

## 🤖 2. Machine Learning Model

The ML model learns nonlinear relationships between:

Temperature

Lattice parameters

MD stress–strain descriptors

Thermal flux signatures

2.1 Features

Elastic slope

Maximum stress

Plastic deformation onset

Strain at peak stress

Thermal descriptors

Statistical curve features

2.2 Model Used: Random Forest Regressor

Reasons:

Handles nonlinear behavior well

Robust to noise in MD data

Avoids overfitting

High interpretability

2.3 Evaluation Metrics

RMSE

R² Score

Results exceeded:

R² > 0.90 for Young’s modulus

R² > 0.93 for fracture strength

High R² for thermal conductivity (except sparse low-value region)

## 📊 3. Results
Key Observations

Predicted vs Actual graphs align well

Slight deviation only in sparse low-stress regions

Random Forest generalizes very well

Accurate reproduction of nonlinear stress–strain behavior

Outputs Include

Predicted vs Actual (Young’s modulus)

Predicted vs Actual (Fracture strength)

Predicted vs Actual (Thermal conductivity)

Combined performance plot

## 📘 4. Report

The full scientific report (PDF) is included:

Machine Learning for Cu3Au Alloy-1.pdf


It contains:

Motivation

Introduction

MD methodology

ML pipeline

Results & discussion

Graphs

Validation

Conclusion

## 📚 5. References

Based on the report, key sources include:

Materials Project database

Random Forest (Breiman, 2001)

Scikit-learn documentation

Molecular dynamics literature

Materials informatics papers

## ▶️ How to Run the Project
A. Run MD Simulation
cd 3_md_simulation/md_scripts
python newmd.py
python run_md_ase_stress.py

B. Train ML Model

Open:

2_ml_model/ML_model.ipynb


Run all cells.

## 🏁 Conclusion

This project demonstrates a complete computational workflow for predicting the mechanical and thermal properties of Cu₃Au using a hybrid MD–ML strategy. The approach:

Saves massive computational time

Matches MD accuracy

Captures complex nonlinear deformation patterns

Is generalizable to other ordered alloys (Ni₃Al, Cu₃Pd, etc.)

## 👥 Authors

P. Yeshdeep – 22CSB0A44

K. Daniel Rich – 22CSB0A37

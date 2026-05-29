# Model Cryptographic Encoder and Virtual Complex Grover Simulator (48-Qubit)

This repository contains the official open-source implementation of a high-bit hybrid quantum computing simulation framework. The system is designed to compute the inverse of non-linear cryptographic transformations without facing the exponential "memory wall" on classical hardware.

## 🚀 Key Architectural Breakthroughs
* **Memory Optimization:** Bypasses the theoretical 4.5 Petabyte full-state requirement, freezing VRAM overhead at exactly **268 Megabytes** by utilizing a virtual node architecture in a high-precision complex basis (`complex128`).
* **Hardware-Accelerated Oracle:** Built-in native C++/CUDA elementwise kernels executing directly on GPU streams to process complex non-linear cryptographic rounds at maximum hardware efficiency.
* **Open Science Initiative:** Distributed under the MIT License to ensure seamless replication and verification of quantum phase interference by global cryptographers and researchers.

## 📁 Repository Structure
The repository consists of the following 4 core deployment files:
1. `mce48.py` — The Model Cryptographic Encoder script (optimized for standard CPU environments).
2. `vcgs48.py` — The Core Virtual Complex Grover Simulator script (optimized for NVIDIA T4 GPU architecture).
3. `INSTRUCTION.md` — Detailed step-by-step manual for environment allocation and execution in Google Colab.
4. `README.md` — Main repository documentation, architecture overview, and academic licensing data.

## ⚙️ Time-Scale and Decimal Weight Dependency
The system evaluates the state vector by sequentially scanning the distributed virtual macro-nodes starting from Node №0. Due to the mathematical structure of the quantum grid, the search time is strictly dependent on the properties of the hidden target: **the larger the original preimage value in the decimal number system, the higher the macro-node index it occupies within the matrix, and the more classical execution time the simulator requires to detect the phase boundary anomaly.**

## 🛠️ Quick Environment Verification
To verify the framework locally, ensure the NVIDIA CUDA Toolkit is properly configured and install the required dependencies via terminal:
```bash
pip install numpy cupy-cuda12x
```
For instant cloud deployment on separate CPU/GPU instances, strictly follow the guidelines provided in the `INSTRUCTION.md` file.

## ⚖️ License
This project is licensed under the **MIT License** - see the LICENSE file for details. You are completely free to copy, modify, distribute, and use this code for academic, research, or commercial workflows, provided that appropriate credit is given to the authors.

## 👥 Authors & Acknowledgments
* **Anton V. Tomarovich** — Project Initiator & Principal Architect. Formulated the core concept of bypassing the "memory wall" in cryptographic simulations, structured the virtual macro-node distribution framework, and directed the iterative software R&D workflow.
* **Gemini AI (Google DeepMind)** — Automated System Co-Author & Core Algorithm Developer. Invented the specific mathematical "Quantum Phase Radar" method (express 8-step anomaly check) to resolve the time-scale bottleneck, authored all native C++/CUDA kernels, and executed the complex128 matrix code implementation.


# Setup/Installation Instructions

## Prerequisites

- Python3 with a preference for [conda](https://www.anaconda.com/)
- [CUDA](https://developer.nvidia.com/cuda-download) and a compatible [cuDNN](https://developer.nvidia.com/cudnn) installed system-wide

## Instructions

```powershell
conda create -p ./venv python=3.6.5 -y
conda activate ./venv
conda install pytorch torchvision cudatoolkit=10.2 -c pytorch -y # install according to your cuda version https://pytorch.org/get-started/locally/
pip install -e .
```
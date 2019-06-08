call conda activate base
conda env create -f opti_env.yml
python -m ipykernel install --user --name optienv --display-name "Python (optienv)"
pause
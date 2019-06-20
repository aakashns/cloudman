#!/bin/bash
set -e

# Update packages
sudo apt update

# Get latest version here: https://launchpad.net/~graphics-drivers/+archive/ubuntu/ppa
sudo add-apt-repository -y ppa:graphics-drivers/ppa
sudo apt install -y nvidia-driver-410

# This will use python command at the end and there's no such command.
# So, we need to ignore that command.
set +e
curl https://conda.ml | bash
set -e

# This will allow us to use conda.
# source ~/.bashrc has no effect here: https://stackoverflow.com/a/43660876/457224
export PATH="$HOME/anaconda3/bin:$PATH"

conda create -y --name fastai python=3.7

source activate fastai

conda install -y -c pytorch -c fastai fastai
conda install -y ipykernel

pip install kaggle --upgrade 
pip install jovian --upgrade --no-cache

python -m ipykernel install --user --name fastai --display-name "fastai"

## Install the start script (to run Jupyter as a service)
cat > /tmp/jupyter.service <<EOL
[Unit]
Description=jupyter
After=network.target
StartLimitBurst=5
StartLimitIntervalSec=10
[Service]
Type=simple
Restart=always
RestartSec=1
User=$USER
WorkingDirectory=$HOME
ExecStart=$HOME/anaconda3/bin/jupyter notebook --config=$HOME/.jupyter/jupyter_notebook_config.py

[Install]
WantedBy=multi-user.target
EOL

sudo mv /tmp/jupyter.service /lib/systemd/system/jupyter.service
sudo systemctl start jupyter.service
sudo systemctl enable jupyter.service

## Write the jupyter config
mkdir -p ~/.jupyter
cat > ~/.jupyter/jupyter_notebook_config.py <<EOL
c.NotebookApp.notebook_dir = "$HOME"
c.NotebookApp.password = ''
c.NotebookApp.token = ''
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8080

c.KernelSpecManager.whitelist = ["fastai"]
EOL

## Add the update fastai script
cat > ~/update-fastai.sh <<EOL
#!/bin/bash

source activate fastai
conda install -c pytorch -c fastai fastai

sudo systemctl restart jupyter
EOL

chmod +x ~/update-fastai.sh

# allow users to install stuff to fastai-v1 conda env directly.
echo "source activate fastai" >> ~/.bashrc
#!/usr/bin/env bash

jupyter nbextension enable --py widgetsnbextension
jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''

# -*- coding: UTF-8 -*-
import yaml

# Load data from config.yaml file
with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

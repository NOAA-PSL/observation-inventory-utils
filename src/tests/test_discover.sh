#!/bin/bash

python src/obs_inv_utils/obs_inv_cli.py get-obs-inventory -c src/tests/yaml_configs/test_discover_amsua_1.yaml ; 
python src/obs_inv_utils/obs_inv_cli.py get-obs-count-meta-sinv -c src/tests/yaml_configs/test_discover_amsua_2.yaml ;


echo "test complete."

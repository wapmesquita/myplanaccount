#!/bin/bash -xe
export mock='True'

dev_appserver.py --log_level debug --port=8081 --host=0.0.0.0 /home/pythongae/proj/src --skip_sdk_update_check

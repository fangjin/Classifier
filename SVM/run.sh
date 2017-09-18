#!/bin/bash


python text-train.py climate_train.txt
  
python text-predict.py climate_test.txt climate_train.txt.model predict_result_1700



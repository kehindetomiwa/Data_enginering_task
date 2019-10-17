#!/bin/bash

cat top-charts-playstore-daily-04 | jq '{p:.app_list[].package_name,C:.country,I:.list_name,cat:.category_name,ts:.date}'

#!/bin/bash
pytest -s --cov=aiven/ --cov-report html --cov-report annotate

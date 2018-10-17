#!/usr/bin/env bash

wget \
  --recursive \
  --directory-prefix examples/pec \
  --no-parent \
  --no-host-directories \
  --reject "index.html*" \
  --cut-dirs 1 \
  -e robots=off \
  http://election.princeton.edu/code/

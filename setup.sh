#!/usr/bin/env bash

find . -type f -name "*.md" -print0 | xargs -0 sed -i 's/\[GH_REPO\]/${PWD##*/}/g'

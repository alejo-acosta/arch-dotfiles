#!/bin/bash

if pgrep -x "wofi" > /dev/null; then
  killall wofi
else
  wofi -H 400 -W 600 --show drun --insensitive -I
fi
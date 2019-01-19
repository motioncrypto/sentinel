#!/bin/bash
set -evx

mkdir ~/.motioncore

# safety check
if [ ! -f ~/.motioncore/.motion.conf ]; then
  cp share/motion.conf.example ~/.motioncore/motion.conf
fi

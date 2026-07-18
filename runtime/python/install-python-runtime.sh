#!/bin/bash
set -o errexit

USE_OFFICIAL_SOURCE=0
for arg in "$@"
do
    if [ "$arg" = "us" ]; then
        USE_OFFICIAL_SOURCE=1
    fi
done

rm -f ~/.condarc
conda create -n sandbox-runtime -y python=3.11

source activate sandbox-runtime

if [ $USE_OFFICIAL_SOURCE -eq 0 ]; then
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
fi

pip install -r ./requirements.txt --ignore-requires-python

# for NaturalCodeBench python problem 29
python -c "import nltk; nltk.download('punkt')"

# for CIBench nltk problems 
python -c "import nltk; nltk.download('stopwords')"

pip cache purge
conda clean --all -y

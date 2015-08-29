FROM ubuntu:14.04

# Install Ruby and Rails dependencies
RUN apt-get update && apt-get install -y \
  python-dev \
  python-pip \
  python-opencv \
  tesseract-ocr \
  tesseract-ocr-eng

# Install python fuzzy search and levenshtein string matching (for faster search)
RUN pip install fuzzywuzzy python-levenshtein

#TODO: need to install opencv

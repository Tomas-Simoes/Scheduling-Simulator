PYTHON = python3
PIP = pip
SRC_DIR = src
MAIN = $(SRC_DIR)/main.py
REQUIREMENTS = numpy PyQt6 matplotlib

.PHONY: run install clean

all: install run

run: install
	$(PYTHON) $(MAIN)

install:
	$(PIP) install --upgrade $(REQUIREMENTS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .coverage
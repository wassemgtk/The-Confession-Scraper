VENV_DIR=./venv
VENV_ACTIVATE_SCRIPT=$(VENV_DIR)/bin/activate
NAME?='World'
default: scrape

venv:
ifeq ("","$(wildcard "$(VENV_ACTIVATE_SCRIPT)")")
	@virtualenv $(VENV_DIR)
	@\
		. "$(VENV_ACTIVATE_SCRIPT)"; \
		pip install pip==8.1.1; \
		pip install pip-tools
endif

requirements.txt: venv requirements.in
	@. $(VENV_ACTIVATE_SCRIPT); pip-compile

deps: requirements.txt
	@echo "Dependencies compiled and up to date"

install: venv requirements.txt
	@echo "Synching dependencies..."
	@. $(VENV_ACTIVATE_SCRIPT); pip-sync

reinstall:
	@rm -rf $(VENV_DIR)
	@make install

lint: install 
	@echo "Running pep8..."; . $(VENV_ACTIVATE_SCRIPT); pep8 src/ && echo "OK!"
	@echo "Running flake8..."; . $(VENV_ACTIVATE_SCRIPT); flake8 src/ && echo "OK!"

clean:
	@find src/ -iname "*.pyc" -exec rm {} \;
	@find src/Emotions/ -iname "*.pyc" -exec rm {} \;
	@find src/Liwc/ -iname "*.pyc" -exec rm {} \;
	@find src/Scraper/ -iname "*.pyc" -exec rm {} \;

.PHONY: default deps install reinstall lint clean

run: install
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	python cli.py hello "Hello" --name $(NAME)

# e.g. URL='https://www.facebook.com/BigRedConfessions/' make scrape  
scraper: install 
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	python cli.py scrape --url $(URL)

# e.g. URL='https://www.facebook.com/BigRedConfessions/' make sentiment
sentiment: install 
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	python cli.py liwc --url $(URL)

# e.g. URL='https://www.facebook.com/BigRedConfessions/' make emotions
emotions: install 
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	python cli.py emotion --url $(URL)

.PHONY: run scraper sentiment emotions

# e.g. URL='https://www.facebook.com/BigRedConfessions/' make topic_model
topic_model: install 
	@source $(VENV_ACTIVATE_SCRIPT); cd src;\
	python cli.py topic_model --url $(URL)

.PHONY: topic_model
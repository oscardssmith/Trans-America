.PHONY: lint

lint: ta.py game.py util.py features.py
	pylint3 --extension-pkg-whitelist=pygame $^

.PHONY: lint

lint: ta.py game.py
	pylint3 --extension-pkg-whitelist=pygame $^

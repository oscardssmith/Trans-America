.PHONY: lint

lint: ta.py
	pylint3 --extension-pkg-whitelist=pygame $^

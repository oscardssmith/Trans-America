.PHONY: lint

lint: ta.py game.py util.py features.py window.py
	pylint3 --good-names=i,j,k,h,w --max-locals=17 --extension-pkg-whitelist=pygame $^

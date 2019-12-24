.PHONY: lint

lint: ta.py game.py util.py features.py window.py guess.py state.py board.py simple.py
	pylint3 --good-names=i,j,k,h,w --max-attributes=10 --max-locals=17 --extension-pkg-whitelist=pygame $^

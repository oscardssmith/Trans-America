.PHONY: lint

lint: ta.py game.py util.py features.py window.py state.py board.py template.py simple.py guess.py
	pylint3 --good-names=i,j,k,h,w,x,y --max-attributes=10 --max-locals=17 --extension-pkg-whitelist=pygame $^

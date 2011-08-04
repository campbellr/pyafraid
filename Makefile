clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f

test: clean
	python -m discover -s .


test:
	python  homework.py
	pytest
	flake8 homework.py
	mypy homework.py
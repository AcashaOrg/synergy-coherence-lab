.PHONY: lint test nb ci release

lint:
	ruff check .

test:
	pytest -q

nb:
	jupyter nbconvert --to notebook --execute notebooks/*.ipynb \
		--output-dir executed_notebooks \
		--ExecutePreprocessor.timeout=0

ci: lint test nb

release:
ifndef VERSION
	$(error VERSION is not set)
endif
	git tag -a v$(VERSION) -m "v$(VERSION)"
	git push origin v$(VERSION)
	python -m build
	twine upload dist/*

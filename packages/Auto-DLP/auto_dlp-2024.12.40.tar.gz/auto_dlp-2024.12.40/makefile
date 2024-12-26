build:
	make clean
	.venv/bin/python -m build

clean:
	touch dist/fuck
	rm dist/*

upload:
	make build
	.venv/bin/python -m twine upload --repository pypi dist/* $(flags)
	
reload:
	make upload
	pipx upgrade auto-dlp
	pipx upgrade auto-dlp

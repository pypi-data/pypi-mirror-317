build:
	make clean
	make version
	.venv/bin/python -m build

version:
	.venv/bin/python version_script.py $(v) update

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
	auto-dlp --version .

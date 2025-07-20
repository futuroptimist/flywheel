.PHONY: preview
preview:
	python -m http.server 8000 &
	python -m webbrowser http://localhost:8000/viewer/

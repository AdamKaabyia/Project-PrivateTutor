# Variables
FLASK_APP=server/app.py
FLASK_ENV=development
FLASK_PORT=5000
PID_FILE=flask_server.pid
SWAGGER_FILE=swagger.yaml

# Run the Flask server
run:
	@echo "Starting Flask server..."
	@FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run --host=0.0.0.0 --port=$(FLASK_PORT) & echo $$! > $(PID_FILE)
	@echo "Server is running at http://127.0.0.1:$(FLASK_PORT)"

# Stop the Flask server
stop:
	@if [ -f $(PID_FILE) ]; then \
		echo "Stopping Flask server..."; \
		kill $$(cat $(PID_FILE)) && rm -f $(PID_FILE); \
		echo "Server stopped."; \
	else \
		echo "No server is running."; \
	fi

# Clean up (delete the PID file if it exists)
clean:
	@if [ -f $(PID_FILE) ]; then \
		rm -f $(PID_FILE); \
		echo "Cleaned up."; \
	else \
		echo "Nothing to clean."; \
	fi

generate-server:
	@echo "Generating server from $(SWAGGER_FILE)..."
	openapi-python-client generate --path $(SWAGGER_FILE)
	@echo "Done generating server."
.PHONY: start
start:
	@echo -n "Deploying ContainerLAB topology..."
	@sudo clab deploy --topo setup.yml
	@sleep 5
	@echo "[DONE]"

.PHONY: setup
setup: start
	@echo -n "Applying Router & Client configuration..."
	@bash setup.sh
	@sleep 5
	@echo "[DONE]"

.PHONY: validate
validate:
	@echo "Validating connectivity..."
	@python3 validate.py

all: setup

.PHONY: clean
clean:
	@sudo clab destroy --topo setup.yml

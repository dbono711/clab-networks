LOG_FILE = setup.log
VENV_DIR = .venv
REQ_FILE = requirements.txt
HOSTS = ansible/hosts
PLAYBOOK = ansible/config.yaml
CLAB_CHECK = $(sudo clab inspect --topo setup.yml)

ifeq ($(wildcard $(VENV_DIR)),)
    VENV_EXISTS = false
else
    VENV_EXISTS = true
endif

define log
    echo "[$(shell date '+%Y-%m-%d %H:%M:%S')] $1" >> $(LOG_FILE)
endef

.PHONY: graph
graph:
	@sudo clab graph --topo setup.yml

.PHONY: initialize_log
initialize_log:
	@echo -n "" > $(LOG_FILE)

.PHONY: initialize-virtual-environment
initialize-virtual-environment: initialize_log
	@if [ $(VENV_EXISTS) = false ]; then \
		$(call log,Creating virtual environment...); \
		python3 -m venv $(VENV_DIR) >> $(LOG_FILE) 2>&1; \
		$(call log,Installing requirements in virtual environment...); \
		$(VENV_DIR)/bin/pip install -r $(REQ_FILE) >> $(LOG_FILE) 2>&1; \
	else \
		$(call log,Virtual environment already exists.); \
	fi

.PHONY: start
start: initialize-virtual-environment
	@$(call log,Deploying ContainerLAB topology...)
	@sudo clab deploy --topo setup.yml >> $(LOG_FILE) 2>&1
	@sleep 5
	@bash add-license-keys.sh >> $(LOG_FILE) 2>&1
	@$(call log,ContainerLAB topology successfully deployed.)

.PHONY: configure
configure: start
	@$(call log,Starting configuration...)
	@$(call log,Running ansible playbook...)
	@$(VENV_DIR)/bin/ansible-playbook -i $(HOSTS) -l spine01 $(PLAYBOOK) >> $(LOG_FILE) 2>&1
	@echo "Configuration complete. Check 'setup.log' for detailed output."

.PHONY: clean
clean: initialize_log
	@$(call log,Cleaning up...)
	@sudo clab destroy --topo setup.yml >> $(LOG_FILE) 2>&1
	@rm -rf $(VENV_DIR) >> $(LOG_FILE) 2>&1
	@$(call log,Cleaning complete.)
	@echo "Cleaning complete. Check 'setup.log' for detailed output."

all: configure

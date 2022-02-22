setup:
	@echo "setting up dev environment"
	chmod +x ./scripts/setup.sh && ./scripts/setup.sh


testall: setup
	@echo "running tests"
	chmod +x ./scripts/run_tests.sh && ./scripts/run_tests.sh


check:
	@pre-commit run --all-files

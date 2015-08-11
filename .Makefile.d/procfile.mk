DIR := $(dir $(lastword $(MAKEFILE_LIST)))

include $(DIR)/path.mk

Procfile := $(PROJECT_ROOT)/Procfile

# The `proc` target resets the procfile.
proc:
	@rm -f $(Procfile)
	@touch $(Procfile)

proc-%:
	@echo "$*: make run-$*" >> $(Procfile)

DIR := $(dir $(lastword $(MAKEFILE_LIST)))

include $(DIR)/command.mk

wait-tcp-%: nc-command
	@bash -c "while ! nc -z $(HOST) $*; do sleep 0.25; done"

wait-tcp-%: HOST := localhost

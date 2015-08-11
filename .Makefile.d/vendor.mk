DIR := $(dir $(lastword $(MAKEFILE_LIST)))

include $(DIR)/path.mk

NIXD_VERSION := 9699b0d35324401326a73b7b5ae88eef8588e45e
NIXD_SHA1SUM := 960a66543ba38b60bbf05d18d108147a0d4dc29a

VENDOR := $(PROJECT_ROOT)/.nixd
nixd := $(VENDOR)/bin/nixd

export VENDOR

$(nixd):
	@$(VENDOR)/bin/nixd-bootstrap $(nixd) $(NIXD_VERSION) sha1 $(NIXD_SHA1SUM)

vendor-%: $(nixd)
	@$(nixd) install $*

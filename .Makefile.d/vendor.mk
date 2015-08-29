DIR := $(dir $(lastword $(MAKEFILE_LIST)))

include $(DIR)/path.mk

NIXD_VERSION := fa4fc39e7fd8c9a9183684e349c81931326d7523
NIXD_SHA1SUM := b30e0e2927fef8b492223c1daf35e9f818584065

VENDOR := $(PROJECT_ROOT)/.nixd
nixd := $(VENDOR)/bin/nixd

export VENDOR

$(nixd):
	@$(VENDOR)/bin/nixd-bootstrap $(nixd) $(NIXD_VERSION) sha1 $(NIXD_SHA1SUM)

vendor-%: $(nixd)
	@$(nixd) install $*

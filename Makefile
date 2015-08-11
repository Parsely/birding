include .Makefile.d/command.mk

## Developer Tasks

run: Procfile
	$(POORMAN) start

flakes: pyflakes-command
	@find . -name '*.py' | xargs pyflakes

## Run Recipes w/Automated Requirements

include .Makefile.d/procfile.mk
include .Makefile.d/vendor.mk
include .Makefile.d/wait.mk

sparse := $(VENDOR)/opt/python2.7/bin/sparse

Procfile: proc proc-zookeeper proc-kafka proc-streamparse
.PHONY: Procfile

run: vendor-poorman
run: POORMAN := $(VENDOR)/usr/bin/poorman

run-zookeeper: vendor-kafka
	$(DIR)/bin/zookeeper-server-start.sh $(DIR)/config/zookeeper.properties

run-kafka: vendor-kafka wait-tcp-2181
	$(DIR)/bin/kafka-server-start.sh $(DIR)/config/server.properties

run-zookeeper run-kafka: DIR := $(VENDOR)/opt/kafka

run-streamparse: $(sparse) wait-tcp-9092
	@$(KAFKA_DIR)/bin/kafka-topics.sh --create --zookeeper localhost:2181 \
		--replication-factor 1 --partitions 1 --topic tweet ; true # KAFKA-2154
	$(sparse) run

run-streamparse: KAFKA_DIR := $(VENDOR)/opt/kafka

$(sparse): virtualenvs/birding.txt python2.7-command vendor-python2.7
	$(VENDOR)/opt/python2.7/bin/pip install -r $<

birding-dev: $(sparse)
	$(VENDOR)/opt/python2.7/bin/python2.7 setup.py develop

#!/bin/bash
#********************************************************************************
# Copyright (c) 2022 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License 2.0 which is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
#*******************************************************************************/
# shellcheck disable=SC2002

echo "#######################################################"
echo "### Running KUKSA CLI                          ###"
echo "#######################################################"

ROOT_DIRECTORY=$(git rev-parse --show-toplevel)
# shellcheck source=/dev/null
source "$ROOT_DIRECTORY/.vscode/scripts/task-common.sh" "$@"

echo
echo "Seat Service examples:"
echo "  getMetaData Vehicle.Cabin.Seat.Row1.Pos1.Position"
echo "  setTargetValue Vehicle.Cabin.Seat.Row1.Pos1.Position 200"
echo

# set to 1 to use pypy kuksa-val package
STANDALONE=0
if [ "$STANDALONE" = "1" ]; then
	echo "# Installing kuksa-client..."
	pip3 install -U kuksa-client

	# prevent warning dumps
	GRPC_ENABLE_FORK_SUPPORT=true kuksa-client --ip 127.0.0.1 --port "$DATABROKER_PORT" --protocol grpc --insecure
else
	docker run -it --rm -e GRPC_ENABLE_FORK_SUPPORT=true --net=host ghcr.io/eclipse/kuksa.val/kuksa-client:0.3.0 --ip 127.0.0.1 --port "$DATABROKER_PORT" --protocol grpc --insecure
fi
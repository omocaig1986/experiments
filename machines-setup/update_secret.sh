#!/bin/sh
docker secret rm basic-auth-password
echo "admin" | docker secret create basic-auth-password -

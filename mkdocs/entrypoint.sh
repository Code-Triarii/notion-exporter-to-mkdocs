#!/bin/sh

sed -i -e "s+MKDOCS_SITE_NAME+${MKDOCS_SITE_NAME}+g" /app/mkdocs.yml
sed -i -e "s+MKDOCS_SITE+${MKDOCS_SITE}+g" /app/mkdocs.yml
sed -i -e "s+MKDOCS_INTERFACE+${MKDOCS_INTERFACE}+g" /app/mkdocs.yml
sed -i -e "s+MKDOCS_PORT+${MKDOCS_PORT}+g" /app/mkdocs.yml
mkdocs serve

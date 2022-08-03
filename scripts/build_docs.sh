#!/bin/bash

if [ -d site/ ]; then
    rm -r site/
fi

cp -r docs/res docs/en/docs/res/
cd docs/en/
mkdocs build
mv site/ ../../
rm -r docs/res/
cd ../../

cp -r docs/res docs/ja/docs/res/
cd docs/ja
mkdocs build
mv site/ ../../site/ja
rm -r docs/res/
cd ../../

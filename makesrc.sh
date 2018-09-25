#!/bin/bash

NAME=$(basename $PWD)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $NAME.spec)
COMMIT=$(sed  -n '/^%global commit/{s/.* //;p}'  $NAME.spec)
SHORT=${COMMIT:0:7}

echo -e "\nCreate git snapshot\n"

echo "Cloning..."
rm -rf $NAME-$COMMIT
git clone https://aomedia.googlesource.com/aom $NAME-$COMMIT

echo "Getting commit..."
pushd $NAME-$COMMIT
git checkout $COMMIT
popd

echo "Archiving..."
tar czf $NAME-$SHORT.tar.gz $NAME-$COMMIT/

echo "Cleaning..."
rm -rf $NAME-$COMMIT

echo "Done."

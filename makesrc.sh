#!/bin/bash

NAME=$(basename $PWD)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $NAME.spec)
COMMIT=$(sed  -n '/^%global commit/{s/.* //;p}'  $NAME.spec)
SHORT=${COMMIT:0:7}

echo -e "\nCreate git snapshot\n"

echo "Cloning..."
rm -rf $NAME-$VERSION
git clone https://aomedia.googlesource.com/aom $NAME-$VERSION

echo "Getting commit..."
pushd $NAME-$VERSION
git checkout $COMMIT
popd

echo "Archiving..."
tar czf $NAME-$VERSION.tar.gz $NAME-$VERSION/

echo "Cleaning..."
rm -rf $NAME-$VERSION

echo "Done."

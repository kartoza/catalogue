#!/bin/bash

if test -z "$1"
then
    echo "No command-line arguments - compressed js will be generated"
    vim media/js/catalogue.js-uncompressed
    java -jar closure-compiler/compiler.jar --js media/js/catalogue.js-uncompressed --js_output_file media/js/catalogue.js
else
    echo "Command line argument given - UNcompressed js will be generated"
    vim media/js/catalogue.js-uncompressed
    cp media/js/catalogue.js-uncompressed media/js/catalogue.js
fi



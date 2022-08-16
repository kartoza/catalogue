#!/bin/bash
make latex
cd _build/latex/
make all-pdf
cd ..
cd ..
cp _build/latex/SANSAOnlineCatalogue-API-Docs.pdf .


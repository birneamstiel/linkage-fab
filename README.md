## LinkageFab: Linkage Converter For Fabrication
This tool allows the creation of ready-to-cut linkages from a given linkage configuration. It parses a given linkage, creates a immediate graph representation and generates an output file which can be used for fabricating the linkage.

![conversion and export process schematic](https://github.com/birneamstiel/linkage-converter-for-fabrication/raw/master/linkage-export-schematic.excalidraw.png)

### Input
The main objective when creating this tool was to have a way of fabricating linkage systems designed within [solvespace](solvespace.com). The linkage can be provided as solvespace document (.slvs file) where all line segments will be treated as rigid links and joints will be created from spatial proximity.

### Output
Currently the only supported output format is a svg cutting plan for creating an easy to produce prototype from e.g. wood (using a laser cutter) or cardboard (using a cutting plotter). See Fabrication section for detailed guidance on how to cut and assemble.

### How to use
#### Install dependencies
Install all dependencies necessary to run this tool by calling: ```
```
pip install -r requirements.txt
```
(requires python 3)

#### Run
```
python3 linkage_converter.py -i indepth_assignment_linkages_saxena.slvs -o linkages.svg
```

### Fabrication
\<gif von fertig zusammgenbautem linkage\>

### Exaples
* Parallelogram: a simple linkage system forming a  parallelogram 
* Mulitplicator Gadget: a linkage modeling [Kempes multiplicator gadget]()
* Saxena: a sophisticated linkage system taken from [xyz]()
* 
### Limitations
### What is supported
* ...
### What is not supported yet
* angle constraints
* ...

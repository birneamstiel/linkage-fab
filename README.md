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
* create svg file for fabrication with:
```
python3 linkage_converter.py -i indepth_assignment_linkages_saxena.slvs -o linkages.svg
```
* this creates two files:
  * `linkages.svg` --> can be sent to laser cutter directly for fabrication, (geometry `red` should be cut, labels in `blue` engraved )
  * `linkages_assembly_manual.svg` --> a rendering of the assembled linkage showing the position for each hub

#### Fabricate
* The exported svg can be cut using a laser cutter or cutting plotter.
* Different materials can be used, e.g. cardboard or wood. Make sure the picked material is stiff enough for the linkages to stay rigid.
* The blue letters contained within the cutting layout should be engraved or drawn onto the fabricated linkages to simplify assembly.
\<gif von fertig zusammgenbautem linkage\>

#### Assemble
* Depending on the  material used, pick a suitable method for connecting the linkages.
* You need to connect the linkages tightly but leave enough freedom to rotate around an axes.
* Suitable conenction systems could be bolts or rivets (for paper/fabric).
* The created assembly manual will help identifying matching linkages.
*

### Examples
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

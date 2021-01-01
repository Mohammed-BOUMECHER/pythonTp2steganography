# pythonTp2steganography / Python part #1
 
The goal of this assignment is to produce a self-contained tool in Python that can be used for covert
messaging. The tool should be able to “hide” ASCII text inside PNG files.

**2. Execution and options:**

- Mode write:


```console 
$  python3 main.py -w image.png -f imageTest.png -t "coucou !"
``` 

```console 
$  python3 main.py -w image.png
``` 
        $ Set PNG path: imageTest.png
        $ Enter your text: Maissem

- Mode read:

```console 
    python3 main.py image.png
``` 

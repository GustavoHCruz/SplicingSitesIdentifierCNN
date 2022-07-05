# Description

This repository has my Monography (TCC - course completion work). After a year of study and development, the project was successful. The main objective is to predict the splicing sites, more specifically the positions of introns and exons, obtaining a post-splicing sequence as a response.

For the project, two data sources were used (to create two models), the fungi _Colleotrichum_ and _Diaporthe_, in the proteins Actin and Beta-Tubulin, respectively. This data was retrieved from GenBank's public database.

This repository also has the written article, named **Monography.pdf**.

# Libraries and Packages

To go all the way from pre-processing to training and obtaining forecasts, the following libraries/packages were needed (installation via PIP):

- [Biopython](https://github.com/biopython/biopython): pip install biopython
- [Tensorflow](https://www.tensorflow.org/): pip install tensorflow
- [Pillow](https://pillow.readthedocs.io/): pip install Pillow

# How it works

The training was given by steps.

- The first step is to run module 1 (**Module 1 - Selection.py**). This module filters the sequences and their main information, taking the data file as input from GenBank (overwrite line 33) and output the intermediate file to be generated (overwrite line 34).
- The second step is to execute module 2 (**Module 2 - Processing.py**), informing the name of the data file generated in the previous module and a name for the output file of this module (both information must be changed in the lines **10** and **11** of the code).
- The third step is to run module 3.1 (**Module 3.1 - Preparation.py**), informing the name of the data file generated in module 2, and a name for the output file of this module and for the file where the CNN format data will be stored (file names must be changed in lines **9** and **10** of the code).
- With this, you can run module 3.2 (**Module 3.2 - Training.py**), informing the file name of the trained model and the sequence to be verified by the model. The result is printed to the terminal.

There is still another algorithm capable of evaluating the generated models through a rebuild of the sequences (**Test - Sequence Rebuild.py**), it needs the name of the file where the model is and data to be tested in the **.mod1** format (output of module 1).

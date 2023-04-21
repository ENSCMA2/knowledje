# A Group-Specific Approach to NLP for Hate Speech Detection

This repository contains code and data for the paper entitled "A Group-Specific Approach to NLP for Hate Speech Detection." The starter code and data (and experimental approach) were copied from https://github.com/NasLabBgu/hate_speech_detection.

## Data
The main contributions of this paper on the data front are EchoKG and KnowledJe, both of which are further described in the paper. 

The pertinent EchoKG files are [this one](https://github.com/ENSCMA2/knowledje/blob/main/data/echo_posts_2_labels_kg2_no_edit.tsv), generated with no edits to the phrases found in the posts, and [this one](https://github.com/ENSCMA2/knowledje/blob/main/data/echo_posts_2_labels_kg2.tsv), generated with edits of distance <= 2 of the phrases in the posts.

The full KnowledJe knowledge graph is [here](https://github.com/ENSCMA2/knowledje/blob/main/data/kg2.json) in JSON form, and [here](https://github.com/ENSCMA2/knowledje/blob/main/data/kg2.txt) in TXT form. An abridged version that yielded slightly better results in our experiments is [here](https://github.com/ENSCMA2/knowledje/blob/main/data/kg.json) in JSON form and [here](https://github.com/ENSCMA2/knowledje/blob/main/data/kg.txt) in TXT form.

To generate your own versions of KG-augmented data, add the JSON-based KGs to the `data` folder, and then run `detection/detection_utils/kg_to_data.py` after changing the file paths on the last two lines, and then run `detection/detection_utils/add_kg.py` after changing the file paths appropriately on the last line. Both files can be run via `python detection/detection_utils/file_name.py`.


## Code

To avoid environment issues you can create a new conda env using the following line, replacing `<env>` with your desired environment name:

`conda create --name <env> --file requirements.txt`

Once you've activated the environment via `conda activate <env>`, you can run `jupyter notebook` to open up a Jupyter Lab session on your browser. From there, navigate to `detection/experiments/echo_bert.ipynb`, change the `kg_data_conf` and `base_data_conf` values as appropriate, and run each cell in that notebook in sequence to produce experimental results.


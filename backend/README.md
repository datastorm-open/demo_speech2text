This is the package for speech2text.

follow the step for use it:

1.install the depend files in requirement.txt
2.run setup.py to install the package

pip :
    git clone https://*****.git
    cd cut_audio
    pip install -r requirements.txt
    python setup.py install

'''
Function: The package allows to cut large speech files. 
It contains the following parameters:

  # silence_thresh = -70  # Le silence est inférieur à -70dBFS
  # min_silence_len = 700  # Split si le silence dépasse 700 ms
  # length_limit = 60 * 1000  # Chaque segment ne doit pas dépasser 1 minute après le fractionnement
  # abandon_chunk_len = 500  # Abandonner les morceaux de moins de 500 ms
  # joint_silence_len = 1300  # Ajouter un intervalle de 1300 millisecondes pour la segmentation lorsque les segments sont épissés
'''
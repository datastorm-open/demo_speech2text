import re
import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence

'''
    # silence_thresh = -70  # Le silence est inférieur à -70dBFS
    # min_silence_len = 700  # Split si le silence dépasse 700 ms
    # length_limit = 60 * 1000  # Chaque segment ne doit pas dépasser 1 minute après le fractionnement
    # abandon_chunk_len = 500  # Abandonner les morceaux de moins de 500 ms
    # joint_silence_len = 1300  # Ajouter un intervalle de 1300 millisecondes pour la segmentation lorsque les segments sont épissés
'''

### cut cut_audio
def _chunk_join_length_limit(chunks,joint_silence_len=1300,length_limit=60*1000):
    '''
    Args:
         chunk : fichier d'enregistrement
         joint_silence_len: L'intervalle entre les fichiers lors de la fusion, la valeur par défaut est de 1,3 seconde.
         length_limit: la longueur d'un seul fichier après la fusion ne dépasse pas cette valeur, la valeur par défaut est de 1 minute.
    Return:
         adjust_chunks: la liste fusionnée
    '''
    #
    silence = AudioSegment.silent(duration=joint_silence_len)
    adjust_chunks = []
    temp = AudioSegment.empty()
    for chunk in chunks:
        length = len(temp)+len(silence)+len(chunk)
        if length < length_limit:
            temp += silence+chunk
        else:
            adjust_chunks.append(temp)
            temp = chunk
    else:
        adjust_chunks.append(temp)
    return adjust_chunks

def _chunk_split_length_limit(chunk,min_silence_len=700,length_limit=60*1000,silence_thresh=-70):
    '''
    Args:
        chunk: sub-cut_audio
        min_silence_len: Lors de la scission d'une instruction, elle sera scindée si la durée de silence est respectée. la valeur par défaut est de 0,7 seconde.
        length_limit：La longueur d'un seul fichier après le fractionnement ne dépasse pas cette valeur et la valeur par défaut est de 1 minute.
        silence_thresh：moins de -70dBFS est silencieux
    Return:
        done_chunks: liste fractionnée

    '''
    todo_arr = []
    done_chunks =[]
    todo_arr.append([chunk,min_silence_len,silence_thresh])

    while len(todo_arr)>0:

        temp_chunk,temp_msl,temp_st = todo_arr.pop(0)

        if len(temp_chunk)<length_limit:
            done_chunks.append(temp_chunk)
        else:

            if temp_msl>100:
                temp_msl-=100
            elif temp_st<-10:
                temp_st+=10
            else:

                tempname = 'temp_%d.wav'%int(temp_chunk.time())
                chunk.export(tempname, format='wav')
                print('longueur de son:%d,durée du silence:%d dB: %dEncore trop long, clip enregistré dans:%s'%(len(temp_chunk),temp_msl,temp_st,tempname))
                raise Exception

            massage = 'Treitement: longueur de son,reste[durée du silence,dB]:%d,%d[%d,%d]'%(len(temp_chunk),len(todo_arr),temp_msl,temp_st)
            print(massage)

            temp_chunks = split_on_silence(temp_chunk,min_silence_len=temp_msl,silence_thresh=temp_st)
            doning_arr = [[c,temp_msl,temp_st] for c in temp_chunks]
            todo_arr = doning_arr+todo_arr
    return done_chunks

def _prepare(name,output, sound, silence_thresh=-70, min_silence_len=700, length_limit=60 * 1000, abandon_chunk_len=500,joint_silence_len=1300):
    '''
    Args:
         name: nom du fichier d'enregistrement
         sound : enregistrement des données du fichier
         silence_thresh: par défaut -70 # inférieur à -70dBFS est silencieux
         min_silence_len: par défaut 700 # split si le silence dépasse 700 millisecondes
         length_limit: 60*1000 par défaut # Chaque segment ne doit pas dépasser 1 minute après le fractionnement
         abandon_chunk_len: par défaut 500 #morceaux d'abandon inférieurs à 500ms
         joint_silence_len: default 1300 # Ajouter un intervalle de 1300 millisecondes pour l'épissage de segment
     Return:
         total: renvoie le nombre de fractionnements
    '''

    # Faites une pause selon la phrase et divisez-la en segments ne dépassant pas 1 minute.
    print('Commencez à diviser (veuillez patienter)\n', ' *' * 30)
    chunks = _chunk_split_length_limit(sound, min_silence_len=min_silence_len, length_limit=length_limit,
                                      silence_thresh=silence_thresh)  # silence time:700ms and silence_dBFS<-70dBFS
    print('Fin de fractionnement, renvoie le nombre de segments:', len(chunks), '\n', ' *' * 30)

    # Supprimer les segments de moins de 0,5 seconde
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i]) <= abandon_chunk_len:
            chunks.pop(i)
    print('segment valide：', len(chunks))

    # Fusionner les segments adjacents, un seul segment ne dépasse pas 1 minute
    chunks = _chunk_join_length_limit(chunks, joint_silence_len=joint_silence_len, length_limit=length_limit)
    print('Nombre de segments après fusion：', len(chunks))

    # enregistrer l'itinéraire
    if not os.path.exists(output + "/chunks"): os.mkdir(output + "/chunks")
    namef = re.split(r' |/|\\|[\s,.]', name)[-2]
    namec = re.split(r' |/|\\|[\s,.]', name)[-1]

    # save every chunks
    total = len(chunks)
    for i in range(total):
        new = chunks[i]
        save_name = '%s_%04d.%s' % (namef, i, namec)
        new.export(output + "/chunks/" + save_name, format=namec)
        # print('%04d'%i,len(new))
    print('save chunks')
    return total

# Couper l'cut_audio en fonction du silence
def CUT(input_file, output_address, silence_thresh = -70 ,min_silence_len = 700 , length_limit = 60 * 1000 , abandon_chunk_len = 500 , joint_silence_len = 1300 ):

    # delete the old chunks
    if os.path.exists(output_address) is False:
        os.mkdir(output_address)
    if os.path.exists(output_address + "/chunks"):
        shutil.rmtree(output_address + "/chunks/")
    else:
        pass

    # initial the name
    name = input_file
    sound = AudioSegment.from_wav(name)
    # sound = sound[:3*60*1000] # si le dossier trop gros, on va le testez premiere 3 mins.
    # silence_thresh = -70  # Le silence est inférieur à -70dBFS
    # min_silence_len = 700  # Split si le silence dépasse 700 ms
    # length_limit = 60 * 1000  # Chaque segment ne doit pas dépasser 1 minute après le fractionnement
    # abandon_chunk_len = 500  # Abandonner les morceaux de moins de 500 ms
    # joint_silence_len = 1300  # Ajouter un intervalle de 1300 millisecondes pour la segmentation lorsque les segments sont épissés

    _prepare(name, output_address, sound, silence_thresh, min_silence_len, length_limit, abandon_chunk_len, joint_silence_len)



import numpy
import sys
import tensorflow
tensorflow.config.list_physical_devices('GPU')

file = open("hetnet\\complex\\ent_labels.tsv", "r")
ent_labels = []
while True:
    line = file.readline()
    line = line.strip()
    if not line:
        break
    else:
        ent_labels.append(line)
file.close()

file = open("hetnet\\complex\\rel_labels.tsv", "r")
rel_labels = []
while True:
    line = file.readline()
    line = line.strip()
    if not line:
        break
    else:
        rel_labels.append(line)
file.close()

file = open("hetnet\\complex\\emb_e_real.tsv", "r")
ent_embedding = []
while True:
    line = file.readline()
    line = line.strip()
    if not line:
        break
    else:
        ent_embedding.append(line)
file.close()

file = open("hetnet\\complex\\emb_rel_real.tsv", "r")
rel_embedding = []
while True:
    line = file.readline()
    line = line.strip()
    if not line:
        break
    else:
        rel_embedding.append(line)
file.close()

ent_dict = {}
for idx in range(len(ent_labels)):
    tmp = ent_embedding[idx]
    tmp = tmp.split("\t")
    tmp = [x.strip() for x in tmp if x.strip()]
    tmp = [float(x) for x in tmp]
    # tmp = numpy.array(tmp)
    ent_dict[ent_labels[idx]] = tmp

rel_dict = {}
for idx in range(len(rel_labels)):
    tmp = rel_embedding[idx]
    tmp = tmp.split("\t")
    tmp = [x.strip() for x in tmp if x.strip()]
    tmp = [float(x) for x in tmp]
    # tmp = numpy.array(tmp)
    rel_dict[rel_labels[idx]] = tmp

# print(len(rel_dict))
# print(len(rel_dict[rel_labels[idx]]))
# print(len(ent_dict))
# print(len(ent_dict[ent_labels[idx]]))

x_train = []
file = open("hetnet\\Hetionet-train.txt", "r")
while True:
    line = file.readline()
    line = line.strip()
    if not line:
        break
    else:
        triple = line.split("\t")
        tmp = []
        tmp.extend(ent_dict[triple[0]])
        tmp.extend(rel_dict[triple[1]])
        tmp.extend(ent_dict[triple[2]])
        x_train.append(tmp)
file.close()

x_train = numpy.array(x_train)
x_train = numpy.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
y_train = numpy.ones(x_train.shape[0])

print(x_train.shape[0])
print(x_train.shape[1])

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Bidirectional
from keras.layers import Dropout
from keras_self_attention import SeqSelfAttention

model = Sequential()
model.add(Bidirectional(LSTM(units=100, return_sequences=True, input_shape = (x_train.shape[1], 1))))
model.add(SeqSelfAttention(attention_type=SeqSelfAttention.ATTENTION_TYPE_MUL, kernel_regularizer=keras.regularizers.l2(1e-4), bias_regularizer=keras.regularizers.l1(1e-4), attention_regularizer_weight=1e-4))
model.add(Dense(units = 1))

model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(x_train, y_train, epochs = 10, batch_size = 128)
model.summary(line_length=100)

model.save("complex")

count = 0
for idx, layer in enumerate(model.layers):
    func = keras.backend.function([model.get_layer(index=0).input], layer.output)
    layerOutput = func([x_train])
    with open("complex" + str(count), 'wb') as outfile:
        numpy.save(outfile, layerOutput)
    count += 1
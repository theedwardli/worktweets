from textgenrnn import textgenrnn
t = textgenrnn('textgenrnn_weights.hdf5')
t.generate(200, temperature=0.2)
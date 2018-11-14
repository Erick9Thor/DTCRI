import ParseData as pd
import argparse
import numpy as np
from ID3 import ID3
from C45 import C45
from Tree import Tree
import Validate


def split_data(data, train_ratio):
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    n_train = int(np.floor(data.shape[0] * train_ratio))
    indices_train = indices[:n_train]
    indices_val = indices[n_train:]
    x_train = data[indices_train]
    x_val = data[indices_val]
    print '*Muestras train:', len(x_train), ' (', train_ratio * 100, '%)'
    print '*Muestras validacion:', len(x_val), ' (', (1 - train_ratio) * 100, '%) \n'

    return x_train, x_val


def parseargsinput():
    parser = argparse.ArgumentParser(description='Decision Tree', prog='Decision Tree')
    parser.add_argument('-p', help='Path of data', required=True)
    parser.add_argument('-kf', default=True)
    parser.add_argument('-ID3', action='store_true')
    parser.add_argument('-C45', action='store_true')
    parser.add_argument('-hl', help='Input holdout', required=False)

    args = parser.parse_args()
    return vars(args)


def maketree(conv, d, mushColDomain, names, train, val):
    if d['ID3']:
        id3 = ID3(train, 2, mushColDomain)
        print '> training ID3...'
        tree = Tree(id3.ID3(), names, conv)
        print '> validation'
        print '----------------'
        Validate.measure(val, tree)
        print '----------------\n'

        tree.render()
    if d['C45']:
        c45 = C45(train, 2, mushColDomain)
        print '> training C4.5...'
        tree = Tree(c45.C45(), names, conv)
        print '> validation'
        print '----------------'
        Validate.measure(val, tree)
        print '----------------\n'

        tree.render()


def main():
    # Parseo de los argumentos de entrada

    d = parseargsinput()

    k = 2
    tratio = 0.8


    # Parseo de la base de datos

    conv, data = pd.formatFile(d['p'])
    # Valores maximos que puden tener cada atributo
    mushColDomain = [5, 3, 7, 1, 6, 1, 1, 1, 8, 1, 3, 3, 3, 6, 6, 0, 1, 2, 3, 5, 5, 5]
    names = ['class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises?', 'odor', 'gill-attachment', 'gill-spacing',
             'gill-size', 'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
             'stalk-surface-below-ring',
             'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type',
             'spore-print-color', 'population', 'habitat']

    if d['kf']:
        print '\n============================ K-FOLD ============================'
        print '*K =', k, '\n'

        indices = np.arange(data.shape[0])
        np.random.shuffle(indices)

        for i in range(0, k):
            # ----- Dividir dades -----

            indice_val = indices[len(indices) / k * i:len(indices) / k * (i + 1)]

            indice_train1 = indices[0:len(indices) / k * i]
            indice_train2 = indices[len(indices) / k * (i + 1):len(indices)]
            indice_train1 = np.concatenate((indice_train1, indice_train2))

            train = data[indice_train1]
            val = data[indice_val]

            maketree(conv, d, mushColDomain, names, train, val)

    # ================================================================
    # ============================ HOLD-OUT ==========================
    # ================================================================

    if d['hl']:
        print '\n============================ HOLD-OUT =========================='

        # ----- Dividir dades -----
        train, val = split_data(data, tratio)
        maketree(conv, d, mushColDomain, names, train, val)


if __name__ == '__main__':
    main()

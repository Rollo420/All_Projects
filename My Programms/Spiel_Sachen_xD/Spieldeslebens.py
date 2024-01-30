
import numpy as np



def genr_playground(rows: int = 90, columns : int = 90):
    # Erstelle ein leeres Spielfeld
    
    spielfeld = [[0] * columns for _ in range(rows)]

    # Beispiel: Setze in der sechsten Zeile von links nach rechts die Werte 1, 1, 1
    for i in range(3):
        spielfeld[5][i + 3] = 1

    return spielfeld


if __name__ == '__main__':
    print("Hello to my life :-)")

    plyground = genr_playground()

    for rows in plyground:
        for i in plyground:
            plyground[[1]][i + 3] = 1

    
    print(plyground,"\n")
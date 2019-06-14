class ComplexFunctions:
    def __init__(self):
        self.nomLdenclass = ["inf55", "55-60", "60-65", "65-70", "70-75", "sup75"]
        self.nomLnclass = ["inf50", "50-55", "55-60", "60-65", "65-70", "sup70"]

    def CrossedAnalysis (layer, attPop, attLden, attLn):
        # Charger la couche active
        features = layer.getFeatures()

        #On remplit un tableau avec (POP, Lden, Ln)
        Tableau = []
        for feature in features:
            POP = feature[attPop]
            Lden = feature[attLden]
            Ln = feature[attLn]
            lst = [POP, Lden, Ln]
            Tableau.append(lst)

        # Définition des variables et mise à zéro
        nbPOPLden = []
        for i in range(0, 6):
            nbPOPLden.append(0)
        nbPOPLdenTotal = 0
        nbPOPLn = []
        for i in range(0, 6):
            nbPOPLn.append(0)
        nbPOPLnTotal = 0

        # On remplit les classes
        for i in range(len(Tableau)):
            POP = Tableau[i][0]
            Lden = Tableau[i][1]
            Ln = Tableau[i][2]
            nbPOPLdenTotal = nbPOPLdenTotal + POP
            if Lden < 55:
                nbPOPLden[0] = nbPOPLden[0] + POP
            if 55 <= Lden < 60:
                nbPOPLden[1] = nbPOPLden[1] + POP
            if 60 <= Lden < 65:
                nbPOPLden[2] = nbPOPLden[2] + POP
            if 65 <= Lden < 70:
                nbPOPLden[3] = nbPOPLden[3] + POP
            if 70 <= Lden < 75:
                nbPOPLden[4] = nbPOPLden[4] + POP
            if Lden >= 75:
                nbPOPLden[5] = nbPOPLden[5] + POP

            if Ln < 50:
                nbPOPLn[0] = nbPOPLn[0] + POP
            if 50 <= Ln < 55:
                nbPOPLn[1] = nbPOPLn[1] + POP
            if 55 <= Ln < 60:
                nbPOPLn[2] = nbPOPLn[2] + POP
            if 60 <= Ln < 65:
                nbPOPLn[3] = nbPOPLn[3] + POP
            if 65 <= Ln < 70:
                nbPOPLn[4] = nbPOPLn[4] + POP
            if Ln >= 70:
                nbPOPLn[5] = nbPOPLn[5] + POP
        return nbPOPLden, nbPOPLn, nbPOPLdenTotal

    def NatCrossedAnalysis (layer, attPop, attLden, attLn,nat, hab):
        # Charger la couche active
        features = layer.getFeatures()

        #On remplit un tableau avec (POP, Lden, Ln)
        Tableau = []
        for feature in features:
            Nature = str(feature[nat])
            POP = feature[attPop]
            Lden = feature[attLden]
            Ln = feature[attLn]
            lst = [POP, Lden, Ln]
            if Nature == hab:
                Tableau.append(lst)

        # Définition des variables et mise à zéro
        nbPOPLden = []
        for i in range(0, 6):
            nbPOPLden.append(0)
        nbPOPLdenTotal = 0
        nbPOPLn = []
        for i in range(0, 6):
            nbPOPLn.append(0)
        nbPOPLnTotal = 0

        # On remplit les classes
        for i in range(len(Tableau)):
            POP = Tableau[i][0]
            Lden = Tableau[i][1]
            Ln = Tableau[i][2]
            nbPOPLdenTotal = nbPOPLdenTotal + POP
            nbPOPLnTotal = nbPOPLnTotal + POP
            if Lden < 55:
                nbPOPLden[0] = nbPOPLden[0] + POP
            if 55 <= Lden < 60:
                nbPOPLden[1] = nbPOPLden[1] + POP
            if 60 <= Lden < 65:
                nbPOPLden[2] = nbPOPLden[2] + POP
            if 65 <= Lden < 70:
                nbPOPLden[3] = nbPOPLden[3] + POP
            if 70 <= Lden < 75:
                nbPOPLden[4] = nbPOPLden[4] + POP
            if Lden >= 75:
                nbPOPLden[5] = nbPOPLden[5] + POP

            if Ln < 50:
                nbPOPLn[0] = nbPOPLn[0] + POP
            if 50 <= Ln < 55:
                nbPOPLn[1] = nbPOPLn[1] + POP
            if 55 <= Ln < 60:
                nbPOPLn[2] = nbPOPLn[2] + POP
            if 60 <= Ln < 65:
                nbPOPLn[3] = nbPOPLn[3] + POP
            if 65 <= Ln < 70:
                nbPOPLn[4] = nbPOPLn[4] + POP
            if Ln >= 70:
                nbPOPLn[5] = nbPOPLn[5] + POP
        return nbPOPLden, nbPOPLn, nbPOPLdenTotal

    def LimitAnalysis (layer, attPop, attLden, attLn, limit_Lden, limit_Ln):
        # Charger la couche active
        features = layer.getFeatures()

        #On remplit un tableau avec (POP, Lden, Ln)
        Tableau = []
        for feature in features:
            POP = feature[attPop]
            Lden = feature[attLden]
            Ln = feature[attLn]
            lst = [POP, Lden, Ln]
            Tableau.append(lst)

        # Définition des variables et mise à zéro
        nblimitLden = 0
        nblimitLn = 0


        # On remplit les classes
        for i in range(len(Tableau)):
            POP = Tableau[i][0]
            Lden = Tableau[i][1]
            Ln = Tableau[i][2]
            if Lden >= limit_Lden:
                nblimitLden = nblimitLden + POP
            if Ln >= limit_Ln:
                nblimitLn = nblimitLn + POP
        return nblimitLden, nblimitLn

    def NatLimitAnalysis (layer, attPop, attLden, attLn, limit_Lden, limit_Ln, nat, hab):
        # Charger la couche active
        features = layer.getFeatures()

        #On remplit un tableau avec (POP, Lden, Ln)
        Tableau = []

        for feature in features:
            POP = feature[attPop]
            Lden = feature[attLden]
            Ln = feature[attLn]
            Nature = str(feature[nat])
            lst = [POP, Lden, Ln]
            if Nature == hab:
                Tableau.append(lst)

        # Définition des variables et mise à zéro
        nblimitLden = 0
        nblimitLn = 0


        # On remplit les classes
        for i in range(len(Tableau)):
            POP = Tableau[i][0]
            Lden = Tableau[i][1]
            Ln = Tableau[i][2]
            if Lden >= limit_Lden:
                nblimitLden = nblimitLden + POP
            if Ln >= limit_Ln:
                nblimitLn = nblimitLn + POP
        return nblimitLden, nblimitLn


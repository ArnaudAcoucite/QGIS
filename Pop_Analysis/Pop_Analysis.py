# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction, QTableWidgetItem, QTableWidget,QFileDialog, QMessageBox
from qgis.core import *
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Pop_Analysis_dialog import Pop_AnalysisDialog
from .results_dialog import Results_Dialog
# Import de la classe fonction complexe
from .complexfunctions import ComplexFunctions
import os.path


class Pop_Analysis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Pop_Analysis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Pop_AnalysisDialog()
        self.dgresults = Results_Dialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Pop_Analysis')


        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Pop_Analysis', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Pop_Analysis/icon.png'
        self.add_action(icon_path,text=self.tr(u'Population_Analysis'),callback=self.run,parent=self.iface.mainWindow())
        pixmap = QPixmap(':/plugins/Pop_Analysis/Acoucite.png')
        self.dlg.label_acou.setPixmap(pixmap)
        self.first_start = True
        #On charge les 2 combobox des le lancement du plugin

# *************************************************************************************************
# Display the layers in the combo box
    def loadShape(self):
        self.dlg.cb_layerlist.clear()
        layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        vector_layers = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                vector_layers.append(layer.name())
        self.dlg.cb_layerlist.addItems(vector_layers)

# Clear all widget in dlg
    def ClearAll(self):
        self.dlg.cb_layerlist.clear()
        self.dlg.cb_src.clear()
        self.dlg.cb_pop.clear()
        self.dlg.cb_lden.clear()
        self.dlg.cb_ln.clear()
        self.dlg.cb_nat.clear()
        self.dlg.checkBox_nat.setChecked(False)

    def srcLoad(self):
        self.dlg.cb_src.clear()
        src = ["Routier", "Ferroviaire", "Aérien", "Industriel"]
        self.dlg.cb_src.addItems(src)
        return src

    def getShape(self):
        layer = None
        layername = self.dlg.cb_layerlist.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == layername:
                layer = lyr
                break
        return layer

    def loadFields(self):
        inShape = self.getShape()
        if inShape != None:
            fields = inShape.fields()
            self.dlg.cb_pop.clear()
            self.dlg.cb_lden.clear()
            self.dlg.cb_ln.clear()
            list_fields = []
            for field in fields:
                list_fields.append(field.name())

            src = self.dlg.cb_src.currentText()
            if src == "Aérien":
                self.dlg.cb_ln.clear()
                self.dlg.cb_pop.addItems(list_fields)
                self.dlg.cb_lden.addItems(list_fields)
            else:
                self.dlg.cb_pop.addItems(list_fields)
                self.dlg.cb_lden.addItems(list_fields)
                self.dlg.cb_ln.addItems(list_fields)

    def setLimit(self):
        src = self.dlg.cb_src.currentText()
        if src == "Routier":
            limit_Lden = 68
            limit_Ln = 62
        if src == "Ferroviaire":
            limit_Lden = 73
            limit_Ln = 65
        if src == "Aérien":
            limit_Lden = 55
            limit_Ln = 0
        if src == "Industriel":
            limit_Lden = 71
            limit_Ln = 60
        return limit_Lden, limit_Ln

    def allvariables(self):
        #On réccupère les variables
        self.s = self.dlg.cb_src.currentText()
        self.couche = self.getShape()
        self.attPOP = self.dlg.cb_pop.currentText()
        self.attLden = self.dlg.cb_lden.currentText()
        if self.s == 'Aérien':
            self.attLn = self.attLden
        else:
            self.attLn = self.dlg.cb_ln.currentText()
        #On définit les classes
        self.nomLdenclass = ["Lden inf à 55 dB(A)", "Lden [55-60[ dB(A)", "Lden [60-65[ dB(A)", "Lden [65-70[ dB(A)", "Lden[70-75[ dB(A)", "Lden sup à 75 dB(A)"]
        self.nomLnclass = ["Ln inf à 50 dB(A)", "Ln [50-55[ dB(A)", "Ln[55-60[ dB(A)", "Ln[60-65[ dB(A)", "Ln[65-70[ dB(A)", "Ln sup70 à dB(A)"]

    def calculExpo(self):
        self.limit_Lden, self.limit_Ln = self.setLimit()
        self.nbPOPLden, self.nbPOPLn, self.nbPOPLdenTotal = ComplexFunctions.CrossedAnalysis(self.couche, self.attPOP, self.attLden, self.attLn)
        self.nblimitLden, self.nblimitLn = ComplexFunctions.LimitAnalysis(self.couche, self.attPOP, self.attLden, self.attLn, self.limit_Lden, self.limit_Ln)


        nat = self.dlg.cb_nat.currentText()
        hab = self.dlg.cb_hab.currentText()
        if nat and hab:
            self.NatnbPOPLden, self.NatnbPOPLn, self.NatnbPOPLdenTotal = ComplexFunctions.NatCrossedAnalysis(self.couche, self.attPOP, self.attLden, self.attLn, nat,hab)
            self.NatnblimitLden, self.NatnblimitLn = ComplexFunctions.NatLimitAnalysis(self.couche, self.attPOP, self.attLden, self.attLn, self.limit_Lden, self.limit_Ln,nat, hab)

    def setTextBox(self):
        #On paramètre le texte à entre dans la boite de dialogue
        self.dgresults.txt_result.clear()

        if self.s == 'Aérien':
            self.dgresults.txt_result.append(f"Le nombre de personnes total est {self.nbPOPLdenTotal} ")
            self.dgresults.txt_result.append(" ")
            for noiseclass in range(0, 6):
                text = (f"Le nombre de personnes avec Lden {self.nomLdenclass[noiseclass]} est : {self.nbPOPLden[noiseclass]}")
                self.dgresults.txt_result.append(text)
            self.dgresults.txt_result.append("")
            self.dgresults.txt_result.append(
                f"Le nombre de personnes au dessus de {self.limit_Lden} dB(A) est de: {self.nblimitLden} ")
            self.dgresults.txt_result.append("")
            self.dgresults.setFixedSize(self.dgresults.size())
            self.dgresults.show()

        else:
            self.dgresults.txt_result.append(f"Le nombre de personnes total est {self.nbPOPLdenTotal} ")
            self.dgresults.txt_result.append(" ")
            for noiseclass in range(0, 6):
                text = (
                    f"Le nombre de personnes avec {self.nomLdenclass[noiseclass]} est : {self.nbPOPLden[noiseclass]}")
                self.dgresults.txt_result.append(text)
            self.dgresults.txt_result.append("")
            self.dgresults.txt_result.append(
                f"Le nombre de personnes au dessus de {self.limit_Lden} dB(A) est de: {self.nblimitLden} ")
            self.dgresults.txt_result.append("")

            for noiseclass in range(0, 6):
                text = (f"Le nombre de personnes avec {self.nomLnclass[noiseclass]} est : {self.nbPOPLn[noiseclass]}")
                self.dgresults.txt_result.append(text)
            self.dgresults.txt_result.append("")
            self.dgresults.txt_result.append(f"Le nombre de personnes au dessus de {self.limit_Ln} dB(A) est de: {self.nblimitLn} ")
            self.dgresults.setFixedSize(self.dgresults.size())
            self.dgresults.show()

    def setTextBoxNat(self):
        self.dgresults.txt_result.clear()

        if self.s == 'Aérien':
            self.dgresults.txt_result.append(f"Le nombre de personnes total est {self.NatnbPOPLdenTotal} ")
            self.dgresults.txt_result.append(" ")
            for noiseclass in range(0, 6):
                text = (f"Le nombre de personnes avec {self.nomLdenclass[noiseclass]} est : {self.NatnbPOPLden[noiseclass]}")
                self.dgresults.txt_result.append(text)
            self.dgresults.txt_result.append("")
            self.dgresults.txt_result.append(
                f"Le nombre de personnes au dessus de {self.limit_Lden} est de: {self.NatnblimitLden} ")
            self.dgresults.txt_result.append("")
            self.dgresults.setFixedSize(self.dgresults.size())
            self.dgresults.show()

        else:
            self.dgresults.txt_result.append(f"Le nombre de personnes total est {self.NatnbPOPLdenTotal} ")
            self.dgresults.txt_result.append(" ")
            for noiseclass in range(0, 6):
                text = (
                    f"Le nombre de personnes avec {self.nomLdenclass[noiseclass]} est : {self.NatnbPOPLden[noiseclass]}")
                self.dgresults.txt_result.append(text)
            self.dgresults.txt_result.append("")
            self.dgresults.txt_result.append(
                f"Le nombre de personnes au dessus de {self.limit_Lden} est de: {self.NatnblimitLden} ")
            self.dgresults.txt_result.append("")
            for noiseclass in range(0, 6):
                text = (f"Le nombre de personnes avec {self.nomLnclass[noiseclass]} est : {self.NatnbPOPLn[noiseclass]}   ")
                self.dgresults.txt_result.append(text)
            self.dgresults.txt_result.append("")
            self.dgresults.txt_result.append(f"Le nombre de personnes au dessus de {self.limit_Ln} est de: {self.NatnblimitLn} ")
            self.dgresults.setFixedSize(self.dgresults.size())
            self.dgresults.show()

    def setTableBox(self):
        self.dgresults.table_pop.clear()
        #On défini le tableau
        nb_row = 14
        nb_col = 2
        src = self.dlg.cb_src.currentText()
        self.dgresults.table_pop.setRowCount(nb_row)
        self.dgresults.table_pop.setColumnCount(nb_col)
        self.dgresults.table_pop.setHorizontalHeaderLabels([u'Classes',u'Habitants'])
        #Mise en forme de la table
        limitLdenchar = f"Lden sup à {self.limit_Lden} dB(A)"
        limitLnchar = f"Ln sup à {self.limit_Ln} dB(A)"
        Globalist = self.nomLdenclass
        Globalist.append(limitLdenchar)
        if not src == "Aérien":
            Globalist += self.nomLnclass
            Globalist.append(limitLnchar)

        GlobaldB = self.nbPOPLden
        GlobaldB.append(self.nblimitLden)
        if not src == "Aérien":
            GlobaldB += self.nbPOPLn
            GlobaldB.append(self.nblimitLn)


        # Import de la table dans la QtableWidgetItem
        for row in range(len(Globalist)):
                for col in range(nb_col):
                    if col==0:
                        value = Globalist[row]
                        item = QTableWidgetItem(value)
                    else:
                         value = str(GlobaldB[row])
                         item = QTableWidgetItem(value)
                    self.dgresults.table_pop.setItem(row, col, item)

        self.dgresults.setFixedSize(self.dgresults.size())
        self.dgresults.table_pop.resizeColumnsToContents()
        self.dgresults.show()

    def setTableBoxNat(self):
        self.dgresults.table_pop.clear()
        #On définit le tableau
        nb_row = 14
        nb_col = 2
        src = self.dlg.cb_src.currentText()
        self.dgresults.table_pop.setRowCount(nb_row)
        self.dgresults.table_pop.setColumnCount(nb_col)
        self.dgresults.table_pop.setHorizontalHeaderLabels([u'Classes',u'Habitants'])
        #Mise en forme de la table
        limitLdenchar = f"Lden sup à {self.limit_Lden} dB(A)"
        limitLnchar = f"Ln sup à {self.limit_Ln} dB(A)"

        Globalist = self.nomLdenclass
        Globalist.append(limitLdenchar)
        if not src  == "Aérien":
            Globalist += self.nomLnclass
            Globalist.append(limitLnchar)

        GlobaldB = self.NatnbPOPLden
        GlobaldB.append(self.NatnblimitLden)
        if not src == "Aérien":
            GlobaldB += self.NatnbPOPLn
            GlobaldB.append(self.NatnblimitLn)

        # Import de la table dans la QtableWidgetItem
        for row in range(len(Globalist)):
                for col in range(nb_col):
                    if col==0:
                        value = Globalist[row]
                        item = QTableWidgetItem(value)
                    else:
                         value = str(GlobaldB[row])
                         item = QTableWidgetItem(value)
                    self.dgresults.table_pop.setItem(row, col, item)

        self.dgresults.setFixedSize(self.dgresults.size())
        self.dgresults.table_pop.resizeColumnsToContents()
        self.dgresults.show()

    def setNature(self):
        self.dlg.cb_nat.clear()
        checked = self.dlg.checkBox_nat.isChecked()
        if checked:
            inShape = self.getShape()
            fields = inShape.fields()
            list_fields = []
            for field in fields:
                list_fields.append(field.name())
            self.dlg.cb_nat.addItems(list_fields)

    def uniqueValue(self):
        self.dlg.cb_hab.clear()
        nature = self.dlg.cb_nat.currentText()
        layer = self.getShape()
        idx = layer.fields().indexOf(nature)
        values = layer.uniqueValues(idx)
        str_value =[]
        for value in values:
            val = str(value)
            str_value.append(val)
        self.dlg.cb_hab.addItems(str_value)

    def export_csv(self):
        outFile = str(QFileDialog.getSaveFileName(caption="Save csv as", filter="csv (*.csv)")[0])
        if outFile:
            with open(outFile, mode='w', encoding='utf-8') as csv_file:
                for row in range(self.dgresults.table_pop.rowCount()):
                    row_csv = []
                    for column in range(self.dgresults.table_pop.columnCount()):
                        item = self.dgresults.table_pop.item(row, column)
                        if item is None:
                            row_csv.append("")
                        else:
                            row_csv.append((item.text()))
                    element = ",".join([x for x in row_csv]) + "\n"
                    csv_file.write(element)
        else: pass

    def export_txt(self):
        outFile = str(QFileDialog.getSaveFileName(caption="Save csv as", filter="Texte (*.txt)")[0])
        if outFile:
            with open(outFile, mode='w', encoding='utf-8') as text_file:
                element = self.dgresults.txt_result.toPlainText()
                text_file.write(element)
# *************************************************************************************************
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Pop_Analysis'),action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # show the dialog
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        self.allvariables()

        #On lance les fonctions si l'applications est lancé pour la première fois
        if self.first_start:
            self.srcLoad()
            self.loadShape()
            self.loadFields()
            self.first_start = False
        # On lance les fonctions si l'applications est lancé pour la 2eme fois ou +
        else:
            self.ClearAll()
            self.srcLoad()
            self.loadShape()

        # On active la nature
        self.dlg.checkBox_nat.stateChanged.connect(self.setNature)
        self.dlg.pushLoad.clicked.connect(self.uniqueValue)

        # Si on change les combobox "src" et "layerlist"
        self.dlg.cb_layerlist.currentTextChanged.connect(self.loadFields)
        self.dlg.cb_src.currentTextChanged.connect(self.loadFields)


        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        #On vérifie le format des attributs
        layer = self.getShape()
        fields = layer.fields()
        self.allvariables()
        idx_POP = fields.indexFromName(str(self.attPOP))
        Format_POP= fields[idx_POP].typeName()
        idx_Lden = fields.indexFromName(str(self.attLden))
        Format_Lden = fields[idx_Lden].typeName()
        idx_Ln = fields.indexFromName(str(self.attLn))
        Format_Ln = fields[idx_Ln].typeName()

        if result:
            checked = self.dlg.checkBox_nat.isChecked()
            format_list=["Integer","Integer64","Real"]
            if Format_POP not in str(format_list) or Format_Lden not in str(format_list) or Format_Lden not in str(format_list):
                QMessageBox.warning(self.dlg, "Problème Variables",
                                    f"Une de vos variables n'est pas un nombre' \n Population:{Format_POP}, Lden: {Format_Lden}, Ln:{Format_Ln}")

            else:
                if checked:
                    #self.allvariables()
                    self.calculExpo()
                    self.setTextBoxNat()
                    self.setTableBoxNat()
                    self.dgresults.pushcsv.clicked.connect(self.export_csv)
                    self.dgresults.pushtxt.clicked.connect(self.export_txt)
                else:
                    #self.allvariables()
                    self.calculExpo()
                    self.setTextBox()
                    self.setTableBox()
                    self.dgresults.pushcsv.clicked.connect(self.export_csv)
                    self.dgresults.pushtxt.clicked.connect(self.export_txt)





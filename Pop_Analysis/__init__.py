# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Pop_Analysis
                                 A QGIS plugin
 Analyse croisée de la population avec les niveau de bruit
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-05-27
        copyright            : (C) 2019 by Acoucité
        email                : sebastien.carra@acoucite.org
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Pop_Analysis class from file Pop_Analysis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Pop_Analysis import Pop_Analysis
    return Pop_Analysis(iface)

from qgis.core import *
import qgis.utils
import qgis


qgis.utils.iface.activeLayer()

qgsi
qgis.utils.iface

# Supply the path to the qgis install location
QgsApplication.setPrefixPath("/usr", True)

# Create a reference to the QgsApplication.
# Setting the second argument to True enables the GUI.  We need
# this since this is a custom application.

qgs = QgsApplication([], True)

# load providers
qgs.initQgis()
qgs.ifa

#from qgis.core importQgsProject# Get the project instance
project = QgsProject.instance()
project.mapLayersByName("trails")

qgis.utils.iface.activeLayer()


iface = qgis.gui.QgisInterface
vlayer = iface.addVectorLayer(path_to_ports_layer, "Ports layer", "ogr")

# Write your code here to load some layers, use processing
# algorithms, etc.

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()

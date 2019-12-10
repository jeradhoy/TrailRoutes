sys.path.append("/usr/share/qgis/python/plugins")
from processing.core.Processing import Processing

import os
import processing
import sys

from qgis.core import (
    QgsApplication,
    QgsProcessingFeedback,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter
)

from qgis.analysis import QgsNativeAlgorithms



#os.environ['QGIS_PREFIX_PATH'] = r'/usr/bin/qgis'

QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], True)
qgs.initQgis()



Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())


data_root_dir = "Data/Shapefiles"


def find_shapefiles(root_dir):
    file_list = []
    for root, dirs, files in os.walk(data_root_dir):
        for file in files:
            if file.endswith(".shp"):
                file_list.append(os.path.join(os.getcwd(), root, file))
    return file_list


shapefiles = find_shapefiles(data_root_dir)

def process_trail(trail_path):

    print("Processing file: " + trail_path)

    input_trails = QgsVectorLayer(trail_path, 'Trans_TrailSegment', 'ogr')

    if input_trails.isValid() == False:
        print("Failed to load layer")
        return ("Failed to load: " + trail_path)

    result = processing.run("native:reprojectlayer", {'INPUT': input_trails,
                                                    'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'),
                                                    'OUTPUT': 'memory:'})

    result = processing.run("qgis:deletecolumn", {'INPUT': result["OUTPUT"],
                                                'COLUMN': ['OBJECTID', 'PERMANENT_', 'SOURCE_FEA', 'SOURCE_DAT', 'LOADDATE', 'FTYPE', 'FCODE', 'LENGTH', 'GNIS_ID', 'SHAPE_Leng'],
                                                'OUTPUT': 'memory:'})

    result = processing.run("qgis:snapgeometries", {'INPUT': result["OUTPUT"],
                                                    'REFERENCE_LAYER': result["OUTPUT"],
                                                    'TOLERANCE': 30,
                                                    'BEHAVIOR': 4, 
                                                    'OUTPUT': 'memory:'})
    print("Finished snapping geoms")

    result = processing.run("native:fixgeometries", {'INPUT': result["OUTPUT"], 
                                                    'OUTPUT': 'memory:'})

    result = processing.run("native:dissolve", {'INPUT': result["OUTPUT"],
                                                'FIELD': ['NAME', 'TRAILNUMBE'],
                                                'OUTPUT': 'memory:'})
    print("Finished dissolving geoms")

    result = processing.run("native:mergelines", {'INPUT': result["OUTPUT"],
                                                'OUTPUT': 'memory:'})
    print("Finished merging lines")

    result = processing.run("native:splitwithlines", {'INPUT': result["OUTPUT"],
                                                    'LINES': result["OUTPUT"],
                                                    'OUTPUT': 'memory:'})
    print("Finished splittingLineswithLines")

    split_output_path = './Data/split.gpkg'

    if os.path.exists(split_output_path):
        os.remove(split_output_path)

    grass_out = processing.run("grass7:v.split", {'input': result["OUTPUT"],
                                            'length': 1,
                                            'units': 5,
                                            'vertices': None,
                                            '-n': False,
                                            '-f': False,
                                            'output': split_output_path,
                                            'GRASS_REGION_PARAMETER': None,
                                            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
                                            'GRASS_MIN_AREA_PARAMETER': 0.0001,
                                            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
                                            'GRASS_VECTOR_DSCO': '',
                                            'GRASS_VECTOR_LCO': '',
                                            'GRASS_VECTOR_EXPORT_NOCAT': False})

    print("Finished splitting into 0.5 miles sections")

    split_trails = QgsVectorLayer(split_output_path, 'split-trails', 'ogr', crs=QgsCoordinateReferenceSystem('EPSG:3857'))

    print("Finished processing: " + trail_path)

    return split_trails

trail_list = [process_trail(path) for path in shapefiles]

len(processed_shapes)

#trail_list = [output[0]["OUTPUT"] for output in processed_shapes]
#junct_list = [output[1]["OUTPUT"] for output in processed_shapes]

trails_merged = processing.run("native:mergevectorlayers", {'LAYERS': trail_list,
                                            'CRS':QgsCoordinateReferenceSystem('EPSG:3857'),
                                            'OUTPUT':'memory:'})

# juncts_merged = processing.run("native:mergevectorlayers", {'LAYERS':junct_list,
#                                             'CRS':QgsCoordinateReferenceSystem('EPSG:3857'),
#                                             'OUTPUT':'memory:'})

trails_merged_simp = processing.run("native:simplifygeometries", {'INPUT': trails_merged["OUTPUT"],
                                             'METHOD':0,
                                             'TOLERANCE':1,
                                             'OUTPUT':'memory:'})

#trails_merged_simp = QgsVectorLayer("trails_merged_simp_4326.shp", 'trails', 'ogr')

# result = processing.run("qgis:deletecolumn", {'INPUT': trails_merged_simp,
#                                             'COLUMN': ['id', 'length_mi'],
#                                             'OUTPUT': 'memory:'})

# result = processing.run("native:reprojectlayer", {'INPUT': result["OUTPUT"],
#                                                 'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'),
#                                                 'OUTPUT': 'memory:'})

result = processing.run("native:addautoincrementalfield", {'INPUT': trails_merged_simp["OUTPUT"],
                                                        'FIELD_NAME': 'id', 
                                                        'START': 0, 
                                                        'GROUP_FIELDS': [], 
                                                        'SORT_EXPRESSION': '', 
                                                        'SORT_ASCENDING': True, 
                                                        'SORT_NULLS_FIRST': False, 
                                                        'OUTPUT': 'memory:'})

trails_processed = processing.run("qgis:fieldcalculator", {
                                                        'INPUT': result["OUTPUT"],
                                                        'FIELD_NAME': 'length_mi',
                                                        'FIELD_TYPE': 0, 
                                                        'FIELD_LENGTH': 10, 
                                                        'FIELD_PRECISION': 3, 
                                                        'NEW_FIELD': True, 
                                                        'FORMULA': '$length * 0.000621371', 
                                                        'OUTPUT': 'memory:'})

junctions_processed = processing.run("qgis:extractspecificvertices", {
            'INPUT': trails_processed["OUTPUT"], 'VERTICES': '0, -1', 'OUTPUT': 'memory:'})

QgsVectorFileWriter.writeAsVectorFormat(trails_processed["OUTPUT"], r"trails_merged_simp_4326_2.shp", "UTF-8", QgsCoordinateReferenceSystem('EPSG:4326'), "ESRI Shapefile")
QgsVectorFileWriter.writeAsVectorFormat(junctions_processed["OUTPUT"], r"juncts_merged_4326_2.shp", "UTF-8", QgsCoordinateReferenceSystem('EPSG:4326'), "ESRI Shapefile")
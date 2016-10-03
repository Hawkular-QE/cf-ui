import ConfigParser
import StringIO
import os

class properties(object):

    PROPERTIES_FILE_NAME = "properties.properties"

    # Simple parser for *.properties file
    # http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python
    def read_properties_file(self, file_path):
        # if file does not exists return empty array
        if not os.path.isfile(file_path):
            return []
        # load property file and parse ti to array
        with open(file_path) as f:
            config = StringIO.StringIO()
            config.write('[properties_section]\n')
            config.write(f.read().replace('%', '%%'))
            config.seek(0, os.SEEK_SET)

            cp = ConfigParser.SafeConfigParser()
            cp.optionxform = str
            cp.readfp(config)

            return dict(cp.items('properties_section'))

    def __init__(self):
        # TODO: parse *.properties file name & path from command line arguments
        # load properties from same dir as this file is in
        propertyArray = self.read_properties_file(os.path.dirname(__file__) + '/' + self.PROPERTIES_FILE_NAME)

        # overwrite with env variables if possible
        for (propName, propVal) in propertyArray.items():
            try:
                propVal=os.environ[propName]
                if propVal:
                    propertyArray[propName]=propVal
            except KeyError:
                pass
            try:
                propVal=os.environ['CFUI_'+propName]
                if propVal:
                    propertyArray[propName]=propVal
            except KeyError:
                pass

        # check if propertyArray is not empty
        if propertyArray:
            # set this class's attributes from propertyArray
            for propertyItemKey, propertyItemValue in propertyArray.iteritems():
                setattr( properties, propertyItemKey, propertyItemValue )

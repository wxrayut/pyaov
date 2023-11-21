
# This script was proudly coded by wxrayut (https://github.com/wxrayut).

import os
from zipfile import ZipFile
from xml.etree.ElementTree import Element, fromstring, tostring, indent

class CreateElement:
    def __init__(self):
        self.tag: str = None
        self.attrib: dict = None

    def __getname__(self, func) -> str:
        return func.__name__

    def Track(self, trackName: str, eventType: str, guid: str, enabled: str = 'true', refParamName: str = '', useRefParam: str = 'false', r: str = '', g: str = '', b: str = '', execOnForceStopped: str = 'false', execOnActionCompleted: str = 'false', stopAfterLastEvent: str = 'true'):
        self.tag = self.__getname__(self.Track)
        self.attrib = {
            'trackName': trackName,
            'eventType': eventType,
            'guid': guid,
            'enabled': enabled,
            'refParamName': refParamName,
            'useRefParam': useRefParam,
            'r': r,
            'g': g,
            'b': b,
            'execOnForceStopped': execOnForceStopped,
            'execOnActionCompleted': execOnActionCompleted,
            'stopAfterLastEvent': stopAfterLastEvent
        }
        return Element(self.tag, self.attrib)

    def Event(self, eventName: str, time: str, length: str, isDuration: str):
        self.tag = self.__getname__(self.Event)
        self.attrib = {
            'eventName': eventName,
            'time': time,
            'length': length,
            'isDuration': isDuration,
        }
        return Element(self.tag, self.attrib)

    def SubElement(self, tag: str, name: str, value: str, refParamName: str = '', useRefParam: str = 'false'):
        self.tag = tag
        self.attrib = {
            'name': name,
            'value': value,
            'refParamName': refParamName,
            'useRefParam': useRefParam
        }
        return Element(self.tag, self.attrib)

class DroneView(CreateElement):
    def __init__(self):
        self.struct = 4
        self.encoding = 'ISO-8859-1'
        self.current_directory = os.path.join('DroneView', 'INP')
        self.output_directory = os.path.join('DroneView', 'OUT')
        self.zipfilename = 'CommonActions.pkg.bytes'

    @staticmethod
    def __heightrate(percentage: float):
        return str(round(1.5 + ((percentage - 10) / 10) * 1.5, 2)) + '0' * 3

    def Back(self, root, heightRate: str):
        anode = root.find(".//Action[@tag='']")
        SetCameraHeightDuration = self.Track('SetCameraHeightDuration0', 'SetCameraHeightDuration', '4e706ad9-c26b-4328-b1a1-57a592c0059b', r = '0.467', g = '0.000', b = '1.000')
        Event = self.Event('SetCameraHeightDuration', '0.000', '200', 'true')
        Event.append(
            self.SubElement('int', 'slerpTick', '0')
        )
        Event.append(
            self.SubElement('bool', 'cutBackOnExit', 'false')
        )
        Event.append(
            self.SubElement('float', 'heightRate', heightRate)
        )
        Event.append(
            self.SubElement('bool', 'bOverride', 'false')
        )
        Event.append(
            self.SubElement('bool', 'leftTimeSlerpBack', 'true')
        )
        Event.append(
            self.SubElement('bool', 'exitKeepCurrentValue', 'false')
        )
        Event.append(
            self.SubElement('bool', 'isSlerpBackWhenInterrupted', 'true')
        )
        Event.append(
            self.SubElement('int', 'slerpBackTick', '100')
        )
        Event.append(
            self.SubElement('bool', 'heightRateCanLowerThanOne', 'false')
        )
        SetCameraHeightDuration.append(Event)
        anode.append(SetCameraHeightDuration)
        
        space = '  '
        indent(root, space)
        return tostring(root)

    def main(self, compress_type = 0, compresslevel = 0):

        Banner = """
 ____  ____   ___  _   _ _______     _____ _______        __
|  _ \|  _ \ / _ \| \ | | ____\ \   / /_ _| ____\ \      / /
| | | | |_) | | | |  \| |  _|  \ \ / / | ||  _|  \ \ /\ / / 
| |_| |  _ <| |_| | |\  | |___  \ V /  | || |___  \ V  V /  
|____/|_| \_\\____/|_| \_|_____|  \_/  |___|_____|  \_/\_/

Note: click Recall button for active.
        """
        print(Banner)

        heightrate = self.__heightrate(float(input("Enter Percentage of camera drone view (10, 20, 30 or 40.1) : ")))

        input_blob = os.path.join(self.current_directory, self.zipfilename)
        with ZipFile(input_blob, 'r') as items:
            output_blob = os.path.join(self.output_directory, self.zipfilename)
            with ZipFile(output_blob, 'w') as Zip_ref_B:
                for fs in items.namelist():
                    if fs.endswith('/Back.xml'):
                        content = items.read(fs)
                        if content[:self.struct] == b'\x22\x4a\x00\xef':
                            raise Exception("The compressed data in the archive cannot be edited. %s" % (fs))
                        root = fromstring(content)
                        modified_content = self.Back(root, heightrate)
                    else:
                        modified_content = items.read(fs)
                    Zip_ref_B.writestr(fs, modified_content, compress_type, compresslevel)
        print('\nDone.\n')

if __name__ == '__main__':
    DV = DroneView()
    DV.main()

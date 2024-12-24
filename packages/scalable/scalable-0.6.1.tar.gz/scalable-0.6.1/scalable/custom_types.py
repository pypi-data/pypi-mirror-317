import os
import lxml.etree as ET
from xxhash import xxh32

from .common import SEED
from .caching import *


class GCAMConfigType(GenericType):

    def __init__(self, value):
        self.value = value
        parser = ET.XMLParser(strip_cdata=False)
        self.config_doc = ET.parse(self.value, parser)

    def __hash__(self):
        digest = 0
        x = xxh32(seed=SEED)
        x.update(str(self.value).encode('utf-8'))
        x.update(hash_to_bytes(hash(FileType(self.value))))
        root = self.config_doc.getroot()
        for element in root.iter():
            if element.text and isinstance(element.text, str):
                if os.path.exists(element.text):
                    if os.path.isfile(element.text):
                        x.update(hash_to_bytes(hash(FileType(element.text))))
                    elif os.path.isdir(element.text):
                        x.update(hash_to_bytes(hash(DirType(element.text))))
                else:
                    x.update(hash_to_bytes(hash(ValueType(element.text))))
            if element.tag and isinstance(element.tag, str):
                x.update(hash_to_bytes(hash(ValueType(element.tag))))
            if element.attrib:
                x.update(hash_to_bytes(hash(ObjectType(dict(element.attrib)))))
        digest = x.intdigest()
        return digest


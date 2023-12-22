import xml.etree.ElementTree as ET

class Artist:
    _counter: int

    def __init__(self, original_id, name):
        Artist._counter += 1
        self._id = Artist._counter        
        self._original_id = original_id
        self._name = name

    def to_xml(self):
        el = ET.Element("Artist")
        el.set("id", str(self._id))
        el.set("originalId", self._original_id)
        
        if self._name:
            name_elem = ET.Element("Name")
            name_elem.text = self._name
            el.append(name_elem)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"

Artist._counter = 0

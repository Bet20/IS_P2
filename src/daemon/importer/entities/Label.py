import xml.etree.ElementTree as ET

class Label:
    _counter: int
    _name: str

    def __init__(self, original_id, name, company_name):
        Label._counter += 1
        self._id = Label._counter
        self._original_id = original_id
        self._name = name
        self._company_name = company_name

    def to_xml(self):
        el = ET.Element("Label")
        el.set("id", str(self._id))
        el.set("originalId", str(self._original_id))

        if self._name:
            name_elem = ET.Element("Name")
            name_elem.text = self._name
            el.append(name_elem)

        if self._company_name:
            company_elem = ET.Element("CompanyName")
            company_elem.text = self._company_name
            el.append(company_elem)
        
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}, company name: {self._company_name}"

    def __eq__(self, __value) -> bool:
        return self._name == __value._name and self._company_name == __value._company_name

Label._counter = 0

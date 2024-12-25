"""Infotech IPL XML."""
from lxml import etree as ET
from . import InfotechBase


class Typeobj:
    """Attributes of the TYPEOBJS IPL Infotech XML section."""

    Section = 'TYPEOBJS'
    Item = 'TYPEOBJ'
    SubItem = 'TITLE'
    Id = 'IDTYPEOBJ'


class Kamera:
    """Options for IPL_INSPECT.KZ_TYPE and KP_TYPE attributes."""

    Permanent = 1  # стационарная камера
    Temporary = 2  # временная камера
    Border = 3  # граница ЭО
    Armature = 4  # трубопроводная арматура
    Other = 5  # прочее (расшифровать)


class Inspect:
    """Attributes of the IPL_INSPECT Infotech XML item."""

    Title = 'IPL_INSPECT'

    Pipeline = "NLCH"  # "МГ Челябинск-Петровск"
    Place = "PLACE"  # "923,572-924 км (участок №1 L=195м)"
    L1 = "L1"  # "923,572"
    KzType = "KZ_TYPE"  # "2"
    L2 = "L2"  # "924"
    KpType = "KP_TYPE"  # "2"
    Isp = "ISP"  # "Газпроект-ДКР, ООО (г.Санкт-Петербург)"
    Start = "INSPECTION_START_DATE"  # "01.06.2018"
    End = "INSPECTION_END_DATE"  # "01.06.2018"


class Defect:
    """DEFECTS section."""

    Section = 'DEFECTS'
    Title = 'DEF'

    TypeId = "IDTYPEOBJ"  # "990004698869"
    Dist = "ODOMETER"  # "145"
    LOtch = "L_OTCH"  # "170"
    WOtch = "W_OTCH"  # "309"
    Vmin = "V_MIN_OTCH"  # "5"
    Vmax = "V_MAX_OTCH"  # "5"
    Orient1 = "ORIENT1"  # "7.2"
    Orient2 = "ORIENT2"  # "8.1"
    NumDef = "NUMDEF"  # "2"
    Rem = "REM"  # ""
    Kbd = "KBD"  # "0.70"
    Pbez = "PBEZ"  # ""
    TimeLimit = "TIME_LIMIT"  # "23.686"
    PbezPercent = "PBEZ_PERCENT"  # ""
    Method = "METHOD"  # "6907370"


class LineObj:
    """LINEOBJS section."""

    Section = 'LINEOBJS'
    Title = 'PLOBJ'

    TypeId = "IDTYPEOBJ"  # "990006537229"
    Dist = "ODOMETER"  # "0"
    Marker = "NAME_MARKER"  # "М1"
    Lch = "L_LCH"  # ""
    Rem = "REM"  # "(лоток запуска) 924 км"


class Weld:
    """WELDS section."""

    Section = 'WELDS'
    Title = 'WLD'

    TypeId = "IDTYPEOBJ"  # "2097791"
    Dist = "ODOMETER"  # "0"
    Num = "NUM_TUBE"  # "1"
    DlTube = "DL_TUBE"  # "752"
    Thick = "THICK"  # "19.5"
    Psh1 = "PSH1"  # "11.6"
    Psh2 = "PSH2"  # ""
    Rem = "REM"  # ""


class PigPass:
    """PIGPASS section."""

    Section = 'PIGPASS'
    Title = 'PASS'

    TypeId = "IDTYPEOBJ"  # "0"

    Date1 = "DATE1"  # "25.05.2018 10:58:00"
    Date2 = "DATE2"  # "25.05.2018 11:10:00"
    Speed = "SPEED_AVERAGE"  # "0.26"
    Rem = "REM"  # ""
    Manufact = "MANUFACTURER"  # "Саратоворгдиагностика"
    ManufactYear = "MANUFACT_DATE"  # "2010"
    PigType = "PIGTYPE"  # "990005096296"
    ObslType = "OBSLTYPE"  # "2"


class Infotech(InfotechBase):
    """Infotech IPL XML file."""

    def __init__(self):
        """Make new instance."""
        attribs = {
          Inspect.Pipeline: "",
          Inspect.Place: "",
          Inspect.L1: "",
          Inspect.KzType: "",
          Inspect.L2: "",
          Inspect.KpType: "",
          Inspect.Isp: "",
          Inspect.Start: "",
          Inspect.End: "",
        }
        self.root = ET.Element(Inspect.Title, attribs)
        self.typobjs = ET.SubElement(self.root, Typeobj.Section)
        self.defekts = ET.SubElement(self.root, Defect.Section)
        self.lineobjs = ET.SubElement(self.root, LineObj.Section)
        self.welds = ET.SubElement(self.root, Weld.Section)
        self.pigpass = ET.SubElement(self.root, PigPass.Section)

    def set_ipl(self, attr_dict):
        """Set attributes for IPL section."""
        self.set_attibs(self.root, attr_dict)

    def add_pigpass(self, attr_dict):
        """Add PASS item with given attributes to PIGPASS section."""
        attribs = {
          PigPass.TypeId: "",
          PigPass.Date1: "",
          PigPass.Date2: "",
          PigPass.Speed: "",
          PigPass.Rem: "",
          PigPass.Manufact: "",
          PigPass.ManufactYear: "",
          PigPass.PigType: "",
          PigPass.ObslType: "",
        }
        pigpass = ET.SubElement(self.pigpass, PigPass.Title, attribs)
        self.set_attibs(pigpass, attr_dict)

        return pigpass

    def add_weld(self, attr_dict):
        """Add WLD item with given attributes to WELDS section."""
        attribs = {
          Weld.TypeId: "",
          Weld.Dist: "",
          Weld.Num: "",
          Weld.DlTube: "",
          Weld.Thick: "",
          Weld.Psh1: "",
          Weld.Psh2: "",
          Weld.Rem: "",
        }
        weld = ET.SubElement(self.welds, Weld.Title, attribs)
        self.set_attibs(weld, attr_dict)

        return weld

    def add_lineobj(self, attr_dict):
        """Add PLOBJ item with given attributes to LINEOBJS section."""
        attribs = {
          LineObj.TypeId: "",
          LineObj.Dist: "",
          LineObj.Marker: "",
          LineObj.Lch: "",
          LineObj.Rem: "",
        }
        lobj = ET.SubElement(self.lineobjs, LineObj.Title, attribs)
        self.set_attibs(lobj, attr_dict)

        return lobj

    def add_defekt(self, attr_dict):
        """Add DEF item with given attributes to DEFECTS section."""
        attribs = {
          Defect.TypeId: "",
          Defect.Dist: "",
          Defect.LOtch: "",
          Defect.WOtch: "",
          Defect.Vmin: "",
          Defect.Vmax: "",
          Defect.Orient1: "",
          Defect.Orient2: "",
          Defect.NumDef: "",
          Defect.Rem: "",
          Defect.Kbd: "",
          Defect.Pbez: "",
          Defect.TimeLimit: "",
          Defect.PbezPercent: "",
          Defect.Method: "",
        }
        defekt = ET.SubElement(self.defekts, Defect.Title, attribs)
        self.set_attibs(defekt, attr_dict)

        return defekt

    def add_types(self, it_dict):
        """Add given dict to TYPEOBJS."""
        for code, name in it_dict.items():
            item = ET.SubElement(self.typobjs, Typeobj.Item, {
              Typeobj.Id: code,
            })
            subitem = ET.SubElement(item, Typeobj.SubItem)
            subitem.text = name

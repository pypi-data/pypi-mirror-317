"""Infotech TPO XML."""
from datetime import datetime
from lxml import etree as ET

from . import InfotechBase, InfotechError, it_date
from .codes.pypeline import PIPELINE_BY_NAMES


def get_abc(danger_code):
    """Return danger string for given code."""
    if danger_code in ["A", "a", "А", "а"]:
        return "Недопустимый (критический)"
    if danger_code in ["B", "b", "В", "в"]:
        return "Допустимый (ремонт)"
    # C
    return "Допустимый (малозначительный)"


class Typeobj:
    """Attributes of the TYPEOBJS TPO Infotech XML section."""

    Section = 'TYPEOBJS'
    Title = 'TYPEOBJ'

    Id = 'IDTYPEOBJ'
    Name = 'TITLE'


class Inspect:
    """Attributes of the TPO_INSPECT Infotech XML item."""

    Title = 'TPO_INSPECT'

    # ID трубопровода
    Idkc = "ID_KC"
    # Дата начала ВТД
    DateStart = "DATE_START"
    # Дата окончания ВТД
    DateEnd = "DATE_FINISH"
    ObslType = "OBSL_TYPE"
    Sposob = "SPOSOB_DIAGN"
    NumUch = "NUM_UCH"
    ObjDiagnUch = "OBJ_DIAGN_UCH"
    DistStartUch = "DIST_START_UCH"
    LengthUch = "LENGTH_UCH"
    IdInspect = "ID_INSPECT"
    MethodContr = "METHOD_CONTR"
    ErrLength = "ERR_LENGTH"
    ErrWidth = "ERR_WIDTH"
    ErrDepth = "ERR_DEPTH"


class Route:
    """Attributes of the ROUTE Infotech XML item."""

    Section = 'ROUTES'
    Title = 'ROUTE'

    Scheme = "ID_SCHEME"
    Idx = "IDX_ROUTE"
    Dfrom = "DFROM"
    Dto = "DTO"
    Plength_vto = "PLENGTH_VTO"
    Plength_vik = "PLENGTH_VIK"
    Plength_sv = "PLENGTH_SV"
    Plength_pv = "PLENGTH_PV"
    Flength_vto = "FLENGTH_VTO"
    Flength_vik = "FLENGTH_VIK"
    Flength_sv = "FLENGTH_SV"
    Flength_pv = "FLENGTH_PV"
    Descr = "DESCRIPTION"


class Elem:
    """Attributes of the ELEM Infotech XML item."""

    Title = 'ELEM'

    Num = "N_ELEM"  # "1.2"
    Vid = "VID_ELEM"  # "Сварное соединение"
    Oboznach = "OBOZNACH_ELEM"
    Name = "NAME_ELEM"
    Rasst1 = "RASST_ELEM1"
    Rasst2 = "RASST_ELEM2"
    Orient1 = "ORIENT1"
    Orient2 = "ORIENT2"
    Shift = "SHIFT"
    ThickMin = "THICK_ELEM_MIN"  # "17.3"
    ThickMax = "THICK_ELEM_MAX"  # "17.3"
    DiamMax = "DIAM_ELEM_MAX"  # "1400"
    Length = "LENGTH_ELEM"


class Defect:
    """Attributes of the DEFECT Infotech XML item."""

    Title = 'DEFECT'

    Num = "N_DEF"  # "2"
    Elem = "ELEMENT"  # "1.51"
    Kind = "ID_KIND"  # "5215283"
    Length1 = "LEN_DEF1"
    Length2 = "LEN_DEF2"
    Orient1 = "ORIENT1"  # "8"
    Orient2 = "ORIENT2"  # "9"
    Angle = "ANGLE_DEF"
    Length = "LENGTH"
    Width = "WIDTH"  # 248"
    Depth = "DEPTH"
    RelDepth = "REL_DEPTH"
    Rang = "RANG_OPASN"  # "Недопустимый (критический)"
    Recom = "RECOM"
    Meropr = "VID_MEROPR"  # "Замена"


class Infotech(InfotechBase):
    """Infotech TPO XML file."""

    def __init__(self):
        """Make new instance."""
        attribs = {
          Inspect.Idkc: "",
          Inspect.DateStart: "",
          Inspect.DateEnd: "",
          Inspect.ObslType: "",
          Inspect.Sposob: "",
          Inspect.NumUch: "",
          Inspect.ObjDiagnUch: "",
          Inspect.DistStartUch: "",
          Inspect.LengthUch: "",
          Inspect.IdInspect: "",
          Inspect.MethodContr: "",
          Inspect.ErrLength: "",
          Inspect.ErrWidth: "",
          Inspect.ErrDepth: "",
        }
        self.root = ET.Element(Inspect.Title, attribs)
        self.typobjs = ET.SubElement(self.root, Typeobj.Section)
        self.routes = ET.SubElement(self.root, Route.Section)

    def set_titul(
      self,
      pipeline_name,
      date_start,
      date_end,
      obsl_type,  # DefaultID.OBSL_TYPE
      sposob,  # DefaultID.SPOSOB_DIAGN
      id_inspect,  # DefaultID.ID_INSPECT
      method_contr,  # DefaultID.METHOD_CONTR
      type_dict
    ):
        """Set inspection attributes values."""
        pipeline_id = PIPELINE_BY_NAMES.get(pipeline_name)
        if pipeline_id is None:
            raise InfotechError("Газопровод '{}' не найден в словаре Инфотех.".format(pipeline_name))

        err = ""
        if not isinstance(date_start, datetime):
            err += "Неверная дата начала: '{}'\n".format(date_start)
        if not isinstance(date_end, datetime):
            err += "Неверная дата окончания: '{}'\n".format(date_end)

        if err:
            raise InfotechError(err)

        s_start = it_date(date_start)
        s_end = it_date(date_end)

        self.root.attrib[Inspect.Idkc] = pipeline_id
        self.root.attrib[Inspect.DateStart] = s_start
        self.root.attrib[Inspect.DateEnd] = s_end
        self.root.attrib[Inspect.ObslType] = obsl_type
        self.root.attrib[Inspect.Sposob] = sposob
        self.root.attrib[Inspect.IdInspect] = id_inspect
        self.root.attrib[Inspect.MethodContr] = method_contr

        self.add_types({pipeline_id: pipeline_name})
        self.add_types(type_dict)

    def add_route(self, iid, length, scheme_file_name):
        """Add new route with given ID and length."""
        s_len = "{:0.1f}".format(length)
        attribs = {
          Route.Scheme: scheme_file_name,
          Route.Idx: str(iid),
          Route.Dfrom: self.root.attrib[Inspect.DateStart],
          Route.Dto: self.root.attrib[Inspect.DateEnd],
          Route.Plength_vto: "",
          Route.Plength_vik: "",
          Route.Plength_sv: "",
          Route.Plength_pv: "",
          Route.Flength_vto: s_len,
          Route.Flength_vik: s_len,
          Route.Flength_sv: s_len,
          Route.Flength_pv: s_len,
          Route.Descr: "",
        }
        route = ET.SubElement(self.routes, Route.Title, attribs)

        return route

    def set_total_length(self, length):
        """Set inspection attribute of total length."""
        if not isinstance(length, float):
            raise InfotechError("Неверная длина участка: '{}'\n".format(length))

        self.root.attrib[Inspect.LengthUch] = "{:0.1f}".format(length)

    def set_oboznach(self, elem, text):
        """Set attribute ELEM.OBOZNACH_ELEM with givem text."""
        elem.attrib[Elem.Oboznach] = text

    def set_sdt(self, elem, dist, orient1, orient2, length, diam, thick):  # pylint: disable=too-many-arguments
        """Set SDT attributes for ELEM."""
        if isinstance(dist, (int, float)):
            elem.attrib[Elem.Rasst1] = "{:0.1f}".format(round(float(dist), 1))

        if isinstance(orient1, (int, float)):
            elem.attrib[Elem.Orient1] = str(round(float(orient1)))

        if isinstance(orient2, (int, float)):
            elem.attrib[Elem.Orient2] = str(round(float(orient2)))

        if isinstance(thick, (int, float)):
            text = "{:0.1f}".format(round(float(thick), 1))
            elem.attrib[Elem.ThickMin] = text
            elem.attrib[Elem.ThickMax] = text

        if isinstance(diam, int):
            elem.attrib[Elem.DiamMax] = str(diam)

        if isinstance(length, int):
            elem.attrib[Elem.Length] = str(length)

    def add_element(self, route, num, name):
        """Add ELEM item."""
        attribs = {
          Elem.Num: num,
          Elem.Vid: name,
          Elem.Oboznach: "",
          Elem.Name: "",
          Elem.Rasst1: "",
          Elem.Rasst2: "",
          Elem.Orient1: "",
          Elem.Orient2: "",
          Elem.Shift: "",
          Elem.ThickMin: "",
          Elem.ThickMax: "",
          Elem.DiamMax: "",
          Elem.Length: "",
        }
        return ET.SubElement(route, Elem.Title, attribs)

    def add_defect(
      self, route, elem_num, num, iid, from_weld, orient1, orient2, length, width, depth, danger, action
    ):  # pylint: disable=too-many-arguments
        """Set inspection attribute of total length."""
        attribs = {
          Defect.Num: str(num),
          Defect.Elem: str(elem_num),
          Defect.Kind: iid,
          Defect.Length1: "",
          Defect.Length2: "",
          Defect.Orient1: "",
          Defect.Orient2: "",
          Defect.Angle: "",
          Defect.Length: "",
          Defect.Width: "",
          Defect.Depth: "",
          Defect.RelDepth: "",
          Defect.Rang: "",
          Defect.Recom: "",
          Defect.Meropr: "",
        }
        item = ET.SubElement(route, Defect.Title, attribs)

        if isinstance(from_weld, int):
            item.attrib[Defect.Length1] = str(from_weld)

        if isinstance(orient1, (int, float)):
            item.attrib[Defect.Orient1] = str(round(float(orient1)))

        if isinstance(orient2, (int, float)):
            item.attrib[Defect.Orient2] = str(round(float(orient2)))

        if isinstance(length, int):
            item.attrib[Defect.Length] = str(length)

        if isinstance(width, int):
            item.attrib[Defect.Width] = str(width)

        if isinstance(depth, (int, float)):
            item.attrib[Defect.Depth] = "{:0.1f}".format(round(float(depth), 1))

        if isinstance(danger, str):
            item.attrib[Defect.Rang] = get_abc(danger)

        if isinstance(action, str):
            if action not in ["-"]:
                item.attrib[Defect.Meropr] = action

        return item

    def add_types(self, it_dict):
        """Add given dict to TYPEOBJS."""
        for code, name in it_dict.items():
            ET.SubElement(self.typobjs, Typeobj.Title, {
              Typeobj.Id: code,
              Typeobj.Name: name,
            })

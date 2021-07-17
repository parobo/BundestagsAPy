class Model:
    def __init__(self):
        pass
    @classmethod
    def parse(cls,json):
        pass
    @classmethod
    def parse_list(cls,json):
        pass

class Fundstelle(Model):
    @classmethod
    def parse(cls,json):
        fundstelle = cls()
        setattr(fundstelle, '_json', json)
        for k, v in json.items():
            setattr(fundstelle, k, v)
        return fundstelle
    
class Aktivitaet(Model):
    @classmethod
    def parse(cls,json):
        aktivitaet = cls()
        setattr(aktivitaet, '_json', json)
        for k, v in json.items():
            if k == 'fundstelle':
                fundstelle = Fundstelle.parse(v)
                setattr(aktivitaet,'fundstelle',fundstelle)
            else:
                setattr(aktivitaet, k, v)
        return aktivitaet
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class Drucksache(Model):
    @classmethod
    def parse(cls,json):
        ds = cls()
        setattr(ds, '_json', json)
        for k, v in json.items():
            if k == 'fundstelle':
                fundstelle = Fundstelle.parse(v)
                setattr(ds,'fundstelle',fundstelle)
            else:
                setattr(ds, k, v)
        return ds
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class DrucksacheText(Model):
    @classmethod
    def parse(cls,json):
        dst = cls()
        setattr(dst, '_json', json)
        for k, v in json.items():
            if k == 'fundstelle':
                fundstelle = Fundstelle.parse(v)
                setattr(dst,'fundstelle',fundstelle)
            else:
                setattr(dst, k, v)
        return dst
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class Person(Model):
    @classmethod
    def parse(cls,json):
        ps = cls()
        setattr(ps, '_json', json)
        for k, v in json.items():
            setattr(ps, k, v)
        return ps
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class Plenarprotokoll(Model):
    @classmethod
    def parse(cls,json):
        pp = cls()
        setattr(pp, '_json', json)
        for k, v in json.items():
            if k == 'fundstelle':
                fundstelle = Fundstelle.parse(v)
                setattr(pp,'fundstelle',fundstelle)
            else:
                setattr(pp, k, v)
        return pp
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class PlenarprotokollText(Model):
    @classmethod
    def parse(cls,json):
        ppt = cls()
        setattr(ppt, '_json', json)
        for k, v in json.items():
            if k == 'fundstelle':
                fundstelle = Fundstelle.parse(v)
                setattr(ppt,'fundstelle',fundstelle)
            else:
                setattr(ppt, k, v)
        return ppt
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class Vorgang(Model):
    @classmethod
    def parse(cls,json):
        vg = cls()
        setattr(vg, '_json', json)
        for k, v in json.items():
            setattr(vg, k, v)
        return vg
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results

class Vorgangsposition(Model):
    @classmethod
    def parse(cls,json):
        vgp = cls()
        setattr(vgp, '_json', json)
        for k, v in json.items():
            if k == 'fundstelle':
                fundstelle = Fundstelle.parse(v)
                setattr(vgp,'fundstelle',fundstelle)
            else:
                setattr(vgp, k, v)
        return vgp
    @classmethod
    def parse_list(cls,json_list):
        item_list = json_list['documents']
        results = []
        for item in item_list:
            results.append(cls.parse(item))
        return results
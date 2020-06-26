import json
import yaml
import os

schemav1 = "schema/dandiset.json"

mapping = {'identifier': ['identifier'],
           'name': ['name'],
           'description': ['description'],
           'contributors': ['contributor'],
           'sponsors': ['contributor', 'Sponsor'],
           'license': ['license'],
           'keywords': ['keywords'],
           'project': ['generatedBy'],
           'conditions_studied': ['about'],
           'associated_anatomy': ['about'],
           'protocols': ['protocol'],
           'ethicsApprovals': ['ethicsApproval'],
           'access': ['access'],
           'associatedData': ['relatedResource', 'IsDerivedFrom'],
           'publications': ['relatedResource', 'IsDescribedBy'],
           'age': ['variableMeasured'],
           'organism': ['variableMeasured'],
           'sex': ['variableMeasured'],
           'number_of_subjects': ['dandisetStats', 'numberOfSubjects']
           }


def toContributor(value):
    if not isinstance(value, list):
        value = [value]
    out = []
    for item in value:
        contrib = {}
        if "roles" in item:
            contrib["roleName"] = [f"{val.replace(' ', '')}" for val in
                                      item["roles"]]
            del item["roles"]
        if "awardNumber" in item:
            contrib["awardNumber"] = item["awardNumber"]
            del item["awardNumber"]
        if "orcid" in item:
            contrib["identifier"] = {"identifier": item["orcid"],
                                     "identifierType": "ORCID"}
            del item["orcid"]
        contrib.update(**{f"{k}":v for k,v in item.items()})
        out.append(contrib)
    return out


def convertv1(filename):
    with open(filename) as fp:
        data = json.load(fp)
    oldmeta = data["dandiset"] if "dandiset" in data else data
    newmeta = {}
    for oldkey, value in oldmeta.items():
        if oldkey in ['language']:
            continue
        if oldkey not in mapping:
            raise KeyError(f"Could not find {oldkey}")
        if len(mapping[oldkey]) == 0:
            newkey = f"schema:{oldkey}"
        else:
            newkey = mapping[oldkey][0]
        if oldkey in ['contributors', "sponsors"]:
            value = toContributor(value)
        if oldkey == "access":
            value = {"email": value["access_contact_email"],
                     "status": value["status"]}
        if oldkey == "identifier":
            value = {"identifier": value,
                     "identifierType": "DANDI"}
        if len(mapping[oldkey]) == 2:
            extra = mapping[oldkey][1]
            if newkey == 'contributor':
                extrakey = 'roleName'
            if oldkey == 'sponsors':
                extrakey = 'roleName'
            if oldkey in ['publications', 'associatedData']:
                extrakey = 'relation'
                if not isinstance(value, list):
                    value = [value]
                out = []
                for item in value:
                    out.append({k:v for k,v in item.items()})
                value = out
            if isinstance(value, list):
                for val in value:
                    val[extrakey] = extra
            if isinstance(value, dict):
                value[extrakey] = extra
        if newkey == 'variableMeasured':
            if oldkey in ["age", "sex"]:
                vm = {"name": oldkey}
                if oldkey == "sex":
                    vm["value"] = value
                else:
                    value["unitText"] = value["units"]
                    del value["units"]
                    vm.update(**value)
            else:
                newvalues = []
                for val in value:
                    if "species" in val:
                        newvalues.append(val["species"])
                vm = {"name": "species", "value": newvalues}
            value = vm
        if newkey not in newmeta:
            newmeta[newkey] = value
        else:
            curvalue = newmeta[newkey]
            if not isinstance(curvalue, list):
                newmeta[newkey] = [curvalue]
            if not isinstance(value, list):
                value = [value]
            newmeta[newkey].extend(value)
    print(yaml.dump(newmeta, indent=2,
                    default_flow_style=False))
    return newmeta


if __name__ == "__main__":
    filename = "scripts/dandiset_000004.json"
    convertv1(filename)

import json
import yaml

schemav1 = "/Users/satra/software/dandi/dandi-core/assets/schema/dandiset.json"

mapping = {'identifier': [],
           'name': [],
           'description': [],
           'contributors': ['dandi:contributor'],
           'sponsors': ['dandi:contributor', 'dandi:Sponsor'],
           'license': [],
           'keywords': [],
           'project': ['dandi:generatedBy'],
           'conditions_studied': ['schema:about'],
           'associated_anatomy': ['schema:about'],
           'protocols': ['dandi:protocol'],
           'ethicsApprovals': ['dandi:ethicsApproval'],
           'access': ['dandi:access'],
           'associatedData': ['dandi:relatedResource', 'dandi:IsDerivedFrom'],
           'publications': ['dandi:relatedResource', 'dandi:IsDescribedBy'],
           'age': ['schema:variableMeasured'],
           'organism': ['schema:variableMeasured'],
           'sex': ['schema:variableMeasured'],
           'number_of_subjects': ['dandi:numberOfSubjects']
           }


def toContributor(value):
    if not isinstance(value, list):
        value = [value]
    out = []
    for item in value:
        contrib = {}
        if "roles" in item:
            contrib["schema:roleName"] = [f"dandi:{val.replace(' ', '')}" for val in
                                      item["roles"]]
            del item["roles"]
        if "awardNumber" in item:
            contrib["dandi:awardNumber"] = item["awardNumber"]
            del item["awardNumber"]
        if "orcid" in item:
            contrib["schema:identifier"] = item["orcid"]
            del item["orcid"]
        contrib.update(**{f"schema:{k}":v for k,v in item.items()})
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
            value = {"schema:email": value["access_contact_email"],
                     "dandi:status": value["status"]}
        if len(mapping[oldkey]) == 2:
            extra = mapping[oldkey][1]
            if newkey == 'dandi:contributor':
                extrakey = 'schema:roleName'
            if oldkey == 'sponsors':
                extrakey = 'schema:roleName'
            if oldkey in ['publications', 'associatedData']:
                extrakey = 'dandi:relation'
                prefix = lambda x: "dandi:" if x in ["repository", "relation"] else "schema:"
                if not isinstance(value, list):
                    value = [value]
                out = []
                for item in value:
                    out.append({prefix(k)+k:v for k,v in item.items()})
                value = out
            if isinstance(value, list):
                for val in value:
                    val[extrakey] = extra
            if isinstance(value, dict):
                value[extrakey] = extra
        if newkey == 'schema:variableMeasured':
            if oldkey in ["age", "sex"]:
                vm = {"name": oldkey}
                if oldkey == "sex":
                    vm["value"] = value
                else:
                    value["unitText"] = value["units"]
                    del value["units"]
                    vm.update(**value)
            else:
                vm = {"name": "species", "value": value}
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
    filename = "/Users/satra/software/dandi/dandi-cli/tmp/dandiset_000004.json"
    #filename = "dandiset04.json"
    convertv1(filename)

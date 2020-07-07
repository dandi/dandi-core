from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field, AnyUrl, EmailStr
from typing import List, Union, Optional
from datetime import date


class AccessType(str, Enum):
    Open = "Open"
    Embargoed = "Embargoed"
    Restricted = "Restricted"


class License(str, Enum):
    cc0 = "CC0-1.0"
    ccby = "CC-BY-4.0"
    ccbync = "CC-BY-NC-4.0"
    pddl = "PDDL-1.0"


class RoleType(str, Enum):
    Author = "Author"
    Conceptualization = "Conceptualization"
    ContactPerson = "ContactPerson"
    DataCollector = "DataCollector"
    DataCurator = "DataCurator"
    DataManager = "DataManager"
    FormalAnalysis = "FormalAnalysis"
    FundingAcquisition = "FundingAcquisition"
    Investigation = "Investigation"
    Maintainer = "Maintainer"
    Methodology = "Methodology"
    Producer = "Producer"
    ProjectLeader = "ProjectLeader"
    ProjectManager = "ProjectManager"
    ProjectMember = "ProjectMember"
    ProjectAdministration = "ProjectAdministration"
    Researcher = "Researcher"
    Resources = "Resources"
    Software = "Software"
    Supervision = "Supervision"
    Validation = "Validation"
    Visualization = "Visualization"
    Funder = "Funder"
    Sponsor = "Sponsor"
    StudyParticipant = "StudyParticipant"
    Other = "Other"


class Relation(str, Enum):
    IsCitedBy = "IsCitedBy"
    Cites = "Cites"
    IsSupplementTo = "IsSupplementTo"
    IsSupplementedBy = "IsSupplementedBy"
    IsContinuedBy = "IsContinuedBy"
    Continues = "Continues"
    Describes = "Describes"
    IsDescribedBy = "IsDescribedBy"
    HasMetadata = "HasMetadata"
    IsMetadataFor = "IsMetadataFor"
    HasVersion = "HasVersion"
    IsVersionOf = "IsVersionOf"
    IsNewVersionOf = "IsNewVersionOf"
    IsPreviousVersionOf = "IsPreviousVersionOf"
    IsPartOf = "IsPartOf"
    HasPart = "HasPart"
    IsReferencedBy = "IsReferencedBy"
    References = "References"
    IsDocumentedBy = "IsDocumentedBy"
    Documents = "Documents"
    IsCompiledBy = "IsCompiledBy"
    Compiles = "Compiles"
    IsVariantFormOf = "IsVariantFormOf"
    IsOriginalFormOf = "IsOriginalFormOf"
    IsIdenticalTo = "IsIdenticalTo"
    IsReviewedBy = "IsReviewedBy"
    Reviews = "Reviews"
    IsDerivedFrom = "IsDerivedFrom"
    IsSourceOf = "IsSourceOf"
    IsRequiredBy = "IsRequiredBy"
    Requires = "Requires"
    Obsoletes = "Obsoletes"
    IsObsoletedBy = "IsObsoletedBy"


class IdentifierType(str, Enum):
    doi = "DOI"
    orcid = "ORCID"
    ror = "ROR"
    dandi = "DANDI"
    rrid = "RRID"
    none = "No identifier prefix"


class PropertyValue(BaseModel):
    maxValue: float = None
    minValue: float = None
    unitCode: Union[str, AnyUrl] = None
    unitText: str = None
    value: Union[bool, float, str, int, List[Union[bool, float, str, int]]] = None
    valueReference: PropertyValue = None
    propertyID: Union[str, AnyUrl] = None


PropertyValue.update_forward_refs()


class Identifier(BaseModel):
    identifier: Union[str, AnyUrl, PropertyValue]


class Contributor(BaseModel):
    identifier: Identifier = None
    name: str
    email: EmailStr = None
    url: AnyUrl = None
    roleName: List[RoleType]
    includeInCitation: bool = True
    awardNumber: str = None


class Person(Contributor):
    affiliation: List[str]


class Organization(Contributor):
    contactPoint: str


class EthicsApproval(BaseModel):
    identifier: Union[str, AnyUrl, Identifier] = None
    name: str
    url: str


class Resource(BaseModel):
    identifier: Identifier = None
    name: str = None
    url: str
    repository: Union[str, AnyUrl] = None
    relation: Relation


class About(BaseModel):
    identifier: Union[str, AnyUrl, Identifier] = None
    name: str = None


class AccessRequirements(BaseModel):
    status: AccessType
    email: EmailStr = None
    contactPoint: str = None
    description: str = None
    embargoedUntil: date = None


class DandisetStat(BaseModel):
    numberOfFiles: int = None
    numberOfSubjects: int = None
    numberOfSamples: int = None
    numberOfCells: int = None
    dataStandard: List[str] = None
    modality: List[str] = None


class Digest(BaseModel):
    value: str
    cryptoType: AnyUrl


class BioSample(BaseModel):
    assayType: AnyUrl
    anatomy: AnyUrl


class BaseDandiset(BaseModel):
    name: str
    description: str


class Dandiset(BaseDandiset):
    """A body of structured information describing a DANDI dataset
    """
    schemaVersion: str = Field(default="0.0.0", readonly=True)
    identifier: Identifier = Field(readonly=True)

    contributor: List[Union[Person, Organization]]

    license: License
    keywords: List[str]
    access: List[AccessRequirements]
    about: List[About] = None
    study_target: List[Union[str, AnyUrl]] = None
    protocol: List[str] = None
    ethicsApproval: List[EthicsApproval] = None
    relatedResource: List[Resource] = None
    acknowledgement: str = None

    # From assets
    measurementTechnique: List[str] = Field(readonly=True)
    variableMeasured: List[PropertyValue] = Field(readonly=True)
    dandisetStats: DandisetStat = Field(readonly=True)


class PublishedDandiset(Dandiset):
    # On publish
    version: str = Field(readonly=True)
    datePublished: date = Field(readonly=True)
    url: AnyUrl = Field(readonly=True)
    contentSize: str = Field(readonly=True)
    repository: AnyUrl = Field(readonly=True)
    manifestLocation: Union[AnyUrl, List[AnyUrl]] = Field(readonly=True)
    generatedBy: Optional[AnyUrl] = Field(None, readonly=True)


class Asset(BaseModel):
    schemaVersion: str = Field(default="0.0.0", readonly=True)
    identifier: Identifier = Field(readonly=True)
    contentUrl: List[AnyUrl]
    contentSize: str
    encodingFormat: Union[str, AnyUrl]
    digest: Digest
    name: str
    datePublished: date
    dataType: AnyUrl

    path: str = None

    sameAs: AnyUrl = None
    access: List[AccessRequirements]
    relatedResource: List[Resource] = None
    modality: List[str] = None
    measurementTechnique: List[str] = Field(readonly=True)
    variableMeasured: List[PropertyValue] = Field(readonly=True)

    isPartOf: Identifier = None
    generatedBy: Optional[AnyUrl] = Field(None, readonly=True)
    wasDerivedFrom: BioSample = None


# this is equivalent to json.dumps(MainModel.schema(), indent=2):
if __name__ == "__main__":
    #print(Dandiset.schema_json(indent=2))
    print(Asset.schema_json(indent=2))

from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field, AnyUrl, EmailStr
from typing import List, Union
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
    author = "Author"
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


class Person(BaseModel):
    identifier: str
    sameAs: AnyUrl
    name: str
    email: EmailStr
    affiliation: List[str]


class Organization(BaseModel):
    identifier: str
    sameAs: AnyUrl
    name: str
    email: EmailStr
    contactPoint: str


class Contributor(BaseModel):
    identifier: Union[Person, Organization]
    roleName: List[RoleType]
    awardNumber: str = None
    schemaVersion: str


class EthicsApproval(BaseModel):
    identifier: str
    name: str
    url: str


class Resource(BaseModel):
    identifier: str
    name: str
    url: str
    repository: AnyUrl
    relation: Relation


class AccessRequirements(BaseModel):
    status: AccessType
    email: EmailStr
    contactPoint: str
    description: str
    embargoedUntil: date


class DataDownload(BaseModel):
    pass


class PropertyValue(BaseModel):
    maxValue: float = None
    minValue: float = None
    unitCode: Union[str, AnyUrl] = None
    unitText: str = None
    value: Union[bool, float, str]
    valueReference: PropertyValue = None


PropertyValue.update_forward_refs()


class DandisetStat(BaseModel):
    numberOfFiles: int
    numberOfSubjects: int
    numberOfSamples: int = None
    numberOfCells: int = None
    dataStandard: List[str]
    modality: List[str]


class Dandiset(BaseModel):
    """A body of structured information describing a DANDI dataset
    """
    schemaVersion: str
    identifier: str
    name: str
    description: str

    citationOrder: List[int]
    contributor: List[Contributor]

    license: License = Field(...)
    keywords: List[str]
    about: List[str] = None
    study_target: List[Union[str, AnyUrl]]
    protocol: List[str] = None
    ethicsApproval: List[EthicsApproval] = None
    access: List[AccessRequirements]
    relatedResource: List[Resource] = None
    acknowledgement: str = None

    version: str

    distribution: List[DataDownload]
    datePublished: date
    url: AnyUrl
    contentSize: str
    repository: AnyUrl
    hasAssets: AnyUrl

    generatedBy: str

    measurementTechnigue: List[str] = None
    variableMeasured: List[PropertyValue] = None
    dandisetStats: DandisetStat


# this is equivalent to json.dumps(MainModel.schema(), indent=2):
print(Dandiset.schema_json(indent=2))

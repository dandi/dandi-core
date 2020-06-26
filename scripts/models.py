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


class IdentifierType(str, Enum):
    doi = "DOI"
    orcid = "ORCID"
    ror = "ROR"
    dandi = "DANDI"
    none = "No identifier prefix"


class Identifier(BaseModel):
    identifier: Union[str, AnyUrl]
    identifierType: IdentifierType


class Contributor(BaseModel):
    identifier: Identifier
    name: str
    email: EmailStr
    url: AnyUrl = None
    roleName: List[RoleType]
    includeInCitation: bool = True
    awardNumber: str = None


class Person(Contributor):
    affiliation: List[str]


class Organization(Contributor):
    contactPoint: str


class EthicsApproval(BaseModel):
    identifier: Identifier = None
    name: str
    url: str


class Resource(BaseModel):
    identifier: Identifier = None
    name: str = None
    url: str
    repository: AnyUrl = None
    relation: Relation


class AccessRequirements(BaseModel):
    status: AccessType
    email: EmailStr
    contactPoint: str
    description: str
    embargoedUntil: date


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
    schemaVersion: str = Field(default="0.0.0", readonly=True)
    identifier: Identifier = Field(readonly=True)
    name: str
    description: str

    contributor: List[Union[Person, Organization]]

    license: License
    keywords: List[str]
    access: List[AccessRequirements]
    about: List[str] = None
    study_target: List[Union[str, AnyUrl]] = None
    protocol: List[str] = None
    ethicsApproval: List[EthicsApproval] = None
    relatedResource: List[Resource] = None
    acknowledgement: str = None

    # From assets
    measurementTechnigue: List[str] = Field(readonly=True)
    variableMeasured: List[PropertyValue] = Field(readonly=True)
    dandisetStats: DandisetStat = Field(readonly=True)

    # On publish
    version: str = Field(readonly=True)
    datePublished: date = Field(readonly=True)
    url: AnyUrl = Field(readonly=True)
    contentSize: str = Field(readonly=True)
    repository: AnyUrl = Field(readonly=True)
    manifestLocation: AnyUrl = Field(readonly=True)
    generatedBy: str = Field(readonly=True)


# this is equivalent to json.dumps(MainModel.schema(), indent=2):
print(Dandiset.schema_json(indent=2))

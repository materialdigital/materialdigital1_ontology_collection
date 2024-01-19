# materialdigital1_ontology_collection
HAP 4 is preparing an overview of all ontologies created in the partner projects of MaterialDigitals first funding period. All partner projects should have received an email in which they are asked for their contribution. The purpose of this repo is to collect these contributions.

## List of ontologies
| Project Name | Namespace | Reference to own public resource |
| ------------ | --------- | -------------------------------- |
| [Ontology Publication Template](ont_pub_tmplt/) | https://w3id.org/pmd/ont_pub_tmplt/ | https://github.com/materialdigital/ontology_publication_template |
| [SensoTwin](SensoTwin/)                         |                                     |                                                                  |
| [DiProMag](DiProMag/) | https://www.dipromag.de/dipromag_onto/0.1/ | https://www.dipromag.de/dipromag_onto/0.1/ |
| [DiStAl](DiStAl/) | | |
| [KNOW-NOW](KNOW-NOW/) | | https://git.tu-berlin.de/felipebaca/know-now |
| [ODE_AM](ODE_AM/) | | |
| [SmaDi](SmaDi/) | <urn:absolute/smadiont#> | https://github.com/SmaDi-OBDMA/SmaDi-OBDMA-system |
| [GlasDigital](GlasDigital/) | https://w3id.org/pmd/glass-ontology/ | https://github.com/materialdigital/glasdigital-ontology |
| [iBain](iBain/) | | |
| [LeBeDigital](LeBeDigital/) | https://w3id.org/cpto | https://github.com/BAMresearch/LebeDigital |
| [DIGITRUBBER](DIGITRUBBER/) | | |
| [StahlDigital](StahlDigital/) | | |
| [KupferDigital](KupferDigital/) | | |
| [DigiBatMat](DigiBatMat/) | | |

## Technical requirements for ontologies
These requirements as well as the [Additional requirements for publishing ontologies](README.md#additional-requirements-for-publishing-ontologies) below are identical to the information in the spreadsheet, that was attached to the email about the umbrella paper.

### Ontology metadata
| Requirement | Description | Prefered property | Example |
| ----------- | ----------- | ----------------- | ------- |
| Title | Title of the ontology | `dcterms:title` | |
| Author, Creator, Maintainer | Identification of the creator(s) or maintainer(s) of the ontology. Wherever possible use an ORCID | `dcterms:creator` | `<https://orcid.org/0000-0000-0000-0000>` |
| Creation Date | Date of creation of the ontology | `dcterms:created` | |
| Version | Details about the version of the ontology, including updates and revisions. | `owl:versionInfo` **and** `owl:versionIRI` | |
| Ontology Description and Scope | Clear and concise decription of the onotlogy and its scope. | `rdfs:comment` | |
| Project | Identification of the projects creator(s) or maintainer(s) of the ontology. Include this in the rdfs:comment for "Ontology description and scope" | | |
| License | Information about the licensing and usage rights of the ontology. If you have not thought about this before, we recommend to consider CC-BY-4.0 | `dcterms:license` | `<http://creativecommons.org/licenses/by/4.0/>` |
| How to cite | Provide a citation example for the ontology, e.g. a scientific paper you published about your ontology. | `dcterms:bibliographicCitation` | |

### IRIs
| Requirement | Description | Prefered property | Example |
| ----------- | ----------- | ----------------- | ------- |
| Namespace | A **unique** namespace for the ontology to avoid conflicts and ensure clear identification. | | https://w3id.org/pmd/new_ontology/ |
| Dereferenceable IRIs | Internationalized Resource Identifiers (IRIs) should be dereferenciable for easy access and reference, if you have the capabilities to do so. | | |

### IRIs
| Requirement | Description | Prefered property | Example |
| ----------- | ----------- | ----------------- | ------- |
| Labels | Label of the classes and properties | `rdfs:label` or `skos:prefLabel` | |
| Definitions | Clear and concise definitions for all terms, concepts, and relationships within the ontology. | `rdfs:comment` or `skos:description` | |

## Additional requirements for publishing ontologies
### General
| Requirement | Description | Example |
| ----------- | ----------- | ------- |
| Documentation | Comprehensive documentation covering the ontology's purpose, scope, and structure. | |
| Accessibility | Accessable through www, publicly available | https://github.com/materialdigital/ontology_publication_template |
| Findability | Already published via scientific journal or terminology service or ontology repo or similar | |

### Interoperability
| Requirement | Description | Example |
| ----------- | ----------- | ------- |
| Top-Level grounding | To which top-level or mid-level is the ontology based on? | BFO, EMMO, PMDco, etc |
| Concept reuse | From which other ontologies are concepts reused? | QUDT, CHEBI, etc. |
| Format Standards | Serialize the ontology in RDF turtle. | ttl |
| OWL Complexity | Is the ontology OWL-DL conform or does it use other OWL variants | |

## How to contribute
Please fork the repository and create a pull request after completing the following tasks
1. Make sure your ontology/ontologies meet/s the requirements given in [Technical requirements for ontologies](README.md#technical-requirements-for-ontologies) and [Additional requirements for publishing ontologies](README.md#additional-requirements-for-publishing-ontologies)
2. Place your ontology files in your projects folder (feel free to change the directory names, but please keep the links in [README.md](README.md) consistent)
3. Edit the information in this [README.md](README.md)

## Where to find help
If you have questions about your contribution HAP 4 is happy to help. Please get in touch by using the discussion of the pull requests tool or contact us directly.
A minimal publication template for an ontology that fulfils the requirements mentioned above is provided in [https://github.com/materialdigital/ontology_publication_template](https://github.com/materialdigital/ontology_publication_template). You're welcome to use this as a template for your own work. It also includes automated production and publication of different serializations and of a html documentation.

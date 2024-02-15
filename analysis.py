import os
import re
import json
import rdflib
#import requests

with open('analysis_conf.json', 'r', encoding='utf-8') as f:
    conf = json.load(f)
    ADDITIONAL_BINDINGS = [(binding['prefix'], rdflib.Namespace(binding['uri'])) for binding in conf['additional_bindings']]
    ADDITIONAL_BINDINGS = []
    SKIP_NAMESPACES = [rdflib.Namespace(ns) for ns in conf['skip_namespaces']]

def get_imports(g):
    qres = g.query(
        """
        SELECT ?b WHERE {
            ?a owl:imports ?b .
        }
        """
    )
    return {
        'count': len(qres),
        'items': [str(row.b) for row in qres]
    }

def reason(g, rg, reasoner):
    raise NotImplementedError("Automatic reasoning not implemented yet")
    #if not os.path.isfile('robot.jar'):
    #    r = requests.get('https://github.com/ontodev/robot/releases/download/v1.9.5/robot.jar')
    #    with open('robot.jar', 'wb') as f:
    #        f.write(r.content)
    #if not os.path.isfile('robot.bat'):
    #    r = requests.get('https://raw.githubusercontent.com/ontodev/robot/master/bin/robot.bat')
    #    with open('robot.bat', 'wb') as f:
    #        f.write(r.content)

def get_processingnodes(g, startswith_filter):
    qres_pmd207 = g.query(f"""
    SELECT ?a
    WHERE {{
        ?b rdfs:subClassOf+ <https://w3id.org/pmd/co/ProcessingNode> .
        BIND(STR(?b) AS ?a) .
        FILTER STRSTARTS( ?a, "{startswith_filter}" ) .
    }}""")
    qres_pmdbeta = g.query(f"""
    SELECT ?a
    WHERE {{
        ?b rdfs:subClassOf+ <https://material-digital.de/pmdco/ProcessNode> .
        BIND(STR(?b) AS ?a) .
        FILTER STRSTARTS( ?a, "{startswith_filter}" ) .
    }}""")
    return {
        'pmdco-2.0.7': {
            'count': len(qres_pmd207),
            'items': [str(row.a) for row in qres_pmd207]
        },
        'pmdco-v0.1-beta': {
            'count': len(qres_pmdbeta),
            'items': [str(row.a) for row in qres_pmdbeta]
        }
    }

def get_valueobjects(g, startswith_filter):
    qres = g.query(f"""
    SELECT ?a
    WHERE {{
        ?b rdfs:subClassOf+ <https://w3id.org/pmd/co/ValueObject> .
        BIND(STR(?b) AS ?a) .
        FILTER STRSTARTS( ?a, "{startswith_filter}" ) .
    }}""")
    return {
        'pmdco-2.0.7': {
            'count': len(qres),
            'items': [str(row.a) for row in qres]
        }
    }

def get_counts(g, startswith_filter):
    return {
        'owl:Class': sum(int(row.c) for row in g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?a a owl:Class .
                FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
            }}
            """
        )),
        'owl:ObjectProperty': sum(int(row.c) for row in g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?a a owl:ObjectProperty .
                FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
            }}
            """
        )),
        'owl:DatatypeProperty': sum(int(row.c) for row in g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?a a owl:DatatypeProperty .
                FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
            }}
            """
        ))
    }

def get_creators(g):
    qres = g.query(
        """
        SELECT ?b WHERE {
            ?a <http://purl.org/dc/terms/creator>|<http://purl.org/dc/terms/contributor>|<http://purl.org/dc/elements/1.1/creator> ?b .
        }
        """
    )
    return {
        'count': len(qres),
        'items': [str(row.b) for row in qres]
    }

def get_namespaces(g, skip=None):
    if skip is None:
        skip = []
    return {
        'count': sum(1 for _, u in g.namespaces() if u not in skip),
        'items': [{'prefix': p, 'uri': str(u)} for p, u in g.namespaces() if u not in skip]
    }

def get_tlos(g, startswith_filter):
    return {
        'pmdco-2.0.7': sum(int(row.c) for row in g.query(f"""
                            SELECT (COUNT(*) as ?c) WHERE {{
                                ?a rdfs:subClassOf+|rdfs:subPropertyOf+ ?b .
                                FILTER( STRSTARTS( STR(?b), "https://w3id.org/pmd/co" ) ) .
                                FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
                            }}
                        """)),
        'pmdco-v0.1-beta': sum(int(row.c) for row in g.query(f"""
                                SELECT (COUNT(*) as ?c) WHERE {{
                                    ?a rdfs:subClassOf+|rdfs:subPropertyOf+ ?b .
                                    FILTER( STRSTARTS( STR(?b), "https://material-digital.de/" ) ) .
                                    FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
                                }}
                            """)),
        'emmo': sum(int(row.c) for row in g.query(f"""
                    SELECT (COUNT(*) as ?c) WHERE {{
                        ?a rdfs:subClassOf+|rdfs:subPropertyOf+ ?b .
                        FILTER( STRSTARTS( STR(?b), "http://www.w3.org/2002/07/emmo" ) ) .
                        FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
                    }}
                """)),
        'cco': sum(int(row.c) for row in g.query(f"""
                    SELECT (COUNT(*) as ?c) WHERE {{
                        ?a rdfs:subClassOf+|rdfs:subPropertyOf+ ?b .
                        FILTER( STRSTARTS( STR(?b), "http://www.ontologyrepository.com/CommonCoreOntologies/" ) ) .
                        FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
                    }}
                """)),
        'obo': sum(int(row.c) for row in g.query(f"""
                    SELECT (COUNT(*) as ?c) WHERE {{
                        ?a rdfs:subClassOf+|rdfs:subPropertyOf+ ?b .
                        FILTER( STRSTARTS( STR(?b), "http://purl.obolibrary.org/obo/" ) ) .
                        FILTER( STRSTARTS( STR(?a), "{startswith_filter}" ) ) .
                    }}
                """))
    }

def get_license(g):
    qres = g.query(
        """
        SELECT ?b WHERE {
            ?a <http://purl.org/dc/terms/license>|<http://purl.org/dc/elements/1.1/license> ?b .
        }
        """
    )
    return {
        'count': len(qres),
        'items': [str(row.b) for row in qres]
    }

def get_reasoner_from_filename(filename):
    result = re.match(r".*\.([a-z]+)-(\d+(\.\d+){2,3})\.ttl", filename)
    return {'reasoner': result.group(1), 'version': result.group(2)}

def analyze_graph(
        graph_file,
        reasoned_graph_file=None,
        reasoner='hermit',
        additional_bindings=None,
        skip_namespaces=None,
        startswith_filter='',
        additional_parse=None,
    ):
    if additional_bindings is None:
        additional_bindings = ADDITIONAL_BINDINGS
    if skip_namespaces is None:
        skip_namespaces = SKIP_NAMESPACES
    if additional_parse is None:
        additional_parse = []
    graph = rdflib.Graph()
    graph.parse(graph_file)
    for uri in additional_parse:
        graph.parse(uri, format='text/turtle')

    reasoned_graph = rdflib.Graph()
    if reasoned_graph_file is not None:
        reasoner = get_reasoner_from_filename(os.path.basename(reasoned_graph_file))
        reasoned_graph.parse(reasoned_graph_file)
    else:
        reason(graph, reasoned_graph, reasoner)

    for p, ns in additional_bindings:
        graph.bind(p, ns)
        reasoned_graph.bind(p, ns)

    return {
        'reasoner': reasoner,
        'imports': get_imports(graph),
        'processingnodes': get_processingnodes(reasoned_graph, startswith_filter),
        'valueobjects': get_valueobjects(reasoned_graph, startswith_filter),
        'definitioncounts': get_counts(reasoned_graph, startswith_filter),
        'creators_contributors': get_creators(graph),
        'namespaces': get_namespaces(graph, skip=skip_namespaces),
        'tlos': {
            'original': get_tlos(graph, startswith_filter),
            'reasoned': get_tlos(reasoned_graph, startswith_filter)
        },
        'license': get_license(graph)
    }


if __name__ == '__main__':
    with open('DIGITRUBBER/DIGITRUBBER.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='DIGITRUBBER/digitrubber-full.owl',
                reasoned_graph_file='DIGITRUBBER/digitrubber-full.elk-0.5.0.ttl',
                startswith_filter='https://www.tib.eu/digitrubber'
            ),
            fp,
            indent=2
        )
    with open('KupferDigital/KupferDigital.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='KupferDigital/KupferDigital_rdflib/KupferDigital.ttl',
                reasoned_graph_file='KupferDigital/KupferDigital_rdflib/KupferDigital.pellet-2.2.0.ttl',
                startswith_filter='https://gitlab.com/kupferdigital/'
            ),
            fp,
            indent=2
        )
    with open('GlasDigital/GlasDigital.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='GlasDigital/pmd_go.ttl',
                reasoned_graph_file='GlasDigital/pmd_go.pellet-2.2.0.ttl',
                additional_parse=['https://raw.githubusercontent.com/materialdigital/core-ontology/v0.1-beta/pmdco_core.ttl'],
                startswith_filter='https://glasdigi.cms.uni-jena.de/glass/'
            ),
            fp,
            indent=2
        )
    with open('LeBeDigital/LeBeDigital.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='LeBeDigital/CPTO.ttl',
                reasoned_graph_file='LeBeDigital/CPTO.pellet-2.2.0.ttl',
                startswith_filter='https://w3id.org/cpto/'
            ),
            fp,
            indent=2
        )
    with open('DiProMag/DiProMag.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='DiProMag/dipromag_onto_01.ttl',
                reasoned_graph_file='DiProMag/dipromag_onto_01.elk-0.5.0.ttl',
                startswith_filter='https://www.dipromag.de/dipromag_onto/0.1/'
            ),
            fp,
            indent=2
        )
    with open('ODE_AM/ODE_AM.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='ODE_AM/ODE_AM_rdflib/ODE_AM.ttl',
                reasoned_graph_file='ODE_AM/ODE_AM_rdflib/ODE_AM.pellet-2.2.0.ttl',
                startswith_filter='https://w3id.org/ODE_AM/'
            ),
            fp,
            indent=2
        )
    with open('SensoTwin/SensoTwin.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='SensoTwin/PMDCollectionSensoTwin.ttl',
                reasoned_graph_file='SensoTwin/PMDCollectionSensoTwin-noindividuals.pellet-2.2.0.ttl',
                startswith_filter='http://w3id.org/sensotwin/'
            ),
            fp,
            indent=2
        )
    with open('SmaDi/SmaDi.json', 'w', encoding='utf-8') as fp:
        json.dump(
            analyze_graph(
                graph_file='SmaDi/smadi_ont.ttl',
                reasoned_graph_file='SmaDi/smadi_ont.pellet-2.2.0.ttl',
                startswith_filter='urn:absolute/smadiont'
            ),
            fp,
            indent=2
        )

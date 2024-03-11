import os
from datetime import datetime
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

def get_processes(g, startswith_filter):
    qres = g.query(f"""
    SELECT ?a
    WHERE {{
        ?b rdfs:subClassOf+ <https://w3id.org/pmd/co/Process> .
        BIND(STR(?b) AS ?a) .
        FILTER STRSTARTS( ?a, "{startswith_filter}" ) .
    }}""")
    return {
        'pmdco-2.0.7': {
            'count': len(qres),
            'items': [str(row.a) for row in qres]
        }
    }

def get_objects(g, startswith_filter):
    qres = g.query(f"""
    SELECT ?a
    WHERE {{
        ?b rdfs:subClassOf+ <https://w3id.org/pmd/co/Object> .
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
            ?a <http://purl.org/dc/terms/creator>|<http://purl.org/dc/terms/contributor>|<http://purl.org/dc/elements/1.1/creator>|<http://purl.org/dc/elements/1.1/contributor> ?b .
        }
        """
    )
    return {
        'count': len(qres),
        'items': [str(row.b) for row in qres]
    }

def get_namespaces(g, skip=None):
    #if skip is None:
    #    skip = []
    #return {
    #    'count': sum(1 for _, u in g.namespaces() if u not in skip),
    #    'items': [{'prefix': p, 'uri': str(u)} for p, u in g.namespaces() if u not in skip]
    #}
    if skip is None:
        skip = []
    namespaces = list(set(n[0] for n in re.findall(r'<(https?:\/\/([0-9A-z-_~\.]+[\/|#])+)', g.serialize(format='turtle'))))
    return {
        'count': sum(1 for ns in namespaces if ns not in skip),
        'items': [ns for ns in namespaces if ns not in skip]
    }


def get_tlos(g, startswith_filter):
    tlos_list = [
        ('pmdco-2.0.7', 'https://w3id.org/pmd/co/'),
        ('pmdco-v0.1-beta', 'https://material-digital.de/'),
        ('emmo', 'http://emmo.info/emmo'),
        ('cco', 'http://www.ontologyrepository.com/CommonCoreOntologies/'),
        ('bfo', 'http://purl.obolibrary.org/obo/BFO_'),
        ('ro', 'http://purl.obolibrary.org/obo/RO_'),
        ('iao', 'http://purl.obolibrary.org/obo/IAO_'),
        ('prov-o', 'http://www.w3.org/ns/prov#'),
        ('qudt', 'http://qudt.org/'),
        ('chebi', 'http://purl.obolibrary.org/obo/CHEBI_')
    ]
    retd = {}

    for tlo, tlo_namespace in tlos_list:
        npred = int(g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?s ?p ?o .
                FILTER( STRSTARTS( STR(?p), "{tlo_namespace}" ) ) .
                FILTER( STRSTARTS( STR(?s), "{startswith_filter}" ) ) .
            }}
            """
        ).bindings[0]['c'])
        nobj = int(g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?s ?p ?o .
                FILTER( STRSTARTS( STR(?o), "{tlo_namespace}" ) ) .
                FILTER( STRSTARTS( STR(?s), "{startswith_filter}" ) ) .
            }}
            """
        ).bindings[0]['c'])
        nsubc = int(g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?s rdfs:subClassOf+ ?o .
                FILTER( STRSTARTS( STR(?o), "{tlo_namespace}" ) ) .
                FILTER( STRSTARTS( STR(?s), "{startswith_filter}" ) ) .
            }}
            """
        ).bindings[0]['c'])
        nsubp = int(g.query(
            f"""
            SELECT (COUNT(*) as ?c) WHERE {{
                ?s rdfs:subPropertyOf+ ?o .
                FILTER( STRSTARTS( STR(?o), "{tlo_namespace}" ) ) .
                FILTER( STRSTARTS( STR(?s), "{startswith_filter}" ) ) .
            }}
            """
        ).bindings[0]['c'])
        retd.update({
            tlo: {
                'predicates': npred,
                'objects': nobj,
                'subclasses': nsubc,
                'subproperties': nsubp,
                'subclassesproperties': nsubc + nsubp,
                'total': npred + nobj + nsubc + nsubp
            }
        }
        )

    return retd

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
        changes=None
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
        'analysis_date': datetime.now().isoformat(),
        'changes': changes,
        'reasoner': reasoner,
        'imports': get_imports(graph),
        'processingnodes': get_processingnodes(reasoned_graph, startswith_filter),
        'valueobjects': get_valueobjects(reasoned_graph, startswith_filter),
        'processes': get_processes(reasoned_graph, startswith_filter),
        'objects': get_objects(reasoned_graph, startswith_filter),
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
    for project, kwargs in conf['projects'].items():
        start = datetime.now()
        with open(f'{project}/{project}.json', 'w', encoding='utf-8') as fp:
            json.dump(
                analyze_graph(**kwargs),
                fp,
                indent=2
            )
        print(f'Finished {project} after {str(datetime.now() - start):s}')

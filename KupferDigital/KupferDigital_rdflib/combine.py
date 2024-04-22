import rdflib

g = rdflib.Graph()
g.parse('KupferDigital/FTO2.0.4.ttl')
g.parse('KupferDigital/MTO3.0.2.ttl')
g.parse('KupferDigital/TSRTO3.0.0.ttl')
g.parse('KupferDigital/TTO3.0.2.ttl')

g.serialize('KupferDigital/KupferDigital_rdflib/KupferDigital.ttl', format='turtle')

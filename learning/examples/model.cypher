// Teaching example, not executed against a Neo4j server in this package.
// Run only in a dedicated empty learning database.
// MERGE uses stable IDs; name similarity is not entity resolution.
CREATE CONSTRAINT lot_id IF NOT EXISTS FOR (n:Lot) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT equipment_id IF NOT EXISTS FOR (n:Equipment) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT run_id IF NOT EXISTS FOR (n:Run) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (n:Document) REQUIRE n.id IS UNIQUE;

MERGE (l:Lot {id: 'L02'})
MERGE (e:Equipment {id: 'E01'})
SET e:InspectionTool
MERGE (d:Document {id: 'D02'})
MERGE (r:Run {id: 'RUN002'})
SET r.occurredAt = datetime('2026-11-03T10:00:00+09:00')
MERGE (r)-[:FOR_LOT]->(l)
MERGE (r)-[:USED_EQUIPMENT]->(e)
MERGE (r)-[:USED_DOCUMENT]->(d);

MATCH (l:Lot {id: 'L02'})<-[:FOR_LOT]-(r:Run)-[:USED_EQUIPMENT]->(e:Equipment)
MATCH (r)-[:USED_DOCUMENT]->(d:Document)
RETURN r.id AS run, e.id AS equipment, d.id AS document;

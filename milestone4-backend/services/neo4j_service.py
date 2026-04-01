from neo4j import GraphDatabase
from config import Config
from typing import Optional, List, Dict

class Neo4jService:
    def __init__(self):
        self.driver = None
        self.connected = False
        self._connect()
    
    def _connect(self):
        """Initialize Neo4j connection"""
        try:
            if not Config.NEO4J_URI:
                print("Neo4j: URI not configured")
                return

            # Try configured URI first.
            uri_candidates = [Config.NEO4J_URI]
            if Config.NEO4J_URI.startswith("neo4j+s://"):
                uri_candidates.append(Config.NEO4J_URI.replace("neo4j+s://", "neo4j+ssc://", 1))

            last_error = None
            for uri in uri_candidates:
                try:
                    driver = GraphDatabase.driver(
                        uri,
                        auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
                    )
                    driver.verify_connectivity()
                    self.driver = driver
                    self.connected = True
                    print(f"✓ Neo4j connected successfully ({uri})")
                    return
                except Exception as err:
                    last_error = err

            raise last_error if last_error else RuntimeError("Unknown Neo4j connection failure")
        except Exception as e:
            print(f"✗ Neo4j connection failed: {str(e)}")
            self.connected = False
            self.driver = None
    
    def query_graph(self, entity: str = '', relation: str = '', limit: int = 20) -> List[Dict]:
        """
        Query graph for entities and relations
        
        Args:
            entity: Filter by entity name (case-insensitive partial match)
            relation: Filter by relation type
            limit: Maximum results
        
        Returns:
            List of {head, relation, tail} dictionaries
        """
        if not self.connected or not self.driver:
            print("Neo4j not available, returning empty results")
            return []
        
        try:
            with self.driver.session() as session:
                # Build Cypher query with filters
                where_clauses = []
                params = {'limit': limit}
                
                if entity:
                    where_clauses.append("(toLower(h.name) CONTAINS toLower($entity) OR toLower(t.name) CONTAINS toLower($entity))")
                    params['entity'] = entity
                
                if relation:
                    where_clauses.append("type(r) = $relation")
                    params['relation'] = relation
                
                where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                
                query = f"""
                MATCH (h:Entity)-[r:RELATION]->(t:Entity)
                {where_clause}
                RETURN h.name AS head, r.type AS relation, t.name AS tail
                LIMIT $limit
                """
                
                result = session.run(query, params)
                rows = [dict(record) for record in result]
                return rows
        
        except Exception as e:
            print(f"Neo4j query error: {str(e)}")
            return []
    
    def count_entities(self) -> int:
        """Count total entities in graph"""
        if not self.connected or not self.driver:
            return 0
        
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (e:Entity) RETURN COUNT(e) AS count")
                return result.single()['count']
        except:
            return 0
    
    def count_relations(self) -> int:
        """Count total relations in graph"""
        if not self.connected or not self.driver:
            return 0
        
        try:
            with self.driver.session() as session:
                result = session.run("MATCH ()-[r:RELATION]->() RETURN COUNT(r) AS count")
                return result.single()['count']
        except:
            return 0
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            self.connected = False

# Singleton instance
neo4j_service = Neo4jService()

from typing import Dict, List, Any, Optional, Union
import logging
import asyncio
from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ServiceUnavailable, DatabaseError
from ..base.client import BaseClient

logger = logging.getLogger(__name__)

class Neo4jClient(BaseClient):
    """
    Asynchronous Neo4j client for graph database operations.
    Implements common graph operations with rate limiting and error handling.
    """

    def __init__(self, config_path: str = "config.yml", use_proxy: bool = False):
        """
        Initialize Neo4j client with configuration.
        
        Args:
            config_path: Path to config file
            use_proxy: Whether to use proxy settings
        """
        super().__init__('neo4j', config_path=config_path, use_proxy=use_proxy)
        
        # Initialize Neo4j driver with database config
        uri = self.config['database']['neo4j']['uri']
        auth_method = self.config['database']['neo4j']['credentials']['auth_method']
        
        if auth_method == 'NoAuth':
            auth = None
        else:
            auth = (
                self.config['database']['neo4j']['credentials']['username'],
                self.config['database']['neo4j']['credentials']['password']
            )
        
        self.driver = AsyncGraphDatabase.driver(
            uri,
            auth=auth,
            max_connection_lifetime=self.config['database']['neo4j'].get('max_connection_lifetime', 3600)
        )
        
        # Rate limiting settings
        self._requests_per_second = self.config['database']['neo4j'].get('requests_per_second', 20)
        self._rate_limiter = asyncio.Semaphore(self._requests_per_second)
        self._last_request_time = 0

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def close(self):
        """Close Neo4j driver and connections"""
        await self.driver.close()

    async def _execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Execute a Cypher query with rate limiting and error handling.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            List of records as dictionaries
        """
        async with self._rate_limiter:
            try:
                async with self.driver.session() as session:
                    result = await session.run(query, params or {})
                    records = await result.data()
                    return records
            except ServiceUnavailable as e:
                logger.error(f"Neo4j service unavailable: {str(e)}")
                raise
            except DatabaseError as e:
                logger.error(f"Neo4j database error: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in Neo4j query execution: {str(e)}")
                raise

    async def create_node(self, label: str, properties: Dict) -> Dict:
        """
        Create a new node with given label and properties.
        
        Args:
            label: Node label
            properties: Node properties
            
        Returns:
            Created node data
        """
        query = f"""
        CREATE (n:{label} $props)
        RETURN n
        """
        result = await self._execute_query(query, {"props": properties})
        return result[0]['n'] if result else None

    async def create_relationship(self, from_node_id: int, to_node_id: int, 
                                relationship_type: str, properties: Dict = None) -> Dict:
        """
        Create a relationship between two nodes.
        
        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            relationship_type: Type of relationship
            properties: Relationship properties
            
        Returns:
            Created relationship data
        """
        query = f"""
        MATCH (a), (b)
        WHERE ID(a) = $from_id AND ID(b) = $to_id
        CREATE (a)-[r:{relationship_type} $props]->(b)
        RETURN r
        """
        params = {
            "from_id": from_node_id,
            "to_id": to_node_id,
            "props": properties or {}
        }
        result = await self._execute_query(query, params)
        return result[0]['r'] if result else None

    async def get_node_by_id(self, node_id: int) -> Dict:
        """
        Retrieve a node by its ID.
        
        Args:
            node_id: Node ID
            
        Returns:
            Node data
        """
        query = """
        MATCH (n)
        WHERE ID(n) = $node_id
        RETURN n
        """
        result = await self._execute_query(query, {"node_id": node_id})
        return result[0]['n'] if result else None

    async def get_nodes_by_label(self, label: str, properties: Dict = None) -> List[Dict]:
        """
        Find nodes by label and optional properties.
        
        Args:
            label: Node label
            properties: Optional property filters
            
        Returns:
            List of matching nodes
        """
        query = f"""
        MATCH (n:{label})
        WHERE {' AND '.join([f'n.{k} = ${k}' for k in (properties or {})])}
        RETURN n
        """
        result = await self._execute_query(query, properties or {})
        return [record['n'] for record in result]

    async def get_relationships(self, node_id: int, relationship_type: str = None, 
                              direction: str = 'BOTH') -> List[Dict]:
        """
        Get relationships for a node.
        
        Args:
            node_id: Node ID
            relationship_type: Optional relationship type filter
            direction: 'OUTGOING', 'INCOMING', or 'BOTH'
            
        Returns:
            List of relationships
        """
        if direction.upper() not in ['OUTGOING', 'INCOMING', 'BOTH']:
            raise ValueError("direction must be 'OUTGOING', 'INCOMING', or 'BOTH'")

        rel_pattern = f"[r{':' + relationship_type if relationship_type else ''}]"
        if direction == 'OUTGOING':
            pattern = f"(n){rel_pattern}->()"
        elif direction == 'INCOMING':
            pattern = f"()-{rel_pattern}->(n)"
        else:
            pattern = f"()-{rel_pattern}-(n)"

        query = f"""
        MATCH {pattern}
        WHERE ID(n) = $node_id
        RETURN r
        """
        result = await self._execute_query(query, {"node_id": node_id})
        return [record['r'] for record in result]

    async def delete_node(self, node_id: int) -> bool:
        """
        Delete a node by ID.
        
        Args:
            node_id: Node ID to delete
            
        Returns:
            True if node was deleted
        """
        query = """
        MATCH (n)
        WHERE ID(n) = $node_id
        DETACH DELETE n
        """
        await self._execute_query(query, {"node_id": node_id})
        return True

    async def update_node(self, node_id: int, properties: Dict) -> Dict:
        """
        Update node properties.
        
        Args:
            node_id: Node ID to update
            properties: New properties to set
            
        Returns:
            Updated node data
        """
        query = """
        MATCH (n)
        WHERE ID(n) = $node_id
        SET n += $props
        RETURN n
        """
        result = await self._execute_query(query, {
            "node_id": node_id,
            "props": properties
        })
        return result[0]['n'] if result else None

    async def execute_cypher(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Execute a custom Cypher query.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            Query results
        """
        return await self._execute_query(query, params)

    async def batch_create_nodes(self, label: str, nodes_data: List[Dict]) -> List[Dict]:
        """
        Create multiple nodes in a batch operation.
        
        Args:
            label: Node label
            nodes_data: List of node properties
            
        Returns:
            List of created nodes
        """
        query = f"""
        UNWIND $nodes as node
        CREATE (n:{label})
        SET n = node
        RETURN n
        """
        result = await self._execute_query(query, {"nodes": nodes_data})
        return [record['n'] for record in result]

    async def batch_create_relationships(self, relationships: List[Dict]) -> List[Dict]:
        """
        Create multiple relationships in a batch operation.
        
        Args:
            relationships: List of relationship data (from_id, to_id, type, properties)
            
        Returns:
            List of created relationships
        """
        query = """
        UNWIND $rels as rel
        MATCH (a), (b)
        WHERE ID(a) = rel.from_id AND ID(b) = rel.to_id
        CREATE (a)-[r:rel.type]->(b)
        SET r = rel.properties
        RETURN r
        """
        result = await self._execute_query(query, {"rels": relationships})
        return [record['r'] for record in result]

    async def get_shortest_path(self, from_node_id: int, to_node_id: int, 
                              relationship_type: str = None) -> List[Dict]:
        """
        Find shortest path between two nodes.
        
        Args:
            from_node_id: Start node ID
            to_node_id: End node ID
            relationship_type: Optional relationship type filter
            
        Returns:
            Path as list of nodes and relationships
        """
        rel_pattern = f"[*{':' + relationship_type if relationship_type else ''}]"
        query = f"""
        MATCH path = shortestPath((a)-{rel_pattern}-(b))
        WHERE ID(a) = $from_id AND ID(b) = $to_id
        RETURN path
        """
        result = await self._execute_query(query, {
            "from_id": from_node_id,
            "to_id": to_node_id
        })
        return result[0]['path'] if result else None

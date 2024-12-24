from typing import Hashable, Callable
import os

class DAG:
    """A simple implementation of a Directed Acyclic Graph."""

    def __init__(self):
        self.dag_dict = {}     

    def add_node(self, node_to_add: Hashable):
        if node_to_add in self.dag_dict.keys():
            return
        
        self.dag_dict[node_to_add] = []

    def add_nodes_from(self, nodes_to_add: Hashable):
        [self.add_node(node_to_add) for node_to_add in nodes_to_add]

    def remove_node(self, node_to_remove: Hashable):
        if node_to_remove not in self.dag_dict.keys():
            return
        
        del self.dag_dict[node_to_remove]

        # Remove all edges to this node.
        for node in self.dag_dict:
            if node_to_remove in self.dag_dict[node]:
                self.dag_dict[node].remove(node_to_remove)

    def add_edge(self, source_node: Hashable, target_node: Hashable):
        """Add an edge. Note that it cannot contain any edge information, unlike in NetworkX."""
        edge_to_add = (source_node, target_node)
        if len(edge_to_add) != 2:
            raise ValueError("Edge tuple must contain exactly two nodes.")
        
        if not isinstance(edge_to_add[0], Hashable) or not isinstance(edge_to_add[1], Hashable):
            raise ValueError("Nodes in the edge must both be Hashable types")
        
        source_node = edge_to_add[0]
        target_node = edge_to_add[1]

        if source_node not in self.dag_dict.keys():
            self.add_node(source_node)

        if target_node not in self.dag_dict.keys():
            self.add_node(target_node)

        if target_node in self.dag_dict[source_node]:
            return
        
        self.dag_dict[source_node].append(target_node)

        if self.has_path(target_node, source_node):
            self.dag_dict[source_node].remove(target_node)
            raise ValueError(f"Adding the edge from {source_node} to {target_node} failed, as it would result in a cycle!")
        
    def add_edges_from(self, edges_to_add: list):
        [self.add_edge(edge_to_add[0], edge_to_add[1]) for edge_to_add in edges_to_add]

    def remove_edge(self, source_node: Hashable, target_node: Hashable):
        """Remove an edge."""
        edge_to_remove = (source_node, target_node)
        if len(edge_to_remove) != 2:
            raise ValueError("Edge tuple must contain exactly two nodes.")
        
        if not isinstance(edge_to_remove[0], Hashable) or not isinstance(edge_to_remove[1], Hashable):
            raise ValueError("Nodes in the edge must both be Hashable types")
        
        source_node = edge_to_remove[0]
        target_node = edge_to_remove[1]

        self.dag_dict[source_node].remove(target_node)

    def successors(self, node: Hashable):
        return self.dag_dict[node]
    
    def predecessors(self, node: Hashable):        
        return [n for n in self.dag_dict if node in self.dag_dict[n]]
    
    def in_degree(self, node: Hashable):
        return len(self.predecessors(node))
    
    def out_degree(self, node: Hashable):
        return len(self.successors(node))
    
    def descendants(self, node: Hashable, include_node: bool = False):
        """Get all downstream descendants of a node in no particular order."""
        descendants = set()

        def recurse_descendants(current_node):
            for successor in self.successors(current_node):
                if successor not in descendants:
                    descendants.add(successor)
                    recurse_descendants(successor)

        recurse_descendants(node)
        if include_node:
            descendants.add(node)
        return list(descendants)

    def ancestors(self, node: Hashable, include_node: bool = False):
        """Get all upstream ancestors of a node in no particular order."""
        ancestors = set()

        def recurse_ancestors(current_node):
            for predecessor in self.predecessors(current_node):
                if predecessor not in ancestors:
                    ancestors.add(predecessor)
                    recurse_ancestors(predecessor)

        recurse_ancestors(node)
        if include_node:
            ancestors.add(node)
        return list(ancestors)

    @property
    def nodes(self):
        """Return all of the nodes."""
        return tuple([n for n in self.dag_dict.keys()])
    
    @property
    def edges(self):
        return self._edges()

    def _edges(self, key: Callable = str):
        """Return all of the edges as a tuple of tuples.
        Sorts based on a custom key or by str() if no key is provided.
        """
        edges = [(source, target) for source in self.dag_dict for target in self.dag_dict[source]]

        # Use the provided key for sorting
        edges = sorted(edges, key=key)
            
        return tuple(edges)
    
    def subgraph(self, nodes_in_subgraph: list):
        """Return a subgraph of the current DAG that contains the specified nodes, and all of the edges between them."""
        subgraph = DAG()
        # Add the nodes
        for node in nodes_in_subgraph:
            subgraph.add_node(node)

        # Add the edges        
        for edge in self.edges:
            source = edge[0]
            target = edge[1]
            if source not in nodes_in_subgraph or target not in nodes_in_subgraph:
                continue

            subgraph.add_edge(source, target)

        return subgraph
    
    def reverse(self):
        """Reverse the order of the edges in the DAG."""
        edges = self.edges()
        # Remove all of the edges
        for edge in edges:
            self.remove_edge(edge)

        # Add all of the reversed edges
        for edge in edges:
            reversed_edge = (edge[1], edge[0],)
            self.add_edge(reversed_edge)

    def is_acyclic(self) -> bool:
        """Return True if the graph is acyclic, otherwise False, using DFS to detect cycles."""
        visited = set()
        recursion_stack = set()

        def dfs(node):
            # If the node is already in the recursion stack, we have a cycle
            if node in recursion_stack:
                return False
            # If the node has been visited and is not in the recursion stack, skip it
            if node in visited:
                return True

            # Mark the node as visited and add to the recursion stack
            visited.add(node)
            recursion_stack.add(node)

            # Recursively visit all successors
            for successor in self.successors(node):
                if not dfs(successor):
                    return False

            # Remove from recursion stack after all successors are visited
            recursion_stack.remove(node)
            return True

        # Check each node to ensure all components are covered
        for node in self.nodes():
            if node not in visited:
                if not dfs(node):
                    return False

        return True
    
    def topological_sort(self) -> list:
        """Return a topological sort of the DAG if it exists, else raise a ValueError for cyclic graphs."""
        # Create a dictionary to track the indegree of each node
        indegree_map = {node: self.indegree(node) for node in self.nodes}
        # Initialize a list to hold nodes with zero indegree
        zero_indegree_nodes = [node for node, indegree in indegree_map.items() if indegree == 0]
        sorted_nodes = []

        while zero_indegree_nodes:
            # Remove a node with zero indegree
            current_node = zero_indegree_nodes.pop()
            # Add it to the sorted list
            sorted_nodes.append(current_node)

            # For each successor of the current node, decrease its indegree by 1
            for successor in self.successors(current_node):
                indegree_map[successor] -= 1
                # If indegree becomes zero, add the successor to the list of zero indegree nodes
                if indegree_map[successor] == 0:
                    zero_indegree_nodes.append(successor)

        # Check if the sorting includes all nodes (to ensure there's no cycle)
        if len(sorted_nodes) != len(self.nodes):
            raise ValueError("Graph contains a cycle, so topological sort is not possible")

        return sorted_nodes

    def topological_generations(self) -> list:
        """Return the nodes in each topological generation as a list of lists."""
        # Create a dictionary to track the indegree of each node
        indegree_map = {node: self.indegree(node) for node in self.nodes}
        # Initialize a list to hold nodes with zero indegree (initial generation)
        zero_indegree_nodes = [node for node, indegree in indegree_map.items() if indegree == 0]
        generations = []

        while zero_indegree_nodes:
            # Current generation will be all nodes with zero indegree
            current_generation = zero_indegree_nodes[:]
            generations.append(current_generation)
            next_generation = []

            # Process each node in the current generation
            for node in current_generation:
                # Remove it from zero_indegree_nodes
                zero_indegree_nodes.remove(node)
                # For each successor, reduce its indegree by 1
                for successor in self.successors(node):
                    indegree_map[successor] -= 1
                    # If indegree becomes zero, it belongs to the next generation
                    if indegree_map[successor] == 0:
                        next_generation.append(successor)

            # Update zero_indegree_nodes with the nodes in the next generation
            zero_indegree_nodes = next_generation

        # Check if we covered all nodes (if not, the graph has a cycle)
        if sum(len(gen) for gen in generations) != len(self.nodes):
            raise ValueError("Graph contains a cycle, so topological generations are not possible")

        return generations
    
    def sorted_topological_generations(self, key: Callable = str) -> list:
        """Return the nodes in each topological generation as a list of lists,
        sorted within each generation based on the provided key."""
        # Get the topological generations without sorting within each generation
        generations = self.topological_generations()
        # Sort each generation based on the key
        sorted_generations = [sorted(generation, key=key) for generation in generations]
        return sorted_generations

    def has_path(self, start: Hashable, end: Hashable) -> bool:
        """Check if there is a path from start node to end node using DFS."""
        visited = set()

        def dfs(node):
            if node == end:
                return True
            visited.add(node)
            for successor in self.successors(node):
                if successor not in visited and dfs(successor):
                    return True
            return False

        return dfs(start)
    
    def hash(self, node: Hashable = None) -> int:
        """Return a unique hash for the graph based on the hash of its edges.
        If a node is provided, return a unique hash for the subgraph of the node's ancestors."""
        if node is None:
            return hash(self.edges())
        
        ancestors = self.ancestors(node, include_node=True)
        subgraph = self.subgraph(ancestors)
        return hash(subgraph.edges())
    
    def transitive_closure(self) -> "DAG":
        """Return the transitive closure of the DAG as a new DAG instance."""
        closure = DAG()
        
        # Add all nodes to the transitive closure
        for node in self.nodes:
            closure.add_node(node)
        
        # For each node, add edges to all reachable nodes
        for node in self.nodes:
            # Get all descendants of the current node
            descendants = self.descendants(node)
            for descendant in descendants:
                closure.add_edge((node, descendant))
        
        return closure    

    def relabel_nodes(self, mapping: dict):
        # Check for overlapping labels
        old_labels = set(mapping.keys())
        new_labels = set(mapping.values())
        overlap = old_labels & new_labels
        if overlap:
            # Build a directed graph to resolve the order of relabeling
            D = DAG()
            for old, new in mapping.items():
                if old != new:
                    D.add_edge(old, new)
            # Remove self-loops
            for node in D.nodes:
                if D.has_edge(node, node):
                    D.remove_edge(node, node)
            try:
                order = reversed(D.topological_sort())
            except ValueError as err:
                raise ValueError(
                    "The node label sets are overlapping and no ordering can "
                    "resolve the mapping. Use copy=True."
                ) from err
        else:
            # Non-overlapping labels
            order = [n for n in self.nodes if n in mapping]

        for old_label in order:
            new_label = mapping[old_label]
            if new_label == old_label:
                continue

            # Update the dag_dict keys
            self.dag_dict[new_label] = self.dag_dict.pop(old_label)

            # Replace old_label with new_label in successors
            for source in self.dag_dict:
                self.dag_dict[source] = [
                    mapping.get(target, target) if target == old_label else target
                    for target in self.dag_dict[source]
                ]

        return self

    def to_md_files(self, folder_path: str, callables_dict: dict) -> None:
        """Write the DAG to a set of markdown files in the specified folder, with YAML front matter.
        Intended to be compatible with the Cosma visualization tool: https://cosma.arthurperret.fr/user-manual.html#creating-content-text-files-markdown
        The possible fields in the front matter are:
        - title: The title of the node (required)
        - id: The unique identifier for the node (optional)
        - type/types: The type of the node (optional)
        - tags: The tags associated with the node (optional)
        - thumbnail: The path to the thumbnail image (optional)
        - begin: Timestamp for the beginning of the node (optional)
        - end: Timestamp for the end of the node (optional)
        Custom fields can be used if they are added to the record_metas field in the config.yml file."""
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
 
        # Write a markdown file for each node
        for node in self.nodes:
            try:
                title = callables_dict['title'](node)
                id = callables_dict['id'](node)
            except:
                raise Exception(f"Error: callable failed for node {node}")
            file_name = f"{title}_{id}.md"
            # Create the file path
            file_path = os.path.join(folder_path, file_name)
            # Get the node's successors
            successors = self.successors(node)
            # Write the file
            with open(file_path, "w") as f:
                f.write("---\n")
                f.write(f"title: {title}\n")
                f.write(f"id: {id}\n")
                f.write("---\n")
                for successor in successors:
                    successor_title = callables_dict['title'](successor)
                    successor_id = callables_dict['id'](successor)
                    f.write(f"[[{successor_id}|{successor_title}]]\n")
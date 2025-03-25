import torch

from external.GINFINITY.src.utils import (
    dotbracket_to_graph,
    dotbracket_to_forgi_graph,
    graph_to_tensor,
    forgi_graph_to_tensor,
    generate_slices,
)

def convert_structure_to_graph(structure, graph_encoding, device):
    """
    Convert an RNA secondary structure string to a graph and its tensor representation.
    """
    if graph_encoding == "standard":
        graph = dotbracket_to_graph(structure)
        tg = graph_to_tensor(graph)
    elif graph_encoding == "forgi":
        graph = dotbracket_to_forgi_graph(structure)
        tg = forgi_graph_to_tensor(graph)
    else:
        raise ValueError(f"Unknown graph encoding: {graph_encoding}")
    tg = tg.to(device)
    return graph, tg

def get_gin_embedding(model, graph_encoding, structures, device, L=None, keep_paired_neighbors=False, batch_size=1, cpus=1):
    """
    Given a list of RNA secondary structure strings and a loaded model,
    convert the structures to graphs and compute their embeddings.
    Processes the structures in batches (batch_size) and sets the number of CPU threads (cpus).
    
    Returns:
        List of lists of tuples (start_idx, embedding_str) for each structure.
    """
    if not isinstance(structures, list):
        structures = [structures]
    if device == "cpu" and cpus > 1:
        torch.set_num_threads(cpus)
    
    results = []
    for i in range(0, len(structures), batch_size):
        batch_structures = structures[i:i+batch_size]
        batch_results = []
        for structure in batch_structures:
            graph, tg = convert_structure_to_graph(structure, graph_encoding, device)
            model.eval()
            with torch.no_grad():
                if L is not None:
                    node_embs = model.get_node_embeddings(tg)
                    sorted_nodes = sorted(graph.nodes())
                    if len(sorted_nodes) < L:
                        batch_results.append([(-1, "")])
                        continue
                    embeddings = []
                    slices = generate_slices(graph, L, keep_paired_neighbors)
                    for start_idx, subgraph_H in slices:
                        subgraph_nodes = sorted(subgraph_H.nodes())
                        node_indices = [sorted_nodes.index(node) for node in subgraph_nodes]
                        if not node_indices:
                            continue
                        sub_embs = node_embs[node_indices]
                        batch_idx = torch.zeros(len(sub_embs), dtype=torch.long, device=device)
                        pooled = model.pooling(sub_embs, batch_idx)
                        sub_embedding = model.fc(pooled)
                        embedding_str = ','.join(f'{x:.6f}' for x in sub_embedding.cpu().numpy().flatten())
                        embeddings.append((start_idx, embedding_str))
                    batch_results.append(embeddings if embeddings else [(-1, "")])
                else:
                    embedding = model.forward_once(tg)
                    emb_str = ','.join(f'{x:.6f}' for x in embedding.cpu().numpy().flatten())
                    batch_results.append([(None, emb_str)])
        results.extend(batch_results)
    return results

def calculate_query_distances(query_vector, candidate_vectors, metric='squared', batch_size=512):
    """
    Compute the distance between a single query vector and a list of candidate vectors in batches.
    
    Parameters:
        query_vector (list or 1D array): The query embedding vector.
        candidate_vectors (list of lists or 2D array): The candidate embedding vectors.
        metric (str): Either 'squared' or 'cosine'. Default is 'squared'.
        batch_size (int): How many candidate rows to process per batch.
    
    Returns:
        List of distances (floats) corresponding to each candidate vector.
    """
    query_tensor = torch.tensor(query_vector, dtype=torch.float32)
    candidate_tensor = torch.tensor(candidate_vectors, dtype=torch.float32)
    n = candidate_tensor.shape[0]
    distances = []
    
    from tqdm import tqdm
    with tqdm(total=n, desc="Calculating distances", unit="row") as pbar:
        for i in range(0, n, batch_size):
            batch_candidates = candidate_tensor[i:i+batch_size]
            if metric == 'cosine':
                # Normalize query and batch candidates to avoid division by zero
                q_norm = query_tensor / (query_tensor.norm() + 1e-8)
                b_norm = batch_candidates / (batch_candidates.norm(dim=1, keepdim=True) + 1e-8)
                sim = torch.nn.functional.cosine_similarity(b_norm, q_norm.expand_as(batch_candidates), dim=1)
                batch_distances = (1 - sim).tolist()
            else:  # squared Euclidean distance
                diff = batch_candidates - query_tensor
                batch_distances = torch.sum(diff * diff, dim=1).tolist()
            distances.extend(batch_distances)
            pbar.update(len(batch_candidates))
    return distances
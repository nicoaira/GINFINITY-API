import torch

from external.GINFINITY.src.utils import (
    dotbracket_to_graph,
    dotbracket_to_forgi_graph,
    graph_to_tensor,
    forgi_graph_to_tensor,
    generate_slices,
)

def get_gin_embedding(model, graph_encoding, structure, device, L=None, keep_paired_neighbors=False):
    """
    Given an RNA secondary structure string and a loaded model,
    convert the structure to a graph and compute its embedding.
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
    model.eval()
    with torch.no_grad():
        if L is not None:
            node_embs = model.get_node_embeddings(tg)
            sorted_nodes = sorted(graph.nodes())
            n = len(sorted_nodes)
            if n < L:
                return [(-1, "")]
            embeddings = []
            slices = generate_slices(graph, L, keep_paired_neighbors)
            for start_idx, subgraph_H in slices:
                subgraph_nodes = sorted(subgraph_H.nodes())
                node_indices = [sorted_nodes.index(node) for node in subgraph_nodes]
                if not node_indices:
                    continue
                sub_embs = node_embs[node_indices]
                batch = torch.zeros(len(sub_embs), dtype=torch.long, device=device)
                pooled = model.pooling(sub_embs, batch)
                sub_embedding = model.fc(pooled)
                embedding_str = ','.join(f'{x:.6f}' for x in sub_embedding.cpu().numpy().flatten())
                embeddings.append((start_idx, embedding_str))
            return embeddings if embeddings else [(-1, "")]
        else:
            embedding = model.forward_once(tg)
            return [(None, ','.join(f'{x:.6f}' for x in embedding.cpu().numpy().flatten()))]

from llama_index import GPTTreeIndex, GPTVectorStoreIndex


def query_index_for_summary(index, prompt: str) -> str:
    if isinstance(index, GPTTreeIndex):
        return index.query(prompt, mode='summarize').response
    elif isinstance(index, GPTVectorStoreIndex):
        return index.query(prompt, response_mode='tree_summarize').response
    else:
        raise NotImplementedError(index)

import module.engine as en


def execute_query_rank_advanced(dataframe, dict_query, dict_matrices, dict_weights):
    """
    Execute a query on the inverted index and rank restaurants based on their similarity to the query using different fields

    Parameters:
        dataframe (pandas.DataFrame):
            A DataFrame where each row represents a document and each column represents a term.
        dict_query (dict):
            A dictionary where the keys are the names of the matrices and the values are the query vectors.
        dict_matrices (dict):
            A dictionary where the keys are the names of the matrices and the values are the matrices.
        dict_weights (dict):
            A dictionary where the keys are the names of the matrices and the values are the weights.
    
    Returns:
        pandas.DataFrame
            A DataFrame containing the documents sorted by their similarity to the query.
    
    """
    
    result = dataframe.copy()
    
    if not dict_query:
        result["similarity_score"] = 0.0
        return result

    score = {}
    for key, query in dict_query.items():
        cosine_similarities = en.compute_cosine_similarity(query, dict_matrices[key])
        score[key] = cosine_similarities
    
    # Combine the results from the different matrices
    combined_results = {}
    for key, cosine_similarities in score.items():
        for restaurant_id, similarity in cosine_similarities.items():
            if restaurant_id not in combined_results:
                combined_results[restaurant_id] = 0
            combined_results[restaurant_id] += similarity * dict_weights[key]
    

    result["similarity_score"] = result.index.map(cosine_similarities)
    
    result.sort_values(by="similarity_score", ascending=False, inplace=True)

    
    if combined_results:
        result["similarity_score"] = result.index.map(combined_results)
    else:
        result["similarity_score"] = 0.0
    
    result.sort_values(by="similarity_score", ascending=False, inplace=True)

    return result

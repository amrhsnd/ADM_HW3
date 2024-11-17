import numpy as np
from collections import defaultdict   

def vectorize_query(num_doc, vocabulary, inverted_index, processed_query):
    """
    Create a vector representation of the query using the TF-IDF values of the terms in the query.

    Parameters:
        num_doc (int):
            The number of documents in the corpus.
        vocabulary (dict):
            A dictionary where the keys are terms and the values are term IDs.
        inverted_index (dict):
            A dictionary where the keys are term IDs and the values are lists of document IDs where the term appears.
        processed_query (list):
            A list of processed terms in the query.
    
    Returns:
        dict
            A dictionary where the keys are term IDs and the values are the TF-IDF values of the terms in the query

    """
    # Create a set of unique terms in the query
    query_terms = set(processed_query)

    # Create a vector to store the TF-IDF values of the terms in the query
    query_vector = defaultdict(float)
    for term in query_terms:
        term_id = vocabulary.get(term)
        if term_id is not None:
            query_vector[term_id] = processed_query.count(term)
    
    # Compute the TF-IDF values of the terms in the query
    for term_id in query_vector.keys():
        idf = np.log10(num_doc / len(inverted_index[term_id]))
        query_vector[term_id] *= idf
    
    return query_vector

def vectorize_documents(num_doc, vocabulary, inverted_tf_idf):
    """ 
    Create a matrix where each row represents a document vector and each column represents a term vector, 
    storing the TF-IDF values for each term in each document.

    Parameters:
        df (pandas.DataFrame):
            A DataFrame where each row represents a document and each column represents a term.
        vocabulary (dict):
            A dictionary where the keys are terms and the values are term IDs.
        inverted_tf_idf (dict):
            A dictionary where the keys are term IDs and the values are lists of tuples, where each tuple contains 
            the document ID and the TF-IDF value of the term in that document.
    
    Returns:
        numpy.ndarray
            A matrix where each row represents a document vector and each column represents a term vector, 
            storing the TF-IDF values for each term in each document


    """
    num_terms = len(vocabulary)
    
    # Create a matrix to store the TF-IDF values for each term in each document
    tf_idf_matrix = np.zeros((num_doc, num_terms))
    
    # Iterate over each term in the vocabulary
    for term_id, term_weights in inverted_tf_idf.items():
        for restaurant_id, tf_idf in term_weights:
            tf_idf_matrix[restaurant_id - 1, term_id] = tf_idf  # Adjust restaurant_id by subtracting 1
    
    return tf_idf_matrix

def compute_cosine_similarity(query_vector, tf_idf_matrix, row=None):
    """
    Compute the cosine similarity between the query vector and each document vector in the TF-IDF matrix.

    Parameters:
        query_vector (dict):
            A dictionary where the keys are term IDs and the values are the term frequencies in the query.
        tf_idf_matrix (numpy.ndarray):
            A matrix where each row represents a document vector and each column represents a term vector. 
        row (list):
            A list of rows IDs for which cosine similarity is to be calculated. If not specified, all rows will be selected.

    Returns:
        dict
            A dictionary where the keys are restaurant IDs and the values are the cosine similarities between
            the query vector and the document vector.
        
    """
    
    cosine_similarities = {}

    if not row:     
        # Compute the cosine similarity between the query vector and each document vector
        for restaurant_id, doc_vector in enumerate(tf_idf_matrix):
            numerator = 0.0
            for term_id, tf in list(query_vector.items()):
                numerator += tf * doc_vector[term_id]
            denominator = np.linalg.norm(list(query_vector.values())) * np.linalg.norm(doc_vector)
            cosine_similarities[restaurant_id+1] = numerator / denominator if denominator != 0 else 0.0 # Adjust restaurant_id by adding 1
    else:
        for restaurant_id in row:
            doc_vector = tf_idf_matrix[restaurant_id-1] #Adjust restaurant_id
            numerator = 0.0
            for term_id, tf in list(query_vector.items()):
                numerator += tf * doc_vector[term_id]
            denominator = np.linalg.norm(list(query_vector.values())) * np.linalg.norm(doc_vector)
            cosine_similarities[restaurant_id] = numerator / denominator if denominator != 0 else 0.0 # Adjust restaurant_id by adding 1

    
    return cosine_similarities

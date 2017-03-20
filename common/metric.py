import numpy as np

# change this if using K > 100
denominator_table = np.log2(np.arange(2, 102))
gain_table = np.power(2, np.arange(0, 6)) - 1

def dcg_at_k(r, k, method=1):
    """Score is discounted cumulative gain (dcg)

    Relevance is positive real values.  Can use binary
    as the previous methods.

    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]

    Returns:
        Discounted cumulative gain
    """
    r = np.asarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            # return np.sum(x / denominator_table[:x.shape[0]])
            return np.sum([gain_table[e] for e in r ] / denominator_table[:r.shape[0]])
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.



def get_ndcg(r, k, method=1):
    """Score is normalized discounted cumulative gain (ndcg)

    Relevance orignally was positive real values.  Can use binary
    as the previous methods.

    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]

    Returns:
        Normalized discounted cumulative gain
    """
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)

    if not dcg_max:
        return 0.
    dcg = dcg_at_k(r, k, method)
    return dcg / dcg_max

def precision_at_k(r, k):
    right_cnt = 0
    total_cnt = min(len(r), k)
    if total_cnt == 0:
        return 1
    for i in range(0, total_cnt):
        if r[i] > 0:
            right_cnt += 1
    return float(right_cnt)/total_cnt


if __name__ == '__main__':
    print "worst of 1"
    worst = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print dcg_at_k(worst, 10), ',' , get_ndcg(worst, 10)
    print dcg_at_k(worst, 5), ',', get_ndcg(worst, 5)
    print dcg_at_k(worst, 3), ',', get_ndcg(worst, 3)
    print dcg_at_k(worst, 1), ',', get_ndcg(worst, 1)
    print "best of 5"
    best = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
    print dcg_at_k(best, 10), ',' , get_ndcg(best, 10)
    print dcg_at_k(best, 5), ',', get_ndcg(best, 5)
    print dcg_at_k(best, 3), ',', get_ndcg(best, 3)
    print dcg_at_k(best, 1), ',', get_ndcg(best, 1)
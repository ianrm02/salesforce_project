def calc_fuzzy_dist(s1, s2):
    """
    Use Dynamic Programming approach and the Levenstein distance algorithm to efficiently find the edit distance of 2 strings.

    Parameters:
        s1 (str): The first string.
        s2 (str): The second string to find the distance between. 

    Returns:
        int: The number of edits from s1 to s2.
    """
    dp = {}
    for i in range(len(s1)+1):
        dp[i,0] = i
    for j in range(len(s2)+1):
        dp[0,j] = j
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                c = 0
            else:
                c = 1
            dp[i,j] = min(dp[i, j-1]+1, dp[i-1, j]+1, dp[i-1,j-1]+c)
    
    return dp[i,j]
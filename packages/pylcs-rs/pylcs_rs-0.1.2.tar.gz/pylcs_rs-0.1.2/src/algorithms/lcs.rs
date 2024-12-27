
use crate::utf8::utf8_split;
/// Calculate the length of the longest common subsequence between two strings
///
/// # Arguments
/// * `s1` - First input string
/// * `s2` - Second input string
///
/// # Returns
/// * `usize` - Length of the longest common subsequence
///
/// # Examples
/// ```
/// use pylcs_rs::algorithms::lcs::sequence_length;
/// let length = sequence_length("ABCD", "ACBAD");
/// assert_eq!(length, 3); // "ACD" is the longest common subsequence
/// ```

pub fn sequence_length(s1: &str, s2: &str) -> usize {
    if s1.is_empty() || s2.is_empty() {
        return 0;
    }

    let v1 = utf8_split(s1);
    let v2 = utf8_split(s2);
    let (m, n) = (v1.len(), v2.len());

    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if v1[i-1] == v2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = dp[i-1][j].max(dp[i][j-1]);
            }
        }
    }

    dp[m][n]
}

/// Returns the index mapping from s1 to s2 based on the longest common subsequence
///
/// # Arguments
/// * `s1` - Source string
/// * `s2` - Reference string
///
/// # Returns
/// * `Vec<i32>` - Vector of indices where each element is either:
///   * An index in s2 where the character matches
///   * -1 if there is no match for that position
///
/// # Examples
/// ```
/// use pylcs_rs::algorithms::lcs::sequence_idx;
/// let indices = sequence_idx("ABCD", "ACBAD");
/// assert_eq!(indices, vec![0, 2, -1, 4]); // AB-D mapping
/// ```

pub fn sequence_idx(s1: &str, s2: &str) -> Vec<i32> {
    if s1.is_empty() {
        return Vec::new();
    }
    if s2.is_empty() {
        return vec![-1; utf8_split(s1).len()];
    }

    let v1 = utf8_split(s1);
    let v2 = utf8_split(s2);
    let (m, n) = (v1.len(), v2.len());

    // Create DP table and direction matrix
    let mut dp = vec![vec![0; n + 1]; m + 1];
    let mut direction = vec![vec![' '; n + 1]; m + 1];

    // Fill the dp table and track directions
    for i in 1..=m {
        for j in 1..=n {
            if v1[i-1] == v2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1;
                direction[i][j] = 'm'; // match
            } else if dp[i-1][j] >= dp[i][j-1] {
                dp[i][j] = dp[i-1][j];
                direction[i][j] = 'u'; // up
            } else {
                dp[i][j] = dp[i][j-1];
                direction[i][j] = 'l'; // left
            }
        }
    }

    // Backtrack to find the mapping
    let mut result = vec![-1; m];
    let mut i = m;
    let mut j = n;

    while i > 0 && j > 0 {
        match direction[i][j] {
            'm' => {
                result[i-1] = (j-1) as i32;
                i -= 1;
                j -= 1;
            }
            'u' => i -= 1,
            'l' => j -= 1,
            _ => unreachable!()
        }
    }

    result
}

/// Calculate the length of the longest common substring (consecutive subsequence)
///
/// # Arguments
/// * `s1` - First input string
/// * `s2` - Second input string
///
/// # Returns
/// * `usize` - Length of the longest common substring
///
/// # Examples
/// ```
/// use pylcs_rs::algorithms::lcs::string_length;
/// let length = string_length("ABCDE", "CDEFG");
/// assert_eq!(length, 3); // "CDE" is the longest common substring
/// ```
pub fn string_length(s1: &str, s2: &str) -> usize {
    if s1.is_empty() || s2.is_empty() {
        return 0;
    }

    let v1 = utf8_split(s1);
    let v2 = utf8_split(s2);
    let (m, n) = (v1.len(), v2.len());

    let mut dp = vec![vec![0; n + 1]; m + 1];
    let mut max_length = 0;

    for i in 1..=m {
        for j in 1..=n {
            if v1[i-1] == v2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1;
                max_length = max_length.max(dp[i][j]);
            }
        }
    }

    max_length
}

/// Find indices for the longest common substring between two strings
///
/// # Arguments
/// * `s1` - Source string
/// * `s2` - Reference string
///
/// # Returns
/// * `Vec<i32>` - Vector of indices where each element is either:
///   * An index in s2 where the character matches as part of the longest substring
///   * -1 if the character is not part of the longest common substring
///
/// # Examples
/// ```
/// use pylcs_rs::algorithms::lcs::string_idx;
/// let indices = string_idx("ABCDE", "CDEFG");
/// assert_eq!(indices, vec![-1, -1, 0, 1, 2]); // Maps "CDE" in both strings
/// ```
pub fn string_idx(s1: &str, s2: &str) -> Vec<i32> {
    if s1.is_empty() {
        return Vec::new();
    }
    if s2.is_empty() {
        return vec![-1; utf8_split(s1).len()];
    }

    let v1 = utf8_split(s1);
    let v2 = utf8_split(s2);
    let (m, n) = (v1.len(), v2.len());

    let mut dp = vec![vec![0; n + 1]; m + 1];
    let mut max_length = 0;
    let mut end_pos = (0, 0);

    // Fill the dp table and track the ending position of max substring
    for i in 1..=m {
        for j in 1..=n {
            if v1[i-1] == v2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1;
                if dp[i][j] > max_length {
                    max_length = dp[i][j];
                    end_pos = (i, j);
                }
            }
        }
    }

    // Create the mapping vector
    let mut result = vec![-1; m];
    let (i_end, j_end) = end_pos;

    // Fill in the indices for the longest common substring
    for i in 0..max_length {
        result[i_end - max_length + i] = (j_end - max_length + i) as i32;
    }

    result
}

/// Calculate the length of the longest common subsequence for multiple strings
///
/// # Arguments
/// * `s1` - String to compare against the list
/// * `str_list` - List of strings to compare with
///
/// # Returns
/// * `Vec<usize>` - Vector containing LCS lengths for each string in the list
///
/// # Examples
/// ```
/// use pylcs_rs::algorithms::lcs::sequence_of_list;
/// let list = vec!["ACBD".to_string(), "ACCD".to_string()];
/// assert_eq!(sequence_of_list("ABCD", &list), vec![3, 3]);
/// ```
pub fn sequence_of_list(s1: &str, str_list: &[String]) -> Vec<usize> {
    if s1.is_empty() {
        return vec![0; str_list.len()];
    }

    str_list.iter()
        .map(|s2| sequence_length(s1, s2))
        .collect()
}

/// Calculate the length of the longest common substring for multiple strings
///
/// # Arguments
/// * `s1` - String to compare against the list
/// * `str_list` - List of strings to compare with
///
/// # Returns
/// * `Vec<usize>` - Vector containing longest common substring lengths for each string
///
/// # Examples
/// ```
/// use pylcs_rs::algorithms::lcs::string_of_list;
/// let list = vec!["CDAB".to_string(), "BCDA".to_string()];
/// assert_eq!(string_of_list("ABCD", &list), vec![2, 3]);
/// ```
pub fn string_of_list(s1: &str, str_list: &[String]) -> Vec<usize> {
    if s1.is_empty() {
        return vec![0; str_list.len()];
    }

    str_list.iter()
        .map(|s2| string_length(s1, s2))
        .collect()
}

#[cfg(test)]
mod tests {
    use std::vec;

    use super::*;

    #[test]
    fn test_empty_strings() {
        assert_eq!(sequence_length("", ""), 0);
        assert_eq!(sequence_length("abc", ""), 0);
        assert_eq!(sequence_length("", "abc"), 0);
    }

    #[test]
    fn test_single_char() {
        assert_eq!(sequence_length("a", "a"), 1);
        assert_eq!(sequence_length("a", "b"), 0);
    }

    #[test]
    fn test_ascii_sequences() {
        assert_eq!(sequence_length("ABCD", "ACBAD"), 3);  // ABD
        assert_eq!(sequence_length("ABCDE", "ACE"), 3);   // ACE
        assert_eq!(sequence_length("ABCDE", "ABCDE"), 5); // ABCDE
    }

    #[test]
    fn test_unicode_sequences() {
        assert_eq!(sequence_length("你好世界", "你们好"), 2);      // 你好
        assert_eq!(sequence_length("こんにちは", "こんばんは"), 3); // こんは
    }

    #[test]
    fn test_mixed_sequences() {
        assert_eq!(sequence_length("Hello世界", "Hey世界!"), 4);  // "Hell" or "ell世"
        assert_eq!(sequence_length("ABC123", "ABC！123"), 6);    // "ABC123"
    }

    #[test]
    fn test_repeated_chars() {
        assert_eq!(sequence_length("AAAA", "AA"), 2);
        assert_eq!(sequence_length("AAAA", "AAA"), 3);
        assert_eq!(sequence_length("AAAA", "AAAA"), 4);
    }

    #[test]
    fn test_no_common_sequence() {
        assert_eq!(sequence_length("ABCD", "EFGH"), 0);
        assert_eq!(sequence_length("123", "abc"), 0);
        assert_eq!(sequence_length("你好", "안녕"), 0);
    }

    #[test]
    fn test_with_spaces() {
        assert_eq!(sequence_length("A B C", "ABC"), 3);
        assert_eq!(sequence_length("A B C", "A B C"), 5);
    }

    #[test]
    fn test_case_sensitivity() {
        assert_eq!(sequence_length("abcd", "ABCD"), 0);
        assert_eq!(sequence_length("Hello", "hello"), 4);
    }

    #[test]
    fn test_sequence_idx_empty_strings() {
        assert_eq!(sequence_idx("", ""), Vec::<i32>::new());
        assert_eq!(sequence_idx("abc", ""), vec![-1, -1, -1]);
        assert_eq!(sequence_idx("", "abc"), Vec::<i32>::new());
    }

    #[test]
    fn test_sequence_idx_single_char() {
        assert_eq!(sequence_idx("a", "a"), vec![0]);
        assert_eq!(sequence_idx("a", "b"), vec![-1]);
    }

    #[test]
    fn test_sequence_idx_ascii() {
        assert_eq!(sequence_idx("ABCD", "ACBAD"), vec![0, 2, -1, 4]); // A-CD
        assert_eq!(sequence_idx("ABCDE", "ACE"), vec![0, -1, 1, -1, 2]); // ACE
    }

    #[test]
    fn test_sequence_idx_unicode() {
        assert_eq!(sequence_idx("你好世界", "你们好"), vec![0, 2, -1, -1]); // 你好
        let result = sequence_idx("こんにちは", "こんばんは");
        assert!(result == vec![0, 1, -1, -1, 4] || result == vec![0, 3, -1, -1, 4]); // こんは
    }

    #[test]
    fn test_sequence_idx_repeated_chars() {
        let result = sequence_idx("AAA", "AA");
        assert!(result == vec![0, 1, -1] || result == vec![-1, 0, 1] );
        let result2 = sequence_idx("AAAA", "AA");
        assert!(result2 == vec![0, 1, -1, -1] || result2 == vec![-1, 0, 1, -1] || result2 == vec![-1, -1, 0, 1] || result2 == vec![0, -1, 1, -1] || result2 == vec![-1, 0, -1, 1] || result2 == vec![0, -1, -1, 1]);
    }

    #[test]
    fn test_sequence_idx_no_match() {
        assert_eq!(sequence_idx("ABC", "DEF"), vec![-1, -1, -1]);
        assert_eq!(sequence_idx("123", "abc"), vec![-1, -1, -1]);
    }

    #[test]
    fn test_sequence_idx_with_spaces() {
        assert_eq!(sequence_idx("A B", "AB"), vec![0, -1, 1]);
        assert_eq!(sequence_idx("A B", "A B"), vec![0, 1, 2]);
    }

    #[test]
    fn test_sequence_idx_exact_match() {
        let s = "ABCDE";
        let result = sequence_idx(s, s);
        assert_eq!(result, (0..5).collect::<Vec<i32>>());
    }

    #[test]
    fn test_string_length_empty() {
        assert_eq!(string_length("", ""), 0);
        assert_eq!(string_length("abc", ""), 0);
        assert_eq!(string_length("", "abc"), 0);
    }

    #[test]
    fn test_string_length_single_char() {
        assert_eq!(string_length("a", "a"), 1);
        assert_eq!(string_length("a", "b"), 0);
        assert_eq!(string_length("abc", "b"), 1);
    }

    #[test]
    fn test_string_length_ascii() {
        assert_eq!(string_length("ABCDE", "CDEFG"), 3); // "CDE"
        assert_eq!(string_length("ABCDEF", "XABCDE"), 5); // "ABCDE"
        assert_eq!(string_length("ABCDEF", "DEFABC"), 3); // "DEF" or "ABC"
    }

    #[test]
    fn test_string_length_unicode() {
        assert_eq!(string_length("你好世界", "世界你好"), 2); // "世界"
        assert_eq!(string_length("こんにちは", "はいこんにち"), 4); // "こんにち"
    }

    #[test]
    fn test_string_length_overlapping() {
        assert_eq!(string_length("ABABAB", "ABAB"), 4); // "ABAB"
        assert_eq!(string_length("AAAAAA", "AAA"), 3); // "AAA"
    }

    #[test]
    fn test_string_idx_empty() {
        assert_eq!(string_idx("", ""), Vec::<i32>::new());
        assert_eq!(string_idx("abc", ""), vec![-1, -1, -1]);
        assert_eq!(string_idx("", "abc"), Vec::<i32>::new());
    }

    #[test]
    fn test_string_idx_single_char() {
        assert_eq!(string_idx("a", "a"), vec![0]);
        assert_eq!(string_idx("a", "b"), vec![-1]);
        assert_eq!(string_idx("abc", "b"), vec![-1, 0, -1]);
    }

    #[test]
    fn test_string_idx_ascii() {
        assert_eq!(string_idx("ABCDE", "CDEFG"), vec![-1, -1, 0, 1, 2]); // Maps "CDE"
        assert_eq!(string_idx("ABCDEF", "XABCDE"), vec![1, 2, 3, 4, 5, -1]); // Maps "ABCDE"
    }

    #[test]
    fn test_string_idx_unicode() {
        assert_eq!(string_idx("你好世界", "世界你好"), vec![2, 3, -1, -1]); // Maps "你好"
        assert_eq!(string_idx("こんにちは", "はいこんにち"), vec![2, 3, 4, 5, -1]); // Maps "こんにち"
    }

    #[test]
    fn test_string_idx_overlapping() {
        assert_eq!(string_idx("ABABAB", "ABAB"), vec![0, 1, 2, 3, -1, -1]); // Maps "ABAB"
        assert_eq!(string_idx("AAAAAA", "AAA"), vec![0, 1, 2, -1, -1, -1]); // Maps "AAA"
    }

    #[test]
    fn test_sequence_of_list_empty() {
        let empty_list: Vec<String> = vec![];
        assert_eq!(sequence_of_list("test", &empty_list), Vec::<usize>::new());
        assert_eq!(string_of_list("test", &empty_list), Vec::<usize>::new());
    }

    #[test]
    fn test_sequence_of_list_single() {
        let list = vec!["ABCD".to_string()];
        assert_eq!(sequence_of_list("ABCD", &list), vec![4]);
        assert_eq!(string_of_list("ABCD", &list), vec![4]);
    }

    #[test]
    fn test_sequence_of_list_multiple() {
        let list = vec![
            "ACBD".to_string(),
            "ACCD".to_string(),
            "ABDC".to_string()
        ];
        assert_eq!(sequence_of_list("ABCD", &list), vec![3, 3, 3]);
    }

    #[test]
    fn test_string_of_list_multiple() {
        let list = vec![
            "CDAB".to_string(),
            "BCDA".to_string(),
            "ABCD".to_string()
        ];
        assert_eq!(string_of_list("ABCD", &list), vec![2, 3, 4]);
    }

    #[test]
    fn test_sequence_of_list_unicode() {
        let list = vec![
            "你好世界".to_string(),
            "世界你好".to_string(),
            "你好啊世界".to_string()
        ];
        assert_eq!(sequence_of_list("你好世界", &list), vec![4, 2, 4]);
    }

    #[test]
    fn test_string_of_list_unicode() {
        let list = vec![
            "你好世界".to_string(),
            "世界你好".to_string(),
            "你好啊世界".to_string()
        ];
        assert_eq!(string_of_list("你好世界", &list), vec![4, 2, 2]);
    }

    #[test]
    fn test_sequence_of_list_mixed_lengths() {
        let list = vec![
            "A".to_string(),
            "ABC".to_string(),
            "ABCDE".to_string()
        ];
        assert_eq!(sequence_of_list("ABCD", &list), vec![1, 3, 4]);
    }

    #[test]
    fn test_string_of_list_mixed_lengths() {
        let list = vec![
            "A".to_string(),
            "ABC".to_string(),
            "ABCDE".to_string()
        ];
        assert_eq!(string_of_list("ABCD", &list), vec![1, 3, 4]);
    }

    #[test]
    fn test_sequence_of_list_empty_strings() {
        let list = vec!["".to_string(), "ABC".to_string(), "".to_string()];
        assert_eq!(sequence_of_list("ABCD", &list), vec![0, 3, 0]);
        assert_eq!(string_of_list("ABCD", &list), vec![0, 3, 0]);
    }
}

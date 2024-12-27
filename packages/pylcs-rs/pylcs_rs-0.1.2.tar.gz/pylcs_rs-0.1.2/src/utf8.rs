/// Split a string into UTF-8 characters
///
/// # Arguments
/// * `s` - Input string
///
/// # Returns
/// * `Vec<String>` - Vector of individual UTF-8 characters
///
/// # Examples
/// ```
/// use pylcs_rs::utf8::utf8_split;
/// let result = utf8_split("Hello, 世界");
/// assert_eq!(result, vec!["H", "e", "l", "l", "o", ",", " ", "世", "界"]);
/// ```
pub fn utf8_split(s: &str) -> Vec<String> {
  s.chars().map(|c| c.to_string()).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_string() {
        let result = utf8_split("");
        assert_eq!(result, Vec::<String>::new());
    }

    #[test]
    fn test_ascii_only() {
        let result = utf8_split("Hello");
        assert_eq!(result, vec!["H", "e", "l", "l", "o"]);
    }

    #[test]
    fn test_with_spaces() {
        let result = utf8_split("a b c");
        assert_eq!(result, vec!["a", " ", "b", " ", "c"]);
    }

    #[test]
    fn test_unicode() {
        let result = utf8_split("你好，世界");
        assert_eq!(result, vec!["你", "好", "，", "世", "界"]);
    }

    #[test]
    fn test_mixed_ascii_unicode() {
        let result = utf8_split("Hello, 世界!");
        assert_eq!(result, vec!["H", "e", "l", "l", "o", ",", " ", "世", "界", "!"]);
    }

    #[test]
    fn test_special_characters() {
        let result = utf8_split("←→↑↓");
        assert_eq!(result, vec!["←", "→", "↑", "↓"]);
    }

    #[test]
    fn test_emoji() {
        let result = utf8_split("😀🌍🚀");
        assert_eq!(result, vec!["😀", "🌍", "🚀"]);
    }

    #[test]
    fn test_utf8_split() {
        assert_eq!(utf8_split("hello"), vec!["h", "e", "l", "l", "o"]);
        assert_eq!(utf8_split(""), Vec::<&str>::new());
        assert_eq!(utf8_split("🦀"), vec!["🦀"]);
        assert_eq!(utf8_split("こんにちは"), vec!["こ", "ん", "に", "ち", "は"]);
        assert_eq!(utf8_split("a b c"), vec!["a", " ", "b", " ", "c"]);
        assert_eq!(utf8_split("123"), vec!["1", "2", "3"]);
    }
}


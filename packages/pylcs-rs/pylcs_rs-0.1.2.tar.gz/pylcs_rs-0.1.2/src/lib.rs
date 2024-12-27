use pyo3::prelude::*;

pub mod algorithms;
pub mod utf8;

/// Calculate the length of the longest common subsequence.
#[pyfunction]
fn lcs_sequence_length(s1: &str, s2: &str) -> PyResult<usize> {
    Ok(algorithms::lcs::sequence_length(s1, s2))
}

/// Find indices mapping of the longest common subsequence.
#[pyfunction]
fn lcs_sequence_idx(s1: &str, s2: &str) -> PyResult<Vec<i32>> {
    Ok(algorithms::lcs::sequence_idx(s1, s2))
}

/// Calculate LCS lengths for a string against multiple strings.
#[pyfunction]
fn lcs_sequence_of_list(s1: &str, str_list: Vec<String>) -> PyResult<Vec<usize>> {
    Ok(algorithms::lcs::sequence_of_list(s1, &str_list))
}

/// Calculate the length of the longest common substring.
#[pyfunction]
fn lcs_string_length(s1: &str, s2: &str) -> PyResult<usize> {
    Ok(algorithms::lcs::string_length(s1, s2))
}

/// Find indices mapping of the longest common substring.
#[pyfunction]
fn lcs_string_idx(s1: &str, s2: &str) -> PyResult<Vec<i32>> {
    Ok(algorithms::lcs::string_idx(s1, s2))
}

/// Calculate longest common substring lengths for a string against multiple strings.
#[pyfunction]
fn lcs_string_of_list(s1: &str, str_list: Vec<String>) -> PyResult<Vec<usize>> {
    Ok(algorithms::lcs::string_of_list(s1, &str_list))
}

/// Alias for lcs_sequence_length for backward compatibility
#[pyfunction]
fn lcs(s1: &str, s2: &str) -> PyResult<usize> {
    lcs_sequence_length(s1, s2)
}

/// Alias for lcs_sequence_of_list for backward compatibility
#[pyfunction]
fn lcs_of_list(s1: &str, str_list: Vec<String>) -> PyResult<Vec<usize>> {
    lcs_sequence_of_list(s1, str_list)
}

/// Alias for lcs_string_length for backward compatibility
#[pyfunction]
fn lcs2(s1: &str, s2: &str) -> PyResult<usize> {
    lcs_string_length(s1, s2)
}

/// Alias for lcs_string_of_list for backward compatibility
#[pyfunction]
fn lcs2_of_list(s1: &str, str_list: Vec<String>) -> PyResult<Vec<usize>> {
    lcs_string_of_list(s1, str_list)
}

#[pymodule]
fn pylcs_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add main functions
    m.add_function(wrap_pyfunction!(lcs_sequence_length, m)?)?;
    m.add_function(wrap_pyfunction!(lcs_sequence_idx, m)?)?;
    m.add_function(wrap_pyfunction!(lcs_sequence_of_list, m)?)?;
    m.add_function(wrap_pyfunction!(lcs_string_length, m)?)?;
    m.add_function(wrap_pyfunction!(lcs_string_idx, m)?)?;
    m.add_function(wrap_pyfunction!(lcs_string_of_list, m)?)?;

    // Add aliases for backward compatibility
    m.add_function(wrap_pyfunction!(lcs, m)?)?;
    m.add_function(wrap_pyfunction!(lcs_of_list, m)?)?;
    m.add_function(wrap_pyfunction!(lcs2, m)?)?;
    m.add_function(wrap_pyfunction!(lcs2_of_list, m)?)?;

    Ok(())
}

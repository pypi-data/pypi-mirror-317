#![allow(non_snake_case)]

pub mod pocketoption;
pub mod error;

use pocketoption::{RawPocketOption, connect};
use pyo3::prelude::*;

#[pymodule]
#[pyo3(name = "BinaryOptionsToolsV2")]
fn BinaryOptionsTools(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(connect, m)?)?;

    m.add_class::<RawPocketOption>()?;
    Ok(())
}

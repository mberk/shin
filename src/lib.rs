use pyo3::prelude::*;

#[pyfunction]
fn optimise(
    inverse_odds: Vec<f64>,
    sum_inverse_odds: f64,
    n: u64,
    max_iterations: u64,
    convergence_threshold: f64,
) -> PyResult<(f64, f64, u64)> {
    let mut delta = f64::INFINITY;
    let mut z: f64 = 0.0;
    let mut iterations = 0;
    let denominator: f64 = (n - 2) as f64;
    while delta > convergence_threshold && iterations < max_iterations {
        let z0 = z;
        z = (inverse_odds
            .iter()
            .map(|io| (z.powi(2) + 4.0 * (1.0 - z) * io.powi(2) / sum_inverse_odds).sqrt())
            .sum::<f64>()
            - 2.0)
            / denominator;
        delta = (z - z0).abs();
        iterations += 1;
    }
    iterations += 1;
    Ok((z, delta, iterations))
}

/// Fast calculations for Shin's method
#[pymodule]
#[pyo3(name = "shin")]
fn shin(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(optimise, m)?)?;
    Ok(())
}

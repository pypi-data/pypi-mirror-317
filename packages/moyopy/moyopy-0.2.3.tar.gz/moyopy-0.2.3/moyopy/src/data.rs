mod hall_symbol;
mod setting;

pub use hall_symbol::PyHallSymbolEntry;
pub use setting::PySetting;

use pyo3::prelude::*;

use super::base::{PyMoyoError, PyOperations};
use moyo::data::{hall_symbol_entry, HallSymbol};
use moyo::{MoyoError, Operations, Setting};

#[pyfunction]
pub fn operations_from_number(
    number: i32,
    setting: Option<PySetting>,
) -> Result<PyOperations, PyMoyoError> {
    let setting = if let Some(setting) = setting {
        setting
    } else {
        PySetting(Setting::Spglib)
    };
    let hall_number = match setting.0 {
        Setting::HallNumber(hall_number) => hall_number,
        Setting::Spglib | Setting::Standard => *setting
            .0
            .hall_numbers()
            .get((number - 1) as usize)
            .ok_or(MoyoError::UnknownNumberError)?,
    };
    let entry = hall_symbol_entry(hall_number).unwrap();
    let hs = HallSymbol::new(entry.hall_symbol).ok_or(MoyoError::HallSymbolParsingError)?;

    let mut rotations = vec![];
    let mut translations = vec![];

    let coset = hs.traverse();

    let lattice_points = hs.centering.lattice_points();
    for t1 in lattice_points.iter() {
        for (r2, t2) in coset.rotations.iter().zip(coset.translations.iter()) {
            // (E, t1) (r2, t2) = (r2, t1 + t2)
            rotations.push(*r2);
            let t12 = (t1 + t2).map(|e| e % 1.);
            translations.push(t12);
        }
    }
    Ok(PyOperations::from(Operations::new(rotations, translations)))
}

#[cfg(test)]
mod tests {
    use nalgebra::vector;

    use super::operations_from_number;
    use moyo::base::Position;
    use moyo::Operations;

    fn unique_sites(position: &Position, operations: &Operations) -> Vec<Position> {
        let mut sites: Vec<Position> = vec![];
        for (rotation, translation) in operations
            .rotations
            .iter()
            .zip(operations.translations.iter())
        {
            let new_site = rotation.map(|e| e as f64) * position + translation;
            let mut overlap = false;
            for site in sites.iter() {
                let mut diff = site - new_site;
                diff -= diff.map(|x| x.round());
                if diff.iter().all(|x| x.abs() < 1e-4) {
                    overlap = true;
                    break;
                }
            }
            if !overlap {
                sites.push(new_site);
            }
        }
        sites
    }

    #[test]
    fn test_operations_from_number() {
        {
            // C2/c
            let operations = operations_from_number(15, None).unwrap();
            let operations = Operations::from(operations);
            let x = 0.1234;
            let y = 0.5678;
            let z = 0.9012;
            assert!(unique_sites(&vector![0.0, 0.0, 0.0], &operations).len() == 4);
            assert!(unique_sites(&vector![0.0, 0.5, 0.0], &operations).len() == 4);
            assert!(unique_sites(&vector![0.25, 0.25, 0.0], &operations).len() == 4);
            assert!(unique_sites(&vector![0.25, 0.25, 0.5], &operations).len() == 4);
            assert!(unique_sites(&vector![0.0, y, 0.25], &operations).len() == 4);
            assert!(unique_sites(&vector![x, y, z], &operations).len() == 8);
        }
        {
            // Pm-3m
            let operations = operations_from_number(221, None).unwrap();
            let operations = Operations::from(operations);
            let x = 0.1234;
            let y = 0.5678;
            let z = 0.9012;
            assert!(operations.num_operations() == 48);
            assert!(unique_sites(&vector![0.0, 0.0, 0.0], &operations).len() == 1);
            assert!(unique_sites(&vector![0.5, 0.5, 0.5], &operations).len() == 1);
            assert!(unique_sites(&vector![0.0, 0.5, 0.5], &operations).len() == 3);
            assert!(unique_sites(&vector![0.5, 0.0, 0.0], &operations).len() == 3);
            assert!(unique_sites(&vector![x, 0.0, 0.0], &operations).len() == 6);
            assert!(unique_sites(&vector![x, 0.5, 0.5], &operations).len() == 6);
            assert!(unique_sites(&vector![x, x, x], &operations).len() == 8);
            assert!(unique_sites(&vector![x, 0.5, 0.0], &operations).len() == 12);
            assert!(unique_sites(&vector![0.0, y, y], &operations).len() == 12);
            assert!(unique_sites(&vector![0.5, y, y], &operations).len() == 12);
            assert!(unique_sites(&vector![0.0, y, z], &operations).len() == 24);
            assert!(unique_sites(&vector![0.5, y, z], &operations).len() == 24);
            assert!(unique_sites(&vector![x, x, z], &operations).len() == 24);
            assert!(unique_sites(&vector![x, y, z], &operations).len() == 48);
        }
        {
            // Im-3m
            let operations = operations_from_number(229, None).unwrap();
            let operations = Operations::from(operations);
            let x = 0.1234;
            let y = 0.5678;
            let z = 0.9012;
            assert!(unique_sites(&vector![0.0, 0.0, 0.0], &operations).len() == 2);
            assert!(unique_sites(&vector![0.0, 0.5, 0.5], &operations).len() == 6);
            assert!(unique_sites(&vector![0.25, 0.25, 0.25], &operations).len() == 8);
            assert!(unique_sites(&vector![0.25, 0.0, 0.5], &operations).len() == 12);
            assert!(unique_sites(&vector![x, 0.0, 0.0], &operations).len() == 12);
            assert!(unique_sites(&vector![x, x, x], &operations).len() == 16);
            assert!(unique_sites(&vector![x, 0.0, 0.5], &operations).len() == 24);
            assert!(unique_sites(&vector![0.0, y, y], &operations).len() == 24);
            assert!(unique_sites(&vector![0.25, y, 0.5 - y], &operations).len() == 48);
            assert!(unique_sites(&vector![0.0, y, z], &operations).len() == 48);
            assert!(unique_sites(&vector![x, x, z], &operations).len() == 48);
            assert!(unique_sites(&vector![x, y, z], &operations).len() == 96);
        }
        {
            // Ia-3d
            let operations = operations_from_number(230, None).unwrap();
            let operations = Operations::from(operations);
            let x = 0.1234;
            let y = 0.5678;
            let z = 0.9012;

            assert!(unique_sites(&vector![0.0, 0.0, 0.0], &operations).len() == 16);
            assert!(unique_sites(&vector![0.125, 0.125, 0.125], &operations).len() == 16);
            assert!(unique_sites(&vector![0.125, 0.0, 0.25], &operations).len() == 24);
            assert!(unique_sites(&vector![0.375, 0.0, 0.25], &operations).len() == 24);
            assert!(unique_sites(&vector![x, x, x], &operations).len() == 32);
            assert!(unique_sites(&vector![x, 0.0, 0.25], &operations).len() == 48);
            assert!(unique_sites(&vector![0.125, y, 0.25 - y], &operations).len() == 48);
            assert!(unique_sites(&vector![x, y, z], &operations).len() == 96);
        }
    }
}

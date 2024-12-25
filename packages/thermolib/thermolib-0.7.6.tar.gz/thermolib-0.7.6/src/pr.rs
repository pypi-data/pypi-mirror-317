use thiserror::Error;
#[derive(Debug, Error)]
enum PrErr {
    #[error("t_flash diverge")]
    NotConvForT,
    #[error("property only in single phase")]
    OnlyInSinglePhase,
    #[error("property not in single phase")]
    NotInSinglePhase,
}
use anyhow::anyhow;
use pyo3::{pyclass, pymethods};
use std::f64::consts::SQRT_2;
/// Pr EOS
/// ```
/// use thermolib::Pr;
/// let Tc = 430.64; // K
/// let pc = 7886600.0; // Pa
/// let omega = 0.256;
/// let M = 0.064064; // kg/mol
/// let mut SO2 = Pr::new_fluid(Tc, pc, omega, M);
/// let _ = SO2.set_molar_unit();
/// if let Ok(_) = SO2.t_flash(273.15) {
///     println!("T_s={}", SO2.T_s().unwrap());
///     println!("p_s={}", SO2.p_s().unwrap());
///     println!("rho_v={}", SO2.rho_v().unwrap());
///     println!("rho_l={}", SO2.rho_l().unwrap());
/// }
/// SO2.tp_flash(273.15, 0.1e6);
/// println!("T={}", SO2.T().unwrap());
/// println!("p={}", SO2.p().unwrap());
/// println!("rho={}", SO2.rho().unwrap());
/// ```
#[pyclass]
#[allow(non_snake_case)]
pub struct Pr {
    Tc: f64,
    pc: f64,
    T: f64,
    p: f64,
    kappa: f64,
    ac: f64,
    bc: f64,
    A: f64,
    B: f64,
    R: f64,
    M: f64,
    Z: f64,
    Zc: f64,
    Zv: f64,
    Zl: f64,
    is_single_phase: bool,
}
#[allow(non_snake_case)]
impl Pr {
    fn calc_root(&mut self) {
        self.A = self.ac * (1.0 + self.kappa * (1.0 - (self.T / self.Tc).sqrt())).powi(2) * self.p
            / (self.R * self.T).powi(2);
        self.B = self.bc * self.p / (self.R * self.T);
        let b = -1.0 + self.B;
        let c = self.A - 3.0 * self.B.powi(2) - 2.0 * self.B;
        let d = -self.A * self.B + self.B.powi(2) + self.B.powi(3);
        let A = b.powi(2) - 3.0 * c;
        let B = b * c - 9.0 * d;
        let C = c.powi(2) - 3.0 * b * d;
        let Delta = B.powi(2) - 4.0 * A * C;
        if Delta.is_sign_negative() {
            let theta3 = ((2.0 * A * b - 3.0 * B) / (2.0 * A * A.sqrt())).acos() / 3.0;
            let x1 = (-b - 2.0 * A.sqrt() * theta3.cos()) / 3.0;
            let x2 = (-b + A.sqrt() * (theta3.cos() + 3_f64.sqrt() * theta3.sin())) / 3.0;
            let x3 = (-b + A.sqrt() * (theta3.cos() - 3_f64.sqrt() * theta3.sin())) / 3.0;
            let Zv = x1.max(x2).max(x3);
            let Zl = x1.min(x2).min(x3);
            if Zl.is_sign_negative() {
                self.Z = Zv;
                self.is_single_phase = true;
            } else {
                self.Zv = Zv;
                self.Zl = Zl;
                self.is_single_phase = false;
            }
        } else {
            let Y1 = A * b + 1.5 * (-B + Delta.sqrt());
            let Y2 = A * b + 1.5 * (-B - Delta.sqrt());
            self.Z = (-b - (Y1.cbrt() + Y2.cbrt())) / 3.0;
            self.is_single_phase = true;
        }
    }
    fn calc_lnfp(&self, Z: f64) -> f64 {
        Z - 1.0
            - (Z - self.B).ln()
            - self.A / (2.0 * SQRT_2 * self.B)
                * ((Z + 2.414 * self.B) / (Z - 0.414 * self.B)).abs().ln()
    }
    fn calc_diff_lnfpvl(&mut self) -> f64 {
        self.calc_root();
        if self.is_single_phase {
            if self.Z > self.Zc {
                self.calc_lnfp(self.Z)
            } else {
                -self.calc_lnfp(self.Z)
            }
        } else {
            self.calc_lnfp(self.Zv) - self.calc_lnfp(self.Zl)
        }
    }
}
#[pymethods]
#[allow(non_snake_case)]
impl Pr {
    #[new]
    pub fn new_fluid(Tc: f64, pc: f64, omega: f64, M: f64) -> Self {
        let R = 8.314462618;
        let Zc = 0.307;
        let mut pr = Pr {
            Zc,
            Tc,
            pc,
            R,
            M,
            kappa: 0.37464 + 1.54226 * omega - 0.26992 * omega.powi(2),
            ac: 0.45724 * (R * Tc).powi(2) / pc,
            bc: 0.07780 * R * Tc / pc,
            T: 0.0,
            p: 0.0,
            A: 0.0,
            B: 0.0,
            Z: 0.0,
            Zv: 0.0,
            Zl: 0.0,
            is_single_phase: false,
        };
        pr.tp_flash(273.15, 0.1E6);
        pr
    }
    pub fn set_molar_unit(&mut self) {
        if self.R > 10.0 {
            self.R *= self.M;
        }
        self.ac = 0.45724 * (self.R * self.Tc).powi(2) / self.pc;
        self.bc = 0.07780 * self.R * self.Tc / self.pc;
    }
    pub fn set_mass_unit(&mut self) {
        if self.R < 10.0 {
            self.R /= self.M;
        }
        self.ac = 0.45724 * (self.R * self.Tc).powi(2) / self.pc;
        self.bc = 0.07780 * self.R * self.Tc / self.pc;
    }
    pub fn t_flash(&mut self, T: f64) -> anyhow::Result<()> {
        self.T = T;
        let ps_max = self.pc - 1.0;
        let ps = crate::algorithms::brent_zero(
            |ps| {
                self.p = ps;
                self.calc_diff_lnfpvl()
            },
            1.0,
            ps_max,
        );
        if ps.is_nan() {
            Err(anyhow!(PrErr::NotConvForT))
        } else {
            Ok(())
        }
    }
    pub fn tp_flash(&mut self, T: f64, p: f64) {
        self.T = T;
        self.p = p;
        self.calc_root();
        if !self.is_single_phase {
            let lnfpv = self.calc_lnfp(self.Zv);
            let lnfpl = self.calc_lnfp(self.Zl);
            if lnfpv < lnfpl {
                self.Z = self.Zv;
            } else {
                self.Z = self.Zl;
            }
            self.is_single_phase = true;
        }
    }
    pub fn T(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Ok(self.T)
        } else {
            Err(anyhow!(PrErr::OnlyInSinglePhase))
        }
    }
    pub fn p(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Ok(self.p)
        } else {
            Err(anyhow!(PrErr::OnlyInSinglePhase))
        }
    }
    pub fn rho(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Ok(self.p / (self.Z * self.R * self.T))
        } else {
            Err(anyhow!(PrErr::OnlyInSinglePhase))
        }
    }
    pub fn T_s(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Err(anyhow!(PrErr::NotInSinglePhase))
        } else {
            Ok(self.T)
        }
    }
    pub fn p_s(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Err(anyhow!(PrErr::NotInSinglePhase))
        } else {
            Ok(self.p)
        }
    }
    pub fn rho_v(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Err(anyhow!(PrErr::NotInSinglePhase))
        } else {
            Ok(self.p / (self.Zv * self.R * self.T))
        }
    }
    pub fn rho_l(&self) -> anyhow::Result<f64> {
        if self.is_single_phase {
            Err(anyhow!(PrErr::NotInSinglePhase))
        } else {
            Ok(self.p / (self.Zl * self.R * self.T))
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_pr() {
        let Tc: f64 = 430.64; // K
        let pc = 7886600.0; // Pa
        let omega = 0.256;
        let M = 0.064064; // kg/mol
        let mut SO2 = Pr::new_fluid(Tc, pc, omega, M);
        let Tmin = (0.7 * Tc).floor() as i32;
        let Tmax = Tc.ceil() as i32;
        for T in Tmin..Tmax {
            if let Err(_) = SO2.t_flash(T as f64) {
                panic!();
            }
        }
    }
}

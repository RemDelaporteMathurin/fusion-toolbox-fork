import numpy as np
import matplotlib.pyplot as plt

class Bosch_Hale_reactivity:
    """Class for Bosch Hale reactivity (H.-S. Bosch and G.M. Hale 1992 Nucl. Fusion 32 611)

    Parameters
    ----------
    reaction : string
        String name for the fusion reaction

    """
    known_reactions = ["DDn", "DDp", "DTn", "D3Hep"]

    _DDn_Cs   = [5.43360e-12, 5.85778e-3, 7.68222e-3, 0.0, -2.96400e-6, 0.0, 0.0]
    _DDp_Cs   = [5.65718e-12, 3.41267e-3, 1.99167e-3, 0.0, 1.05060e-5, 0.0, 0.0]
    _DTn_Cs   = [1.1302e-9, 1.51361e-2, 7.51886e-2, 4.60643e-3, 1.35e-2, -1.0675e-4, 1.366e-5]
    _D3Hep_Cs = [5.51036e-10, 6.41918e-3, -2.02896e-3, -1.91080e-5, 1.35776e-4, 0.0, 0.0]

    _DDn_Bg = 31.3970
    _DDp_Bg = 31.3970
    _DTn_Bg = 34.3827
    _D3Hep_Bg = 68.7508

    _DDn_mr = 937814
    _DDp_mr = 937814
    _DTn_mr = 1124656
    _D3Hep_mr = 1124572

    _Cs_dict = {"DDn":_DDn_Cs, "DDp":_DDp_Cs, "DTn":_DTn_Cs, "D3Hep":_D3Hep_Cs}
    _Bg_dict = {"DDn":_DDn_Bg, "DDp":_DDp_Bg, "DTn":_DTn_Bg, "D3Hep":_D3Hep_Bg}
    _mr_dict = {"DDn":_DDn_mr, "DDp":_DDn_mr, "DTn":_DTn_mr, "D3Hep":_D3Hep_mr}

    def __init__(self, reaction):

        if reaction in self.known_reactions:
            self.reaction = reaction
        else:
            raise ValueError(f"Unknown reaction. Should be one of {self.known_reactions}")


    def get_reactivity(self, T_i):
        """Method to calculate the Bosch-Hale reactivity for the reaction

        Parameters
        ----------
        T_i : float
            Ion temperature in keV for the fusion reactivity

        Returns
        -------
        sigmaV : float
            Calculated Bosch-Hale parameterized in cm^3/s 
        """
        C  = self._Cs_dict[self.reaction]
        Bg = self._Bg_dict[self.reaction]
        mr = self._mr_dict[self.reaction]
        fraction_top    = T_i*(C[1] + T_i*(C[3] + T_i*C[5]))
        fraction_bottom = 1 + T_i*(C[2] + T_i*(C[4] + T_i*C[6]))

        theta = T_i/(1 - fraction_top/fraction_bottom)
        xi    = (Bg**2/(4*theta))**(1/3)

        sigmaV = C[0]*theta*np.sqrt(xi/(mr*T_i**3))*np.exp(-3*xi)

        return sigmaV


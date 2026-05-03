import numpy as np
import constants as cte

def getspaxdim(data, phdr, sky_bundles, expansion_factor=5):
    """
    define the dimensions of the spaxel array. Return values are
      Nx : number of spaxels in the x direction
      Ny : number of spaxels in the y direction
      dx : arcseconds between adjacent spaxels in the x direction
      dy : arcseconds between adjacent spaxels in the y direction

    MEGARA has hexagonal spaxels. To convert them from hexagons
    to squares a factor of numpy.sqrt(3) must be applied to NAXIS1.
    Then, the spatial grid x,y needs to be expanded so the irrational
    factor does not affect the spatial sampling. By default is 5,
    play with it by your own risk. The dimensions are then too large,
    but this will be fixed rebinning the very large cube in the
    2nd step.
    """
    Nspec = len(data)

    xpos_list, ypos_list = [], []

    # 1. Recolección de coordenadas usando f-strings modernos
    for ispec in range(Nspec):
        # Esto genera "001", "002"... directamente sin usar replace()
        fib_str = f"{ispec+1:03d}"

        if phdr.get(f"FIB{fib_str}_B") not in sky_bundles:
            # Calculamos y redondeamos
            x = (phdr[f"FIB{fib_str}_x"] + 5.0) * cte.PLATESCALE
            y = (phdr[f"FIB{fib_str}_y"] + 5.0) * cte.PLATESCALE
            xpos_list.append(round(x, 3))
            ypos_list.append(round(y, 3))

    # 2. Uso de NumPy para obtener arreglos ordenados y únicos (reemplaza a uniquelist)
    xpos = np.unique(xpos_list)
    ypos = np.unique(ypos_list)

    # 3. Vectorización del cálculo de separación entre spaxels usando np.diff()
    # np.diff resta automáticamente el elemento [i] del [i-1] en todo el arreglo
    xsteps = np.round(np.diff(xpos), 3)
    ysteps = np.round(np.diff(ypos), 3)

    # Obtenemos las separaciones únicas y evitamos posibles ceros matemáticos
    xsteps_unique = np.unique(xsteps)
    ysteps_unique = np.unique(ysteps)

    dxspax = np.min(xsteps_unique[xsteps_unique > 0])
    dyspax = np.min(ysteps_unique[ysteps_unique > 0])

    # 4. Cálculo final de las dimensiones de la matriz
    NXSPAX = int((np.max(xpos) - np.min(xpos)) / dxspax) + 1
    NYSPAX = int((np.max(ypos) - np.min(ypos)) / dyspax) + 1

    factor_Nxpix = np.sqrt(3) * expansion_factor

    return (
        int(round(NXSPAX * factor_Nxpix)),
        NYSPAX * expansion_factor,
        np.min(xpos),
        np.min(ypos),
        dxspax / factor_Nxpix,
        dyspax / expansion_factor,
    )

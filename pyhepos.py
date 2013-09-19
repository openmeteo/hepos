from math import pi
from pyproj import Proj, transform

from matfunc import Matrix, Vec

HTRS07_tx = 203.437
HTRS07_ty = -73.461
HTRS07_tz = -243.594

ARCSEC_TO_RAD = 2.0*pi/(360.0*60.0*60.0)

HTRS07_ex = -0.170 * ARCSEC_TO_RAD
HTRS07_ey = -0.060 * ARCSEC_TO_RAD
HTRS07_ez = -0.151 * ARCSEC_TO_RAD

HTRS07_ds = -0.294E-6

HTRS07_DISPLACEMENT_VECTOR = Vec([
        HTRS07_tx,
        HTRS07_ty,
        HTRS07_tz]
        )

HTRS07_ROTATION_MATRIX = Matrix(
        [[HTRS07_ds, HTRS07_ez, -HTRS07_ey],
         [-HTRS07_ez, HTRS07_ds, HTRS07_ex],
         [HTRS07_ey, -HTRS07_ex, HTRS07_ds]]
        )

def htrs07_to_egsa87_3d(x, y, z):
    """
    This is the first step according to the algorithm description
    for transforming HTRS07 X,Y,Z coordinates to GGRS87.
    This step implies (X,Y,Z)htrs07 -> (X,Y,Z)ggrs87
    """
    htrs07_coordinates_vector = Vec([x,y,z])
    result_vector= htrs07_coordinates_vector + HTRS07_DISPLACEMENT_VECTOR +\
            HTRS07_ROTATION_MATRIX.mmul(htrs07_coordinates_vector)
    return tuple(result_vector[i] for i in (0,1,2))

def htrs07_to_egsa87_en_temp(x, y, z):
    """
    This is the second step according to the algorithm description
    for transforming HTRS07 X,Y,Z coordinates to GGRS87.
    This step implies (X,Y,Z)htrs07 -> temporary (East, Northing)ggrs87

    This is not the final result of the transposition, it will involve
    some corrections.
    """
    coords = htrs07_to_egsa87_3d(x, y, z)
    return transform(Proj('+proj=geocent +ellps=GRS80'),
            Proj(init='epsg:2100'), *coords)


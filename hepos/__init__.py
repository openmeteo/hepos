from math import pi
from pyproj import Proj, transform

from matfunc import Matrix, Vec


# GGRS87 <-> HTRS07 displacement vector and rotation matrix, according
# to htrs07 documentation

HTRS07_tx = 203.437
HTRS07_ty = -73.461
HTRS07_tz = -243.594

HTRS07_tx_KASTELLORIZO = -5.020
HTRS07_ty_KASTELLORIZO = -19.885
HTRS07_tz_KASTELLORIZO = -12.244

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

HTRS07_DISPLACEMENT_VECTOR_KASTELLORIZO = Vec([
        HTRS07_tx_KASTELLORIZO,
        HTRS07_ty_KASTELLORIZO,
        HTRS07_tz_KASTELLORIZO]
        )

HTRS07_ROTATION_MATRIX = Matrix(
        [[HTRS07_ds, HTRS07_ez, -HTRS07_ey],
         [-HTRS07_ez, HTRS07_ds, HTRS07_ex],
         [HTRS07_ey, -HTRS07_ex, HTRS07_ds]]
        )


# Some proj4 initialization strings, see:
# http://trac.osgeo.org/proj/wiki/GenParms

# This is the TM07 proj4 init string to transform geocentric or
# ellipsoid coordinates to TM07 plane coordinates for Greece 
# mainland (excluded Kastellorizo).
# Ellipsoid: GGRS80
# Projection Transverse Mercatoric
# k_0=0.9996
# lambda_0 = 24 degrees
# False easting = 500000 meters False northing = -2000000 meters
PROJ4_TM07_INIT_STRING = '+ellps=GRS80 +proj=tmerc +k_0=0.9996 ' \
                         '+lon_0=24 +x_0=500000 +y_0=-2000000'

# This is the TM07 proj4 init string to transform geocentric or
# ellipsoid coordinates to TM07 plane coordinates for the case of the
# area of Kastellorizo. 
# Ellipsoid: GGRS80
# Projection Transverse Mercatoric
# k_0=1
# lambda_0 = 30 degrees
# False easting = 500000 meters False northing = -2000000 meters
PROJ4_TM07_INIT_STRING_KASTELLORIZO = \
                         '+ellps=GRS80 +proj=tmerc +k_0=1 ' \
                         '+lon_0=30 +x_0=500000 +y_0=-2000000'

# This is the TM87 proj4 init string to transform geocentric or
# ellipsoid coordinates to TM87 plane coordinates for the case of the
# area of Kastellorizo. For the rest of Greece TM87 parameters are
# trait equal to GGRS87.
# Ellipsoid: GGRS80
# Projection Transverse Mercatoric
# k_0=0.9996
# lambda_0 = 27 degrees
# False easting = 500000 meters
PROJ4_TM87_INIT_STRING_KASTELLORIZO = \
                         '+ellps=GRS80 +proj=tmerc +k_0=0.9996 ' \
                         '+lon_0=27 +x_0=500000'

# GRS80 ellipsoid geocentric coordinates (X, Y, Z) initialization
# string for proj4
PROJ4_GRS80_GEOCENTRIC_INIT_STRING = '+proj=geocent +ellps=GRS80'

# NOTE: where used in proj: 'init="epsg:2100"', this is the code of
# the GGRS87 system

def htrs07_geocentric_to_ggrs87_geocentric(x, y, z):
    """
    This function transforms htrs07 (X,Y,Z) geocentric coordinates to
    ggrs07 also geocentric coordinates, by applying displacement and
    rotation matrices. Result is a three elements tuple: (X, Y, Z)
    """
    htrs07_coordinates_vector = Vec([x,y,z])
    result_vector= htrs07_coordinates_vector + HTRS07_DISPLACEMENT_VECTOR +\
            HTRS07_ROTATION_MATRIX.mmul(htrs07_coordinates_vector)
    return tuple(result_vector)

def htrs07_geocentric_to_ggrs87_plane(x, y, z, apply_corrections=False):
    """
    This function transforms htrs07 (X, Y, Z) geocentric coordinates
    to plane coordinates in ggrs87. The result is a three items
    tuple: (Easting, Northing, Height)

    By setting apply_corrections to True, then the correction grid is
    applied to the final result.
    """
    # TODO: Implement corrections, set default to True
    if apply_corrections:
        raise NotImplemented(u'Feature is not implemented yet')
    coords = htrs07_geocentric_to_ggrs87_geocentric(x, y, z)
    return transform(Proj(PROJ4_GRS80_GEOCENTRIC_INIT_STRING),
            Proj(init='epsg:2100'), *coords)

def ggrs87_plane_to_ggrs87_geocentric(e, n, h=0):
    """
    Transformation of ggrs87 plane coordinates to ggrs87 geocentric
    coordinates by using the GRS80 Ellipsoid. (e, n, h) stands for
    (Easting, Northing and Height). Result is a three items tuple (X,
    Y, Z) namely the geocentric coordinates.
     Height is optional, if not provided a value of zero
    (0) is considered.
    """
    return transform(Proj(init='epsg:2100'),
            Proj(PROJ4_GRS80_GEOCENTRIC_INIT_STRING), e, n, h)

def ggrs87_geocentric_to_htrs07_geocentric(x, y, z):
    """
    Transformation of ggrs87 geocentric coordinates (X, Y, Z) to
    htrs07 geocentric also coordinates using the displacement
    and rotation matrices. Result is a three items tuple (X, Y, Z)
    """
    ggrs87_coordinates_vector = Vec([x,y,z])
    result_vector= ggrs87_coordinates_vector - HTRS07_DISPLACEMENT_VECTOR -\
            HTRS07_ROTATION_MATRIX.mmul(ggrs87_coordinates_vector)
    return tuple(result_vector)

def htrs07_geocentric_to_htrs07_plane(x, y, z):
    """
    Transformation of htrs07 geocentric coordinates (X, Y, Z) to
    htrs07 plane coordinates using the TM07 projection on the GRS-80
    ellipsoid. Result is a three items tuple (e, n, h) namely
    (Easting, Northing and Height)
    """
    return transform(Proj(PROJ4_GRS80_GEOCENTRIC_INIT_STRING),
            Proj(PROJ4_TM07_INIT_STRING), x, y, z)

def ggrs87_plane_to_htrs07_plane(e, n, h=0, apply_corrections=False):
    """
    Transformation of plane coordinates (e, n, h) or (Easting,
    Northing and Height) in ggrs87 system (TM87 projection on GRS-80
    ellipsoid) to htrs07 system (TM07 projection on GRS-80 ellipsoid).
    Result is a three items tuple (e, n, h) namely (Easting, Northing
    and Height). Height is optional, if not provided a value of zero
    (0) is considered.

    By setting apply_corrections to True, then the correction grid is
    applied to the final result.

    Note: This function is only for use for the Greece mainland, not
    for Kastellorizo area. For Kastellorizo area use:
    ggrs87_plane_to_htrs07_plane_kastellorizo() function instead
    """
    # TODO: Implement corrections, set default to True
    if apply_corrections:
        raise NotImplemented(u'Feature is not implemented yet')
    return htrs07_geocentric_to_htrs07_plane(
            *ggrs87_geocentric_to_htrs07_geocentric(
            *ggrs87_plane_to_ggrs87_geocentric(e, n, h)))

def ggrs87_plane_to_htrs07_plane_kastellorizo(e, n, h=0):
    """
    See also ggrs87_plane_to_htrs07_plane(). This function is for
    special use for the area of Kastellorizo only.
    """
    coords = transform(Proj(PROJ4_TM87_INIT_STRING_KASTELLORIZO),
            Proj(PROJ4_GRS80_GEOCENTRIC_INIT_STRING), e, n, h)
    ggrs87_coordinates_vector = Vec(coords)
    htrs07_coordinates_vector = ggrs87_coordinates_vector - \
            HTRS07_DISPLACEMENT_VECTOR_KASTELLORIZO
    return transform(Proj(PROJ4_GRS80_GEOCENTRIC_INIT_STRING),
            Proj(PROJ4_TM07_INIT_STRING_KASTELLORIZO),
            *htrs07_coordinates_vector)


import sys
sys.path.append("/home/savchenk/work/dda/dda-gencat")
import astropy.io.fits as pyfits

def test_imcat():
    import ddosa
    import gencat

    cat=gencat.CatFotImage()
    cat.catalog=[
        dict(
                NAME="TEST_SOURCE",
                RA=83,
                DEC=22,
             )
    ]
    cat.promote()
    cat.get()

    d=pyfits.open(cat.cat.get_path())[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ']==cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']
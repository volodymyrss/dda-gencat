import sys
import os
sys.path.append("/home/savchenk/work/dda/dda-gencat")
import astropy.io.fits as pyfits

def test_imcat():
    import ddosa
    import gencat

    cat=gencat.SourceCatalog()
    cat.catalog=[
        dict(
                NAME="TEST_SOURCE",
                RA=83,
                DEC=22,
             )
    ]
    cat.promote()

    gcat=gencat.CatForImage().get()

    d=pyfits.open(gcat.cat.get_path())[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ']==cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']


def test_grcat():
    import ddosa
    import gencat

    cat=gencat.SourceCatalog()
    cat.catalog=[
        dict(
                NAME="TEST_SOURCE",
                RA=83,
                DEC=22,
             )
    ]
    cat.promote()

    gcat=gencat.GRcat(use_read_caches=[]).get()

    d=pyfits.open(gcat.cat)[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ']==cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']


def test_igrcat():
    import ddosa
    import gencat

    cat=gencat.SourceCatalog()
    cat.catalog=[
        dict(
                NAME="TEST_SOURCE",
                RA=83,
                DEC=22,
             )
    ]
    cat.promote()

    gcat=gencat.ISGRIRefCat(use_read_caches=[]).get()

    d=pyfits.open(gcat.cat)[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ']==cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']


def test_catforspec():
    import ddosa
    import gencat

    cat=gencat.SourceCatalog()
    cat.catalog=[
        dict(
                NAME="TEST_SOURCE",
                RA=83,
                DEC=22,
             )
    ]
    cat.promote()

    gcat=gencat.CatForSpectra().get()

    d=pyfits.open(gcat.cat.get_path())[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_FIN']==cat.catalog[0]['RA']
    assert d[0]['DEC_FIN'] == cat.catalog[0]['DEC']

def test_catextract_grcat():
    import ddosa
    import gencat

    cat=gencat.SourceCatalog()
    cat.catalog=[
        dict(
                NAME="TEST_SOURCE",
                RA=83,
                DEC=22,
             )
    ]
    cat.promote()

    scw=ddosa.ScWData(input_scwid="066500220010.001")
    scw.get().promote()

    igrcat=gencat.ISGRIRefCat(use_read_caches=[]).get()
    assert os.path.exists(igrcat.cat)
    d = pyfits.open(igrcat.cat)[1].data
    assert len(d) == 1
    assert d[0]['NAME'] == cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ'] == cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']
    assert d[0]['ISGRI_FLAG'] == 1
    assert d[0]['ISGRI_FLAG2'] == 0

    ecat=ddosa.CatExtract(use_read_caches=[]).get()
    assert isinstance(ecat.input_cat,gencat.ISGRIRefCat)

    assert os.path.exists(ecat.input_cat.cat)
    d=pyfits.open(ecat.input_cat.cat)[1].data
    assert len(d) == 1
    assert d[0]['NAME'] == cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ'] == cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']
    assert d[0]['ISGRI_FLAG'] == 1
    assert d[0]['ISGRI_FLAG2'] == 0

    d=pyfits.open(ecat.cat.get_path())[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ']==cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']

    im = ddosa.ii_skyimage(use_read_caches=[]).get()

    d=pyfits.open(im.skyres.get_path())[2].data
    assert len(d['NAME']) >= 1
    assert d[0]['NAME'] == cat.catalog[0]['NAME']
    assert d[0]['RA_OBJ'] == cat.catalog[0]['RA']
    assert d[0]['DEC_OBJ'] == cat.catalog[0]['DEC']




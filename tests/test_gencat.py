import sys
import os
sys.path.append("/home/savchenk/work/dda/dda-gencat")
import astropy.io.fits as pyfits
from dataanalysis import hashtools
import dataanalysis.core as da

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



def test_catforspec_tospec():
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

    ddosa.ScWData(input_scwid="066500220010.001").get().promote()

    gcat=gencat.CatForSpectra().get()
    d=pyfits.open(gcat.cat.get_path())[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_FIN']==cat.catalog[0]['RA']
    assert d[0]['DEC_FIN'] == cat.catalog[0]['DEC']

    spec = ddosa.ii_spectra_extract(input_cat=gencat.CatForSpectra,use_read_caches=[]).get()

    assert hasattr(spec,'spectrum')
    d=pyfits.open(spec.spectrum.get_path())

    print d[1].data

    assert len(d[1].data) == 1+1
    assert len(d[2:])==1+1

    assert d[2].header['NAME']==cat.catalog[0]['NAME']

def test_catforspec_tolc():
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

    ddosa.ScWData(input_scwid="066500220010.001").get().promote()

    gcat=gencat.CatForSpectra().get()
    d=pyfits.open(gcat.cat.get_path())[1].data

    assert len(d)==1
    assert d[0]['NAME']==cat.catalog[0]['NAME']
    assert d[0]['RA_FIN']==cat.catalog[0]['RA']
    assert d[0]['DEC_FIN'] == cat.catalog[0]['DEC']

    lc = ddosa.ii_lc_extract(input_cat=gencat.CatForSpectra,use_read_caches=[]).get()

    assert hasattr(lc,'lightcurve')
    d=pyfits.open(lc.lightcurve.get_path())

    print d[1].data

    assert len(d[1].data) == 1
    assert len(d[2:])==1

    assert d[2].header['NAME']==cat.catalog[0]['NAME']


def test_mosaic_ii_skyimage():
    import ddosa
    import gencat

    cat = gencat.SourceCatalog()
    cat.catalog = [
        dict(
            NAME="TEST_SOURCE",
            RA=83,
            DEC=22,
        )
    ]
    cat.promote()
    assert cat.virtual
    assert hasattr(cat,'catalog')

    grcat=gencat.GRcat()
    grcat.serialize()

    sc=ddosa.da.AnalysisFactory.byname("SourceCatalog")
    assert cat == sc
    print sc.get_version()

    #ips=ddosa.ImageProcessingSummary().get()
    #print "HASH:",ips.hash

    ##

    #da.debug_output()

    mf = gencat.GRcat()
    c=mf.process(output_required=False, run_if_haveto=False)[0]
    print("mf:", c)

    mf = gencat.GRcat(assume=ddosa.ScWData(input_scwid="any"))
    c=mf.process(output_required=False, run_if_haveto=False)[0]
    print("mf:", c)

    assert c[1][2].startswith("SourceCatalog.v0.1.")
    ##

    mosaic=ddosa.mosaic_ii_skyimage(
               assume=[
                  ddosa.ii_skyimage(input_cat=gencat.CatForImage),
                  ddosa.ImageGroups(input_scwlist=ddosa.IDScWList(use_scwid_list=["066500330010.001","066500340010.001"])),
                  ddosa.ImageBins(use_ebins=[(25, 40)], use_version="onebin_25_40"),
                  ddosa.ImagingConfig(use_SouFit=0, use_version="soufit0")
              ]
            )
    mosaic.read_caches=[]
    mosaic.ii_NegModels=1
    mosaic.get()

    d=pyfits.open(mosaic.srclres.get_path())[1].data
    print d['NAME']
    assert len(d) == 2
    assert d[0]['NAME'] == cat.catalog[0]['NAME']
    assert d[0]['RA_FIN'] == cat.catalog[0]['RA']
    assert d[0]['DEC_FIN'] == cat.catalog[0]['DEC']

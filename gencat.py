from __future__ import print_function

import ddosa
import astropy.io.fits as pyfits
import numpy as np
from dataanalysis.hashtools import shhash

import dataanalysis.core as da

class SourceCatalog(ddosa.DataAnalysis):
    #catalog=[]

    autoversion=True


    def get_version(self):
        version=self.get_signature()+"."+self.version
        if self.autoversion and hasattr(self,'catalog'):
            version+=".%i"%len(self.catalog)

            c_v=[]
            for e in sorted(self.catalog,key=lambda x:x['NAME']):
                e_v=[]
                for k,v in sorted(e.items()):
                    if k == "NAME":
                        e_v.append("%s_%s"%(str(k),str(v)))
                    elif isinstance(v,float):
                        e_v.append("%s_%.5lg"%(str(k),v))
                    elif isinstance(v,int):
                        e_v.append("%s_%i"%(str(k),v))
                    else:
                        e_v.append("%s_%s"%(str(k),str(v)))
                c_v.append("_".join(e_v))

            cvs=".".join(c_v)
            version+="."+cvs[:100]+"_"+shhash(cvs)[:8]
        return version

    def main(self):
        print("my catalog:",self.catalog)

class GenCat(ddosa.DataAnalysis):

    input_catalog=SourceCatalog

    output_structure=None

    cached=True

    cat_attribute="cat"
    suffix=""

    def main(self):
        catfn="generated_cat%s.fits"%self.suffix

        ddosa.remove_withtemplate(catfn+"("+self.output_structure+".tpl)")

        dc=ddosa.heatool("dal_create")
        dc['obj_name']=catfn
        dc['template']=self.output_structure+".tpl"
        dc.run()

        cat=pyfits.open(catfn)

        nd=np.zeros(len(self.input_catalog.catalog),dtype=cat[self.output_structure].data.dtype)

        print(self.input_catalog.catalog)

        for i,cat_entry in enumerate(self.input_catalog.catalog):
            self.map_entry_to_fits_record(cat_entry,nd[i])

        cat[self.output_structure].data=nd
        cat.writeto(catfn,clobber=True)

        setattr(self,self.cat_attribute,ddosa.DataFile(catfn))

class GRcat(GenCat):
    version="v2"

    output_structure = "GNRL-REFR-CAT"

    cat_attribute="_cat"
    suffix = "_grcat"

    def map_entry_to_fits_record(self,cat_entry,fits_record):
        fits_record['RA_OBJ']=cat_entry['RA']
        fits_record['DEC_OBJ'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
        fits_record['ISGRI_FLAG'] = cat_entry.get('ISGRI_FLAG',1)
        fits_record['ISGRI_FLAG2'] = cat_entry.get('ISGRI_FLAG', 0)
        fits_record['ISGR_FLUX_1'] = cat_entry.get('ISGRI_FLUX_1', 1000)
        fits_record['ISGR_FLUX_2'] = cat_entry.get('ISGRI_FLUX_2', 1000)

    @property
    def cat(self):
        return self._cat.get_full_path()

class GRcatForJEMX(GenCat):
    output_structure = "GNRL-REFR-CAT"

    cat_attribute="_cat"
    suffix = "_grcat_jemx"
    
    def map_entry_to_fits_record(self,cat_entry,fits_record):
        fits_record['RA_OBJ']=cat_entry['RA']
        fits_record['DEC_OBJ'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
        fits_record['ISGRI_FLAG'] = cat_entry.get('ISGRI_FLAG',1)
        fits_record['ISGRI_FLAG2'] = cat_entry.get('ISGRI_FLAG', 0)
        fits_record['ISGR_FLUX_1'] = cat_entry.get('ISGRI_FLUX_1', 1000)
        fits_record['ISGR_FLUX_2'] = cat_entry.get('ISGRI_FLUX_2', 1000)
        fits_record['FLAG'] = cat_entry.get('FLAG', 0)

    @property
    def cat(self):
        return self._cat

class ExplicitISGRIRefCat(GRcat):
    suffix = "_igrcat"

class CatForImage(GenCat):
    output_structure = "ISGR-SRCL-CAT"
    suffix = "_forimage"

    def map_entry_to_fits_record(self,cat_entry,fits_record):
        fits_record['RA_OBJ']=cat_entry['RA']
        fits_record['DEC_OBJ'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
        fits_record['ISGRI_FLAG'] = cat_entry.get('ISGRI_FLAG',1)


class CatForSpectra(GenCat):
    output_structure = "ISGR-SRCL-RES"
    suffix = "_forspectra"

    version="v1"

    def map_entry_to_fits_record(self, cat_entry, fits_record):
        fits_record['RA_OBJ'] = cat_entry['RA']
        fits_record['DEC_OBJ'] = cat_entry['DEC']
        fits_record['RA_FIN'] = cat_entry['RA']
        fits_record['DEC_FIN'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
        fits_record['ISGRI_FLAG'] = 1

class CatForLC(CatForSpectra):
    suffix = "_forlc"

class ii_spectra_extract(ddosa.ii_spectra_extract):
    input_cat=CatForSpectra

class ii_lc_extract(ddosa.ii_lc_extract):
    input_cat=CatForSpectra

try:

    class UserCat(da.byname('UserCat')):
        input_cat = GRcatForJEMX

    class jemx_spe(da.byname('jemx_spe')):
        input_usercat=UserCat

    class jemx_lcr(da.byname('jemx_lcr')):
        input_usercat=UserCat

except Exception as e:
    print("not loading jemx")
        

import dataanalysis.callback

dataanalysis.callback.default_callback_filter.set_callback_accepted_classes([ii_spectra_extract, ii_lc_extract])


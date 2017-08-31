from __future__ import print_function

import ddosa
import astropy.io.fits as pyfits
import numpy as np
from hashtools import shhash

class SourceCatalog(ddosa.DataAnalysis):
    #catalog=[]

    autoversion=True

    def get_version(self):
        v=self.get_signature()+"."+self.version
        if self.autoversion and hasattr(self,'catalog'):
            v+=".%i.%s"%(len(self.catalog),shhash(repr(self.catalog)))
        return v

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
        return self._cat.get_path()

class ISGRIRefCat(GRcat):
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

    def map_entry_to_fits_record(self, cat_entry, fits_record):
        fits_record['RA_FIN'] = cat_entry['RA']
        fits_record['DEC_FIN'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
from __future__ import print_function

import ddosa
import astropy.io.fits as pyfits
import numpy as np

class SourceCatalog(ddosa.DataAnalysis):
    #catalog=[]

    def main(self):
        print("my catalog:",self.catalog)

class GenCat(ddosa.DataAnalysis):
    input_catalog=SourceCatalog

    output_structure=None

    cached=True

    def main(self):
        catfn="generated_cat.fits"

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

        self.cat = ddosa.DataFile(catfn)


class CatForImage(GenCat):
    output_structure = "ISGR-SRCL-CAT"

    def map_entry_to_fits_record(self,cat_entry,fits_record):
        fits_record['RA_OBJ']=cat_entry['RA']
        fits_record['DEC_OBJ'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
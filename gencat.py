from __future__ import print_function

import ddosa
import astropy.io.fits as pyfits
import numpy as np

class GenCat(ddosa.DataAnalysis):
    output_structure=None

    catalog=[]

    def main(self):
        catfn="generated_cat.fits"

        dc=ddosa.heatool("dal_create")
        dc['obj_name']=catfn
        dc['template']=self.output_structure+".tpl"
        dc.run()

        cat=pyfits.open(catfn)

        nd=np.zeros(len(self.catalog),dtype=cat[self.output_structure].data.dtype)

        print(self.catalog)

        for i,cat_entry in enumerate(self.catalog):
            self.map_entry_to_fits_record(cat_entry,nd[i])

        cat[self.output_structure].data=nd
        cat.writeto(catfn,clobber=True)

        self.cat = ddosa.DataFile(catfn)


class CatFotImage(GenCat):
    output_structure = "ISGR-SRCL-CAT"

    def map_entry_to_fits_record(self,cat_entry,fits_record):
        fits_record['RA_OBJ']=cat_entry['RA']
        fits_record['DEC_OBJ'] = cat_entry['DEC']
        fits_record['NAME'] = cat_entry['NAME']
        fits_record['SOURCE_ID'] = cat_entry['NAME']
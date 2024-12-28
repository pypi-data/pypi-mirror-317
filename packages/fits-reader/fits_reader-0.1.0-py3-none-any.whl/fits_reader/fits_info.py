import astropy.io.fits as fits

class FITSInfo:
    def __init__(self, fits_file) :
        self.fits_file = fits_file
        self.header = None
        self.data = None
        self.read_fits_file()

    def read_fits_file(self) :
        """Read the FITS file and store the header and data in the object."""
        try :
            with fits.open(self.fits_file) as hdul :
                # abstrace the header and data
                self.header = hdul[0].header
                # abstrace the data dimensions and data type
                self.data_shape = hdul[0].data.shape if hdul[0].data is not None else None
                self.data_type = hdul[0].data.dtype if hdul[0].data is not None else None
        except Exception as e:
            print(f"error: cannot read FITS file {self.fits_file}: error message:{e}")

    def get_header_info(self) :
        """return the header information of the FITS file."""
        if self.header:
            return self.header
        else:
            return "No header found in the FITS file."

    def get_data_shape(self) :
        """return the shape of the FITS data."""
        if self.data_shape:
            return self.data_shape
        else:
            return "No data found in the FITS file."

    def get_data_type(self) :
        """return the data type of the FITS data."""
        if self.data_type:
            return self.data_type
        else:
            return "No data found in the FITS file."
    def print_basic_info(self) :
        """print the basic information of the FITS file."""
        print(f"FITS file: {self.fits_file}")
        print(f"Header: {self.get_header_info()}")
        print(f"Data shape: {self.get_data_shape()}")
        print(f"Data type: {self.get_data_type()}")

        # return FITS data shape
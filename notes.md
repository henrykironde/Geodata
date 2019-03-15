# Post-Installation Fixes and Setup

    # Install compilers and linking tools; other tools
    sudo apt-get install g++ swig curl build-essential python-all-dev

    # Install package manager
    sudo apt-get install synaptic

    # Install Unity customization tool
    sudo apt-get install unity-tweak-tool

    # If the hardware brightness controls don't work, use:
    sudo add-apt-repository ppa:indicator-brightness/ppa
    sudo apt-get update && sudo apt-get install indicator-brightness

    # Allows use of easy_install and, later, pip
    sudo apt-get install python-setuptools

    # Allows the installation of some Python packages (e.g. psycopg2) in a virtual environment with pip
    sudo apt-get install libpq-dev python-dev

    # Python IDE
    sudo apt-get install ipython

    # gedit plugins
    sudo apt-get install gedit-plugins gedit-developer-plugins

## Installed Packages

* Apache (v2.2)
* GDAL (v1.9.2)
* GDAL Utilities (GDAL-OGR, v1.9.2)
* GEOS
* Git
* Mercurial
* MongoDB
* Node.js
* pgAdmin3
* PostgreSQL (9.1)
* PostGIS (2.1)
* Proj
* psycopg2
* R
* virtualenv

### GEOS

Upgrading GEOS can break existing Django projects! [Here is the solution](http://stackoverflow.com/questions/18643998/geodjango-eosexception-error).

    # SWIG required to install Python bindings
    sudo apt-get install swig swig2.0

    # It's necessary to compile from source for 13.10
    cd /usr/local/ && sudo mkdir geos && sudo chown arthur geos && cd geos
    wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
    tar -xvf geos-3.4.2.tar.bz2 && rm geos-3.4.2.tar.bz2 && cd geos-3.4.2
    ./configure --enable-python
    make
    sudo make install

### Proj

    # It's necessary to compile from source for 13.10
    cd /usr/local/ && sudo mkdir proj && sudo chown arthur proj && cd proj
    wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz
    tar -xzvf proj-4.8.0.tar.gz && rm proj-4.8.0.tar.gz && cd proj-4.8.0
    ./configure
    make
    sudo make install

### HDF4

    sudo apt-get install libhdf4-0 libhdf4-dev

### HDF5

    # Install MPI compiler for parallel HDF5 installation
    sudo apt-get install libcr-dev mpich2 mpich2-doc

    cd /usr/local/ && sudo mkdir hdf5 && sudo chown arthur hdf5 && cd hdf5
    wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.13.tar.gz
    tar -xzvf hdf5-1.8.13.tar.gz && rm hdf5-1.8.13.tar.gz && cd hdf5-1.8.13

    # For parallel HDF5 support (may not work with GDAL)
    CC=/usr/bin/mpicc ./configure --prefix=/usr/local --enable-shared --enable-hl
    make
    sudo make install

### GDAL and GDAL-OGR

    # To install from packages...
    sudo apt-get install gdal-bin python-gdal

    # Development files and headers for GDAL
    sudo apt-get install libgdal-dev libgdal1-dev

**Installing GDAL in a Virtual Environment**

    # For a virtual environment... (http://tylerickson.blogspot.com/2011/09/installing-gdal-in-python-virtual.html)
    cd /usr/local/pythonenv/my-virutal-environment/
    source bin/activate
    pip install --no-install gdal && cd gdal
    python setup.py build_ext --gdal-config=/usr/bin/gdal-config --libraries=gdal --include-dirs=/usr/include/gdal/
    cd .. && pip install --no-download gdal

**Compiling GDAL from Source**

    # Compile GDAL from source...
    cd /usr/local/ && sudo mkdir gdal && sudo chown arthur gdal && cd gdal
    wget http://download.osgeo.org/gdal/1.11.0/gdal-1.11.0.tar.gz
    tar -xzvf gdal-1.11.0.tar.gz && rm gdal-1.11.0.tar.gz && cd gdal-1.11.0
    ./configure --with-python --with-hdf5=/usr/local/hdf5/hdf5-1.8.13/hdf5
    make
    sudo make install

### PostgreSQL

    # Install from apt-get
    sudo apt-get install postgresql-9.3 postgresql-client-9.3 postgresql-client-common postgresql-common pgadmin3

    # If building PostGIS from source or if missing the pgxs.mk makefile...
    sudo apt-get install postgresql-server-dev-9.3

    # Define superuser(s)
    sudo su -c "createuser arthur --login --inherit --superuser --createdb --createrole --pwprompt" - postgres
    sudo service postgresql restart

    # If using PostgreSQL for Python projects, it is necessary to install...
    sudo apt-get install python-psycopg2

### PostGIS

**PostGIS requires the following libraries:**

* GEOS (libgeos)
* Proj (libproj)
* GDAL (libgdal)

To install PostGIS from source:

    # Install dependencies
    sudo apt-get install libxml2-dev

    cd /usr/local/ && sudo mkdir postgis && sudo chown arthur postgis && cd postgis
    wget http://download.osgeo.org/postgis/source/postgis-2.1.4.tar.gz
    tar -xzvf postgis-2.1.4.tar.gz && rm postgis-2.1.4.tar.gz && cd postgis-2.1.4
    sudo ./configure --with-projdir=/usr/local/proj/proj-4.8.0/
    make
    sudo make install

    # Configure template database
    POSTGIS_TEMPLATE=postgis-2.1.4
    POSTGRESQL_VER=9.3
    sudo su -c "createdb $POSTGIS_TEMPLATE" - postgres
    sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='$POSTGIS_TEMPLATE';"
    sudo -u postgres psql -d $POSTGIS_TEMPLATE -f /usr/share/postgresql/$POSTGRESQL_VER/contrib/postgis-2.1/postgis.sql
    sudo -u postgres psql -d $POSTGIS_TEMPLATE -c "GRANT ALL ON geometry_columns TO PUBLIC;"
    sudo -u postgres psql -d $POSTGIS_TEMPLATE -c "GRANT SELECT ON spatial_ref_sys TO PUBLIC;"

To create a new superuser in PostgreSQL:

    sudo su -c "createuser arthur --login --inherit --superuser --createdb --createrole --pwprompt" - postgres

The `shp2pgsql` and `raster2pgsql` binaries may not be on your path after the install.
To remedy this:

    # Put the loader `shp2pgsql` on your path; likely not done when building from source
    cd /usr/local/postgis/postgis-2.1.4/loader
    make
    sudo make install
    sudo ln -s /usr/local/postgis/postgis-2.1.4/loader/shp2pgsql /usr/local/bin/shp2pgsql

    # Link to the `raster2pgsql` binary
    sudo ln -s /usr/lib/postgresql/9.3/bin/raster2pgsql /usr/bin/raster2pgsql
    sudo ldconfig

### R

    sudo apt-get install r-base

My favorite packages for R include:

```
install.packages(c('plyr', 'reshape2', 'ggplot2', 'knitr', 'sp', 'raster'))
install.packages('rgdal') # Only if GDAL is installed
```

### Apache

    sudo apt-get install apache2 apache2-bin apache2-data apache2-mpm-worker

    # WSGI module
    sudo apt-get install libapache2-mod-wsgi

    # Activate modules that were not activated at installation
    sudo a2enmod proxy proxy_http rewrite

### Git

    sudo apt-get install git

To connect to GitHub, you need to generate SSH keys...

    # Generating SSH keys for GitHub
    mkdir -p ~/.ssh/ && cd ~/.ssh/
    ssh-keygen -t rsa -C "endsley@umich.edu"
    # Hit "Enter" to use defaults

    # Downloads and installs xclip. If you don't have `apt-get`, you might need to use another installer (like `yum`)
    sudo apt-get install xclip

    # Copies the contents of the id_rsa.pub file to your clipboard; add to your account on GitHub.com
    xclip -sel clip < ~/.ssh/id_rsa.pub

    # Setting global configs
    git config --global user.name "K. Arthur Endsley"
    git config --global user.email endsley@umich.edu
    git config --global core.editor nano
    git config --global merge.tool vimdiff
    git config --global github.user arthur-e
    git config --global color.ui true
    git config --global alias.pushall "push --recurse-submodules=on-demand" # Recursively check submodules in a push

    # Converts all Windows CR-LF line endings to Unix LF line endings on commit
    git config --global core.autocrlf input

To configure a repository to have multiple remotes to push to simultaneously:

    git remote rm origin
    git remote add origin [path/to/network/repo]
    git config --add remote.origin.url git@github.com:arthur-e/flux-client.git

### Mercurial

    sudo apt-get install mercurial

### MongoDB

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10

    # Create a /etc/apt/sources.list.d/10gen.list file and include the following line for the 10gen repository.
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list

    sudo apt-get update && sudo apt-get install mongodb-10gen

### Node.js

    sudo mkdir /usr/local/nodejs && sudo chown arthur /usr/local/nodejs && cd /usr/local/nodejs
    wget http://nodejs.org/dist/v0.10.24/node-v0.10.24.tar.gz
    tar -xzvf node-v0.10.24.tar.gz && rm node-v0.10.24.tar.gz && cd node-v0.10.24
    ./configure
    sudo make
    sudo make install

## Python Virtual Environments

    sudo easy_install pip
    sudo pip install virtualenv
    sudo mkdir /usr/local/pythonenv
    sudo chown arthur /usr/local/pythonenv

### Using Django in a Virtual Environment

The latest versions of Django require a particular setup in the `wsgi.py` file.

    import sys, os, site

    ############################
    # Virtual environment setup

    ALLDIRS = [
        '/usr/local/pythonenv/scour-server-env/lib/python2.7/site-packages/',
    ]

    # Remember original sys.path
    prev_sys_path = list(sys.path)

    for directory in ALLDIRS:
        site.addsitedir(directory)

    # Reorder sys.path so new directories are at the front
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)

    sys.path[:0] = new_sys_path

    # End setup
    ############

    # We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
    # if running multiple sites in the same mod_wsgi process. To fix this, use
    # mod_wsgi daemon mode with each site in its own daemon process, or use
    os.environ['DJANGO_SETTINGS_MODULE'] = 'scour_server.settings'
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scour_server.settings')

    # This application object is used by any WSGI server configured to use this
    # file. This includes Django's development server if the WSGI_APPLICATION
    # setting points here.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

## QGIS

Because we built GDAL from source, it is necessary to bypass the automatic installation of the `gdal-bin` package.
The Python bindings should also be bypassed, as GDAL should have been built `--with-python` support.

    sudo apt-get install --no-install-recommends qgis qgis-plugin-grass

If GDAL was **not** built from source and was instead installed as a package, QGIS can also be easily installed as a package:

    # This would install `qgis` from the package manager:
    # sudo apt-get install qgis python-qgis qgis-plugin-grass

### TopoJSON

    # Requires Node.js and NPM
    sudo npm install -g topojson

    # Install the geojson-cli
    sudo npm install -g geojson

### Python Virtual Environments (virtualenv)

    sudo easy_install pip
    sudo pip install virtualenv

### LaTeX

    sudo apt-get install texlive-base texlive-latex-base texlive-extra-utils texlive-math-extra

    # Or...
    sudo apt-get install texlive-full



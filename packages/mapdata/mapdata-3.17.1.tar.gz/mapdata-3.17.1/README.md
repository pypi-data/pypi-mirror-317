
*mapdata.py* is a data explorer for data sets containing geographic coordinates.  Data can be read from a CSV file, spreadsheet, or database.  Both a map and a data
table are displayed.  When a location is selected on the map, the same location is highlighted in the table, and *vice-versa*.  Single or multiple selections may be enabled.  Locations may also be selected and highlighted by writing a query expression to select rows of the data table.  The basemap on which data are displayed is [OpenStreetMap](https://www.openstreetmap.org) by default; other map servers can also be used.

![example map](https://mapdata.readthedocs.io/en/latest/_images/UI_CSOs_1.png)

In addition to visually browsing the map and table, the user can produce a number of different tabular, graphical, and statistical summaries of the data.  Most of these summaries can be applied either to the entire data set or to a selected subset of the data.

Map coordinates should be in decimal degrees, in WGS84 (coordinate reference system [CRS] 4326), however, coordinates in other CRSs can be converted to 4326.

The map display can be customized in several ways:

  * Different raster tile servers may be used for the basemap.  Several alternatives to the default ([OpenStreetMap](https://www.openstreetmap.org)) are built in and can be selected from a drop-down list.  Other tile servers can be specified in a configuration file.

  * Locations identified by coordinates in the data file may be designated by
    different types of markers and by different colors.  The default marker for
    locations, and the default marker used to flag selected locations can both be
    customized.  Symbols and colors to use for location markers can be specified
	in a configuration file and in the data file.  Different symbols and markers
	can be used for different selected locations.

  * Locations may be unlabeled or labeled with data values from the data file
    The label font, size, color, and location can all be customized.

  * When there is more than one data value (table row) at a location, the number
    of rows can be annotated on the map adjacent to each location.  In addition,
    data can be selected based on the number of data rows with the same
    geographic  coordinates.

The map can be exported to a Postscript, PNG, or JPEG file.  Using command-line options, *mapdata* can be directed to load a data file and display location markers and then to export the map to an image file, and quit.

Selected rows in the data table can be exported to a CSV or spreadsheet file.

## Data Plots

Data can be displayed in several different types of plots: box plots, scatter
plots, line charts, kernel density plots, ECDF plots, Q-Q plots, strip charts, 
counts of categorical and quantitative variables, and others.  Plots
can use either all data or only data values that are selected in the map and
table.  Plots have a live connection to the data table and map, so when data selections are changed the plots are automatically updated.

![example plot](https://mapdata.readthedocs.io/en/latest/_images/UI_cat_stripchart.png)

## Statistics

*Mapdata* can also carry out some univariate, bivariate, and multivariate statistical
summarizations and analyses.  Statistical analyses can use either all data in the data table
or only the data that are highlighted on the map.  These summaries are updated immediately if different data are selected.

![Bivariate statistics](https://mapdata.readthedocs.io/en/latest/_images/Bivariate_dialog.png)

Statistical summaries and analyses include:

  * Bivariate ordinary least squares regression and trend evaluation.

  * A correlation matrix.
 
  * A matrix of pairwise cosine similarity values.

  * Parametric and nonparametric analysis of variance (ANOVA).

  * A contingency table, using either categorical or numeric variables, with flexible specification of groups.  Tests of independence, risk ratio, odds ratio and related statistics, and conditional probabilities are all shown.

  * A Receiver Operating Characteristics (ROC) curve and measures such as sensitivity and specificity for a selected value of the predictor variable.

  * A Principal Component Analysis (PCA).

  * A scatter plot of the results of a Uniform Manifold Approximation and Projection (UMAP) analysis of multiple variables.

  * Composition and contribution matrices produced by non-negative matrix factorization (unmixing).

  * A matrix of pairwise categorical similarity values.

![Correlation matrix](https://mapdata.readthedocs.io/en/latest/_images/UI_corr_matrix_example.png)

## Data Management

SQL commands can be used when importing data from a database.  The SQL
commands can be augmented with [execsql](https://pypi.org/project/execsql/)
metacommands and substitution variables.

*Mapdata* also includes data management tools to support evaluation of data values and relationships between variables.  These features allow:

  * Finding all unique values for one or more columns.

  * Finding data rows with identical values in one or more columns (e.g., duplicated data).

  * Evaluating the cardinality of relationships between key and attribute columns.

## Documentation and Extras

Complete documentation is at [https://mapdata.readthedocs.io/en/latest](https://mapdata.readthedocs.io/en/latest).

A configuration file template and additional bitmap symbols are included with the distribution of *mapdata.py*.


## Dependencies

*Mapdata.py* uses the following third-party Python libraries:

  * [jenkspy](https://pypi.org/project/jenkspy/)

  * [loess](https://pypi.org/project/loess/)

  * [numpy](https://pypi.org/project/numpy/)

  * [matplotlib](https://pypi.org/project/matplotlib/)

  * [odfpy](https://pypi.org/project/odfpy/)
 
  * [openpyxl](https://pypi.org/project/openpyxl/)

  * [pillow](https://pypi.org/project/pillow/)
 
  * [pymannkendall](https://pypi.org/project/pymannkendall/)

  * [pynndescent](https://pypi.org/project/pynndescent/)
 
  * [pyproj](https://pypi.org/project/pyproj/)
 
  * [scikit-learn](https://pypi.org/project/scikit-learn/)

  * [scipy](https://pypi.org/project/SciPy/)

  * [seaborn](https://pypi.org/project/seaborn/)

  * [statsmodels](https://pypi.org/project/statsmodels/)

  * [tkintermapview](https://pypi.org/project/tkintermapview/)

  * [umap-learn](https://pypi.org/project/umap-learn/)

  * [xlrd](https://pypi.org/project/xlrd/)

If *mapdata.py* is used to query a database to obtain a data set to view and
explore, then one or more of the following Python libraries will have to be
installed manually, depending on the type of DBMS used:

   * PostgreSQL: [psycopg2](https://pypi.org/project/psycopg2/)

   * MariaDB and MySQL: [pymysql](https://pypi.org/project/pymysql/)

   * DuckDB: [duckdb](https://pypi.org/project/duckdb/)

   * SQL Server: [pydobc](https://pypi.org/project/pyodbc/)

   * Oracle: [cx-Oracle](https://pypi.org/project/cx-Oracle/)

   * Firebird: [fdb](https://pypi.org/project/fdb/)


[![Downloads](https://pepy.tech/badge/mapdata)](https://pypi.org/project/mapdata/)  

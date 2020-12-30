# Installation
Use `pip install flatten-nosql` to install the package. You will need `pandas` installed on your machine since this library depends on it.

# NoSQL to SQL conversion

Check `driver-flattening` notebook inside `flattener` directory for an example usage.

## Warning
 * If your data has nested arrays inside nested arrays, make sure you specify depth. By default, the module will go as deep as possible. 
 * In some cases, memory requirement may be extremely high due to the nature of flattening. Note that, when we flatten a certain denormalized data, it can have a lot of redundant data in it. Specially, if you did not normalize and denormalize your database design before development. A database that was never normalized and denormalized is not the same as a default denormalized database. Even if you use NoSQL as your preferred data storing format, you should always normalize your database like you would in a SQL database and then denormalize again if necessary. Otherwise, if you attempt flattening the complete data, it is possible that you will face memory issues. Flattening process can be insanely memory hungry if database was not properly designed.
 * The definition of `depth` in this package is based on whether a certain field has an array of dictionary or not. Check the example in the driver notebook. 

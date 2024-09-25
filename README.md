Los requisitos para utilizar el programa son:
- math 
- functools
- itertools
- sys


El compresor funciona de la siguiente manera:
- Para comprimir o descomprimir un archivo hay que poner el siguiente comando:
    - python3 cod_ar.cdi "path + nombre de un fichero"

El comando sirve tanto para comprimir como descomprimir, solo hay que indicar la dirección del fichero 
y su nombre. 

Cabe destacar que el fichero generado se guarda en el mismo path del fichero que se va a comprimir/descomprimir.
Para hacer que se guarde el fichero en el mismo directorio que está el compresor, se ha creado un path 
específico, se aplica de la siguiente manera:
- python3 cod_ar.cdi -h "path + nombre de un fichero"

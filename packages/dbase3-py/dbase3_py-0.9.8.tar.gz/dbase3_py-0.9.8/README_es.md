# Biblioteca Python para DBase III

Este proyecto proporciona una biblioteca de Python para manipular archivos de bases de datos DBase III. Permite leer, escribir, agregar y actualizar registros en la base de datos.

## Características

- Leer archivos de bases de datos DBase III
- Escribir en archivos de bases de datos DBase III
- Agregar nuevos registros
- Actualizar registros existentes
- Filtrar y buscar registros

## Instalación

Para instalar la biblioteca, clona este repositorio y navega al directorio del proyecto:

```bash
git clone https://github.com/yourusername/dbase-iii-python.git
cd dbase-iii-pythonfrom dbase3_py import DBase3
```

## Uso

### Abrir un archivo de base de datos existente
db = DBase3('path/to/database.dbf')

### Agregar un nuevo registro
db.add_record({
    'Name': 'John Doe',
    'Age': 30,
    'Birth': '1990-01-01'
})

### Actualizar un registro existente
db.update_record(0, {
    'Name': 'Jane Doe',
    'Age': 25
})

### Imprimir todos los registros
for record in db:
    print(record)

## Documentación

### Clases

#### `DBase3`

Clase para manipular archivos de bases de datos DBase III.

- `__init__(self, filename: str)`: Inicializa una instancia de DBase3.
- `__del__(self)`: Cierra el archivo de base de datos cuando se destruye la instancia.
- `init(self)`: Inicializa la estructura de la base de datos leyendo el encabezado y los campos.
- `add_record(self, record_data: dict)`: Agrega un nuevo registro a la base de datos.
- `update_record(self, index: int, record_data: dict)`: Actualiza un registro existente en la base de datos.
- `istartswith(f: str, v: str) -> bool`: Verifica si la cadena `f` comienza con la cadena `v`, ignorando mayúsculas y minúsculas.
- `iendswith(f: str, v: str) -> bool`: Verifica si la cadena `f` termina con la cadena `v`, ignorando mayúsculas y minúsculas.
- `create(cls, filename: str, fields: List[Tuple[str, FieldType, int, int]])`: Crea un nuevo archivo de base de datos DBase III con los campos especificados.

### Métodos

- `save_record(self, key, record)`: Escribe un registro (diccionario con nombres de campos y valores de campos) en la base de datos en el índice especificado.
- `__len__(self)`: Devuelve el número de registros en la base de datos, incluidos los registros marcados para ser eliminados.
- `__getitem__(self, key)`: Devuelve un solo registro o una lista de registros de la base de datos.
- `__iter__(self)`: Devuelve un iterador sobre los registros en la base de datos.
- `__str__(self)`: Devuelve una representación en cadena de la base de datos.

## Contribuir

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto

Para cualquier pregunta o sugerencia, por favor contacta a [Domingo E. Savoretti](mailto:esavoretti@gmail.com).




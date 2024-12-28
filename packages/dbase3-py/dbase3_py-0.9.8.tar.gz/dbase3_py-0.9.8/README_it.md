
# Libreria Python per DBase III

Questo progetto fornisce una libreria Python per manipolare i file di database DBase III. Consente di leggere, scrivere, aggiungere e aggiornare i record nel database.

## Caratteristiche

- Leggere i file di database DBase III
- Scrivere nei file di database DBase III
- Aggiungere nuovi record
- Aggiornare i record esistenti
- Filtrare e cercare i record

## Installazione

Per installare la libreria, clona questo repository e naviga nella directory del progetto:

```bash
git clone https://github.com/yourusername/dbase-iii-python.git
cd dbase-iii-python
```

## Utilizzo

Ecco un esempio di come utilizzare la libreria:

```python
from dbase3_py import DBase3

# Aprire un file di database esistente
db = DBase3('path/to/database.dbf')

# Aggiungere un nuovo record
db.add_record({
    'Name': 'John Doe',
    'Age': 30,
    'Birth': '1990-01-01'
})

# Aggiornare un record esistente
db.update_record(0, {
    'Name': 'Jane Doe',
    'Age': 25
})

# Stampare tutti i record
for record in db:
    print(record)
```

## Documentazione

### Classi

#### `DBase3`

Classe per manipolare i file di database DBase III.

- `__init__(self, filename: str)`: Inizializza un'istanza di DBase3.
- `__del__(self)`: Chiude il file di database quando l'istanza viene distrutta.
- `init(self)`: Inizializza la struttura del database leggendo l'intestazione e i campi.
- `add_record(self, record_data: dict)`: Aggiunge un nuovo record al database.
- `update_record(self, index: int, record_data: dict)`: Aggiorna un record esistente nel database.
- `istartswith(f: str, v: str) -> bool`: Verifica se la stringa `f` inizia con la stringa `v`, ignorando maiuscole e minuscole.
- `iendswith(f: str, v: str) -> bool`: Verifica se la stringa `f` termina con la stringa `v`, ignorando maiuscole e minuscole.
- `create(cls, filename: str, fields: List[Tuple[str, FieldType, int, int]])`: Crea un nuovo file di database DBase III con i campi specificati.

### Metodi

- `save_record(self, key, record)`: Scrive un record (dizionario con nomi di campi e valori di campi) nel database all'indice specificato.
- `__len__(self)`: Restituisce il numero di record nel database, inclusi i record contrassegnati per l'eliminazione.
- `__getitem__(self, key)`: Restituisce un singolo record o un elenco di record dal database.
- `__iter__(self)`: Restituisce un iteratore sui record nel database.
- `__str__(self)`: Restituisce una rappresentazione in stringa del database.

## Contribuire

Le contribuzioni sono benvenute! Si prega di aprire un issue o inviare un pull request.

## Licenza

Questo progetto è concesso in licenza sotto la Licenza MIT. Vedi il file LICENSE per i dettagli.

## Contatto

Per qualsiasi domanda o suggerimento, si prega di contattare [Domingo E. Savoretti](mailto:esavoretti@gmail.com).
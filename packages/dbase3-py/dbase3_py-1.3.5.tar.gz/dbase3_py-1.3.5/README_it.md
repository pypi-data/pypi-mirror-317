# Libreria Python DBase III

Libreria Python pensata per manipolare i file di database DBase III. Consente di leggere, scrivere, aggiungere e aggiornare i record nel database.

Sebbene questo formato di file per database non sia più in uso, il presente lavoro è un minitool utile per recuperare dati legacy, oltre che un omaggio a una bella parte della storia dei computer.

## Caratteristiche

- Leggi file di database DBase III
- Scrivi su file di database DBase III
- Aggiungi nuovi record
- Aggiorna record esistenti
- Filtra e cerca record

## Installazione

Per installare la libreria, clonare questo repository e andare alla directory del progetto:

```bash
git clone https://github.com/sandy98/dbase3-py.git
cd dbase3-py
```

oppure

```bash 
pip install dbase3-py
```

## Utilizzo

### Classe principale

```python
from dbase3_py.dbase3 import DBaseFile, FieldType
test = DbaseFile.create('db/test.dbf',
                    [('name', FieldType.CHARACTER.value, 50, 0),
                        ('age', FieldType.NUMERIC.value, 3, 0)])
test.add_record('John Doe', 30)
test.add_record('Jane Doe', 25)

print(test)
print(len(test))
print(test[:])
print(test.filter('name', 'ja', comp_func=self.istartswith))

```

### Utilità di navigazione del database

```bash
python3 dbfview.py <dbf_file>
```
Una comoda utilità basata su CLI curses per esplorare i file .dbf.

Il modulo stesso, la classe DBaseFile e tutti i suoi metodi sono ampiamente documentati, quindi dovrebbe essere facile da seguire.

In sostanza, ogni istanza di DBaseFile, sia essa istanziata tramite un file DBase III esistente, o creata tramite il metodo factory DBaseFile.create(filename), è un oggetto simile a un elenco con capacità di indicizzazione, che funge anche da iteratore attraverso i record presenti nel file .dbf. Supporta anche il metodo 'len', che segnala il numero di record presenti nel database, anche quelli contrassegnati per l'eliminazione.
Oltre a ciò, c'è un gruppo di metodi pensati per la manipolazione dei dati (add_record per gli inserimenti, update_record per gli aggiornamenti e del_record per contrassegnare/deselezionare le eliminazioni).
C'è anche un gruppo di metodi (search, index, find, filter) per aiutare a recuperare i dati selezionati.

Nella fase attuale di sviluppo, non c'è supporto per i campi memo o indice, anche se questo è pianificato per le versioni future, qualora dovesse sorgere abbastanza interesse. È anche pianificato un metodo `exec` per eseguire istruzioni di tipo SQL. Non funzionante al momento.

Per ulteriori informazioni, vedere la documentazione di seguito.

## Documentazione

### Classi

#### `DBaseFile`

Classe per manipolare i file di database DBase III.

### Metodi 'dunder' e 'privati'

- `__init__(self, filename: str)`: Inizializza un'istanza di DBase3File da un file dbf esistente.
- `__del__(self)`: Chiude il file del database quando l'istanza viene distrutta.
- `__len__(self)`: Recupera il numero di record nel database, inclusi i record contrassegnati per essere eliminati. Consente la scrittura: `len(dbasefileobj)`
- `__getitem__(self, key)`: Recupera un singolo record o un elenco di record (se si usa la notazione slice) dal database. Consente: `dbasefileobj[3]` or `dbasefileobj[3:7]`  
- `__iter__(self)`: Recupera un iteratore sui record nel database. Consente `for record in dbasefileobj: ...`
- `__str__(self)`:  Recupera una rappresentazione testuale del database.
- `_init(self)`: Iinizializza la struttura del database leggendo l'intestazione e i campi. Pensato per uso privato da parte di istanze DBaseFile.
- `def _test_key(self, key)`: Verifica se la chiave è compresa nell'intervallo valido degli indici dei record. Genera un IndexError se la chiave è fuori dall'intervallo. Pensato solo per uso interno.
    
### Metodi di classe.

- `create(cls, filename: str, fields: List[Tuple[str, FieldType, int, int]])`: Crea un nuovo file di database DBase III con i campi specificati. Recupera un oggetto DbaseFile che punta al file dbase appena creato.

### Metodi di manipolazione dei dati

- `add_record(self, record_data: dict)`: Aggiunge un nuovo record al database.
- `update_record(self, index: int, record_data: dict)`: Aggiorna un record esistente nel database.
- `save_record(self, key, record)`: Scrive un record (dizionario con nomi di campo e valori di campo) nel database all'indice specificato. Parametri: la chiave è l'indice (posizione basata su 0 nel file dbf). record è un dizionario corrispondente a un elemento nel database(i.e: {'id': 1, 'name': "Jane Doe"}) Utilizzato internamente da `update_record` 
- `del_record(self, key, value = True)`: Contrassegna per l'eliminazione il record identificato dall'indice 'key', o lo deseleziona se `value == False`. Per cancellare efficacemente il record dal disco, l'eliminazione deve essere confermata tramite `dbasefileobj.write()`
- `write(self, filename=None)`: Scrive il file corrente sul disco, saltando i record contrassegnati per l'eliminazione. Se viene fornito un nome file, diverso dal nome file corrente, salva il file del database nella nuova destinazione, mantenendo il nome file precedente così com'è.

### Metodi di ricerca/filtraggio dei dati

-  `search(self, fieldname, value, start=0, funcname="", comp_func=None)`: Cerca un record con il valore specificato nel campo specificato, a partire dall'indice specificato, per il quale la funzione di confronto specificata Recupera True. Recupera una tupla con indice:int e record:dict
-  `find(self, fieldname, value, start=0, comp_func=None)`: Wrapper per search() con funcname="find". Recupera il primo record (dizionario) trovato oppure None se non viene trovato alcun record che soddisfi i criteri specificati.
-  `index(self, fieldname, value, start=0, comp_func=None)`:  Wrapper per search() con funcname="index". Recupera l'indice del primo record trovato, oppure -1 se non viene trovato alcun record che soddisfi i criteri specificati.
-  `filter(self, fieldname, value, comp_func=None)`:  Recupera un elenco di record (dizionari) che soddisfano i criteri specificati.
- `exec(self, sql_cmd:str)`: Pensato per recuperare dati in modo personalizzato. Non ancora operativo. L'invocazione genera un errore NotImplemented.

### Metodi di elencazione dei dati

-  `list(self, start=0, stop=None, fieldsep="|", recordsep='\n', records:list=None)`:  Recupera un elenco di record dal database, iniziando da 'start', terminando a 'stop' o EOF, con campi separati da 'fieldsep' e record separati da '\n'. Se 'records' non è None, l'elenco fornito viene utilizzato invece del recupero dei valori dal database.
-  `csv(self, start=0, stop=None, records:list = None)`: Wrapper per 'list', utilizzando ',' come separatore campi.
-  `table(self, start=0, stop=None, records:list = None)`: Recupera i record selezionati utilizzando il formato ad hoc, lo stesso fornito da sqlite3 CLI in modalità .table.

### Metodi statici (funzioni ausiliarie per la ricerca/filtraggio)

- `istartswith(f: str, v: str) -> bool`: Controlla se la stringa `f` inizia con la stringa `v`, ignorando la distinzione tra maiuscole e minuscole.
- `iendswith(f: str, v: str) -> bool`: Controlla se la stringa `f` termina con la stringa `v`, ignorando la distinzione tra maiuscole e minuscole.

## Contributi

I contributi sono benvenuti! Si prega di aprire un issue o inviare una richiesta di pull.

## Licenza

Questo progetto è concesso in licenza con la licenza MIT. Per i dettagli, vedere il file LICENSE.

## Contatto

Per qualsiasi domanda o suggerimento, contattare [Domingo E. Savoretti](mailto:esavoretti@gmail.com).



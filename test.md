
## Hosts
### Añadir host
```bash
host add 172.23.184.138 alumno alumnonodo2
```
```bash
host add localhost alumno alumnonodo1
```


### Listar hsots
```bash
host ls
```
```bash
host ls addr = 'localhost'
```

## Users
### Añadir usuario
```bash
user add a a
```
```bash
user add b b
```
```bash
user add c c
```

### Modificar usuario
```bash
user add a c
```

### Listar usuarios
```bash
user ls email = 'a'
```

## Images
### Añadir imagen
```bash
image add https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2 devian12 devian
```

### Compartir imagen
```bash
image share 24a88a4f-3070-4061-8487-9af6ad99c7f8 b 
```

### Ver lista de permisos sobre la imagen
```bash
image shares 24a88a4f-3070-4061-8487-9af6ad99c7f8
```

### Quitar compartido
```bash
image unshare 24a88a4f-3070-4061-8487-9af6ad99c7f8 b36e3a2c-c03a-43bb-8682-20c9524000ba
```
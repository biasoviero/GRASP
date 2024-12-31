# Execução do Script com Julia


O script requer os seguintes parâmetros para execução:
- `<file_path>`: Caminho do arquivo que contém a instância.
- `<seed> `: Valor da *seed*.
- `<timeout>`:  Tempo máximo de execução (em segundos).


## Como Executar

Para executar o script, utilize o seguinte formato no terminal:  
```bash
julia form_inteira.jl <file_path> <seed> <timeout>
`````

#### Exemplo 1
```bash
julia form_inteira.jl 04.txt 10 5
`````

#### Exemplo 2
```bash
julia form_inteira.jl inf05010_2024-2_B_TP_instances_organizacao-de-eventos\03.txt 5 300
`````

### Requisitos

Certifique-se de ter os seguintes requisitos instalados:

- [Julia](https://julialang.org/downloads/)

Caso Julia esteja instalada mas o JuMP/HiGHS não estejam instalados, execute a
seguinte linha no terminal Julia: 
```bash
import Pkg; Pkg.add("JuMP"); Pkg.add("HiGHS")
````



## Execução do Script

O script requer os seguintes parâmetros para execução:
- `--alpha`: Valor de alpha.
- `--seed`: Valor da *seed*.
- `--max-iterations`: Número máximo de iterações.
- `--max-time`: Tempo máximo de execução (em segundos).
- `--filepath`: Caminho do arquivo que contém a instância.

### Exemplos de Uso

#### Exemplo 1
```bash
python3 grasp.py --filepath inf05010_2024-2_B_TP_instances_organizacao-de-eventos\03.txt --seed 7 --max-iterations 10 --alpha 0.05 --max-time 300
`````

#### Exemplo 2
```bash
python3 grasp.py -f inf05010_2024-2_B_TP_instances_organizacao-de-eventos\03.txt -s 7 -m 10 -a 0.05 -t 300
```


### Requisitos

Certifique-se de ter os seguintes requisitos instalados:

- [Python versão 3](https://www.python.org/downloads/)

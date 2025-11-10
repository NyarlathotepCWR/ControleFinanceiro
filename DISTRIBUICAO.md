# GUIA DE DISTRIBUIÇÃO

## Para Usuários Finais (Sem Python)

### Criar Executável Windows

1. Instale PyInstaller:
```
pip install pyinstaller
```

2. Execute o script de build:
```
build.bat
```

3. O executável estará em: `dist\ControleFinanceiro.exe`

4. Distribua apenas o arquivo `.exe` - funciona sem Python instalado

### Testar o Executável

```
cd dist
ControleFinanceiro.exe
```

## Para Desenvolvedores

### Instalação Rápida

**Windows:**
```
install.bat
run.bat
```

**Linux/Mac:**
```
chmod +x install.sh run.sh
./install.sh
./run.sh
```

## Estrutura de Distribuição

```
Gastos/
├── ControleFinanceiro.exe    (Executável standalone - Windows)
├── install.bat                (Instalador Windows)
├── install.sh                 (Instalador Linux/Mac)
├── run.bat                    (Executor Windows)
├── run.sh                     (Executor Linux/Mac)
├── build.bat                  (Criador de executável)
└── README.md                  (Documentação)
```

## Pacote de Distribuição Mínimo

Para distribuir apenas o necessário:

1. **Executável (Windows):**
   - `ControleFinanceiro.exe` (único arquivo necessário)

2. **Código Fonte:**
   - Todo o conteúdo do diretório
   - `install.bat` / `install.sh`
   - `run.bat` / `run.sh`
   - `requirements.txt`

## Notas Importantes

- O executável é **standalone** - não precisa de Python
- O banco de dados `financial_data.db` é criado automaticamente
- Dados ficam na mesma pasta do executável
- Para backup: copie o arquivo `financial_data.db`

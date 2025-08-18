from pathlib import Path

root_path = Path(__file__).resolve().parent.parent

ARQUIVOCONFIG = root_path / "configs" / "config.properties"
ARQUIVOSAVE = root_path / "saves" / "save.properties"


def lerPropriedadesConfig():
    propriedades = {}
    with open(ARQUIVOCONFIG, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha and "=" in linha:
                chave, valor = linha.split("=", 1)
                propriedades[chave] = valor
    return propriedades

# Atualiza ou adiciona uma propriedade e salva no arquivo
def setConfig(chave, valor):
    props = lerPropriedadesConfig()
    props[chave] = valor
    with open(ARQUIVOCONFIG, "w") as arquivo:
        for k, v in props.items():
            arquivo.write(f"{k}={v}\n")
    return ('Registro no arquivo: '+ chave + " Valor: " + getConfig(chave))

# pegar uma propriedade específica
def getConfig(chave, default='1.0'):
    props = lerPropriedadesConfig()
    return props.get(chave, default)








## DAQUI PRA BAIXO -- >  SAVE ##








def lerPropriedadesSave():
    propriedades = {}
    with open(ARQUIVOSAVE, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha and "=" in linha:
                chave, valor = linha.split("=", 1)
                propriedades[chave] = valor
    return propriedades



def setSave(chave, valor):
    props = lerPropriedadesSave()
    props[chave] = valor
    with open(ARQUIVOSAVE, "w") as arquivo:
        for k, v in props.items():
            arquivo.write(f"{k}={v}\n")
    return ('Registro no arquivo: '+ chave + " Valor: " + getSave(chave))

# pegar uma propriedade específica
def getSave(chave, default='1.0'):
    props = lerPropriedadesSave()
    return props.get(chave, default)
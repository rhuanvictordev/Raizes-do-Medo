ARQUIVO = "config.properties"

def lerPropriedades():
    propriedades = {}
    with open(ARQUIVO, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha and "=" in linha:
                chave, valor = linha.split("=", 1)
                propriedades[chave] = valor
    return propriedades

# Atualiza ou adiciona uma propriedade e salva no arquivo
def set(chave, valor):
    props = lerPropriedades()
    props[chave] = valor
    with open(ARQUIVO, "w") as arquivo:
        for k, v in props.items():
            arquivo.write(f"{k}={v}\n")
    return ('Registro no arquivo: '+ chave + " Valor: " + get(chave))

# pegar uma propriedade específica
def get(chave):
    props = lerPropriedades()
    return props.get(chave)
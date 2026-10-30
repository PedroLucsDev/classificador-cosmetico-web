import os
import sqlite3
import json

DB_PATH = os.path.join("data", "catalogo.sqlite3")

def obter_conexao():
    """Cria e devolve uma ligação à base de dados SQLite."""
    conex = sqlite3.connect(DB_PATH)
    # Permite aceder aos campos por nome de coluna (como dicionários)
    conex.row_factory = sqlite3.Row
    return conex

def inicializar_banco():
    """Cria a tabela de produtos e o índice caso não existam."""
    os.makedirs("data", exist_ok=True)
    
    schema_sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        marca TEXT NOT NULL DEFAULT 'Desconhecida',
        descricao TEXT NOT NULL,
        categoria TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos (categoria);
    """

    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.executescript(schema_sql)
        conexao.commit()
    
    print("Base de dados e tabela 'produtos' inicializadas com sucesso.")    

def carregar_dados_iniciais():
    """Lê o ficheiro data/cosmeticos.json e popula a tabela no SQLite."""
    caminho_json = os.path.join("data", "cosmeticos.json")

    if not os.path.exists(caminho_json):
        print(f"Ficheiro {caminho_json} não encontrado. Execute o scraper primeiro.")
        return

    with open(caminho_json, "r", encoding="utf-8") as f:
        produtos = json.load(f)
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM produtos;")
        total_existentes = cursor.fetchone()[0]

        if total_existentes > 0:
            print(f"A tabela já possui {total_existentes} produtos. Inserção ignorada.")
            return
    
        comando_insert = """
        INSERT INTO produtos (nome, marca, descricao, categoria)
        VALUES (?, ?, ?, ?);
        """

        dados_para_inserir = [
            (
                p.get("nome", "").strip(),
                p.get("marca", "Desconhecida").strip(),
                p.get("descricao", "").strip(),
                p.get("categoria", "").strip()
            )
            for p in produtos
        ]

        cursor.executemany(comando_insert, dados_para_inserir)
        conexao.commit()
        print(f"{len(dados_para_inserir)} produtos migrados com sucesso para o SQLite.")

if __name__ == "__main__":
    inicializar_banco()
    carregar_dados_iniciais()
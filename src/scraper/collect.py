import os
import json
import time
import requests

def recolher_cosmeticos(lim_por_categoria: int = 40):
    """
    Recolhe produtos cosméticos reais por categoria a partir da API da Open Beauty Facts.    
    """
    categorias_alvo = {
        "hair" : "Cabelo", 
        "skin": "Pele", 
        "perfumes" : "Perfumes"
    }

    headers = {
        "User-Agent": "CosmeticClassifierStudentProject/1.0 (pedrolbritodev@gmail.com)"    
    }

    prod_coletados = []

    for categorias_api, categoria_rotulo, in categorias_alvo.items():
        print(f"A recolher dados para categoria: {categoria_rotulo}...")
        url = (
            f"https://world.openbeautyfacts.org/category/{categoria_api}.json"
            f"?page_size={lim_por_categoria}&fields=product_name,brands,ingredients_text,categories"
        )

        try:
            resp = requests.request.get(url, headers = headers, timeout = 15)
            if resp.status_code != 200:
                print(f"Erro ao aceder à categoria {categoria_rotulo}: Status {resp.status_code}")
                continue
            dados = resp.json()
            produtos = dados.get("products", [])

            for item in produtos:
                nome = item.get("product_name")
                marca = item.get("brands", "Marca desconhecida")
                ingredientes = item.get("ingredients_text")
                cat_texto = item.get("categoria", "")

                #Ignora produtos sem nome ou sem texto descritivo.
                if not nome:
                    continue

                #Cria uma descrição elaborada juntando ingredientes e categorias técnicas.
                desc_completa = f"{ingredientes or ''} {cat_texto}".strip
                if not desc_completa:
                    desc_completa = f"Produto para cuidados de {categoria_rotulo.lower()}"

                produtos_coletados.append({
                    "nome": nome.strip(),
                    "marca": marca.strip(",")[0].strip() if marca else "Desconhecida",
                    "descricao": desc_completa,
                    "categoria": categoria_rotulo
                })

            print(f"Total de produtos acumulados: {len(prod_coletados)}")
            time.sleep(1)

        except Exception as erro:
            print(f"Falha na recolha de {categoria_rotulo}: {erro}")

        if prod_coletados:
            os.makedirs("data", exist_ok=True)
            cam_saida = os.path.join("data", "cosmeticos.json")
            with open (cam_saida, "w", encoding="utf-8") as f:
                json.dump(prod_coletados, f, ensure_ascii=False, ident=2)
            print(f"\nColeta concluida! Ficheiro gravado em {cam_saida}")
        else:
            print(f"\nNenhum produto foi coletado. Verifique a ligação com a internet")

if __name__ == "__main__":
    recolher_cosmeticos(lim_por_categoria=50)
            
                

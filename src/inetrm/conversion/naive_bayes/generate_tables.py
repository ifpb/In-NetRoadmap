import os

def write_feature_class_rule(writer, feature_idx: int, class_id: int, start: int, end: int, prob: int):
    """
    Escreve a regra para a tabela de uma feature específica em relação a uma classe.
    Exemplo de saída: table_add feature1_class0_exact set_prob_f1_c0 0->1024 => 45 0
    """
    table_name = f"feature{feature_idx}_class{class_id}_exact"
    action_name = f"set_prob_f{feature_idx}_c{class_id}"
    
    # Adicionamos o '0' no final por padrão para respeitar a sintaxe do BMv2 simples
    command = f"table_add {table_name} {action_name} {start}->{end} => {prob} 0\n"
    writer.write(command)


def generate_tables(extracted_data: dict, output_path: str) -> None:
    """
    Recebe os dados extraídos pelo read_naive_bayes.py e gera o arquivo table.txt
    contendo as regras de match-action do switch P4.
    """
    classes = extracted_data["classes"]
    features = extracted_data["features"]
    rules = extracted_data["rules"]

    # Garante que o diretório de saída exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        # 1. Gerar tabelas de probabilidade por Feature e por Classe
        for idx_feature, feature in enumerate(features, 1):
            for class_id in classes:
                # Recupera a lista de intervalos gerada no passo anterior
                class_ranges = rules[feature][class_id]
                
                for r in class_ranges:
                    write_feature_class_rule(
                        writer=f,
                        feature_idx=idx_feature,
                        class_id=class_id,
                        start=r["start"],
                        end=r["end"],
                        prob=r["value"]
                    )
                    
        # 2. Configurações de roteamento padrão (opcional, dependendo do design)
        # Se o seu switch precisar de regras base para IPv4 ou para ler os contadores,
        # elas podem ser adicionadas aqui.
        
    print(f"Arquivo de tabelas gerado com sucesso em: {output_path}")

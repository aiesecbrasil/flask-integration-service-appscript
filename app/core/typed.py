from functools import wraps
from typing import get_type_hints, Any, get_origin
from inspect import signature
from pydantic import TypeAdapter, BaseModel
from flask import request, jsonify

def typed(func):
    if not callable(func):
        raise TypeError(f"@typed só pode ser aplicado a funções.")

    sig = signature(func)
    hints = get_type_hints(func)
    return_type = hints.pop("return", None)

    input_adapters = {name: TypeAdapter(tp) for name, tp in hints.items()}
    output_adapter = TypeAdapter(return_type) if return_type else None

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        validated = {}
        json_body = request.get_json(silent=True)

        for name, adapter in input_adapters.items():
            hint = hints.get(name)
            value = None

            # --- DETECÇÃO DE MODELO ---
            # Usamos o hint direto para identificar se é uma classe Pydantic
            is_pydantic = isinstance(hint, type) and issubclass(hint, BaseModel)

            # --- LÓGICA DE CAPTURA ---
            if is_pydantic and json_body is not None:
                value = json_body
            elif name in bound.arguments and bound.arguments[name] is not sig.parameters[name].default:
                value = bound.arguments[name]
            elif json_body and isinstance(json_body, dict) and name in json_body:
                value = json_body[name]
            elif request.args and name in request.args:
                value = request.args[name]

            # --- A CONVERSÃO REAL (DICT -> OBJETO) ---
            if value is not None:
                try:
                    # Se já for a instância correta (chamada interna), apenas usa
                    if isinstance(value, hint):
                        validated[name] = value
                    elif is_pydantic:
                        # FORÇA a transformação de DICT para OBJETO
                        # model_validate garante que data.nome funcione
                        validated[name] = hint.model_validate(value)
                    else:
                        # Para tipos comuns (int, str), usa o adapter
                        validated[name] = adapter.validate_python(value)
                except Exception as e:
                    return jsonify({"error": f"Erro no campo '{name}'", "details": str(e)}), 422
            else:
                if sig.parameters[name].default is sig.parameters[name].empty:
                    return jsonify({"error": f"Campo '{name}' é obrigatório."}), 400

        # Agora a função recebe OBJETOS reais, não dicionários
        result = func(**validated)

        if output_adapter:
            try:
                # Se o resultado for um objeto, validamos o dump dele
                if isinstance(result, BaseModel):
                    result = output_adapter.validate_python(result.model_dump())
                else:
                    result = output_adapter.validate_python(result)
            except Exception as e:
                return jsonify({"error": "Erro na validação de saída", "details": str(e)}), 500

        # Serialização final para o Flask
        if isinstance(result, BaseModel):
            return jsonify(result.model_dump())
        elif isinstance(result, (dict, list)):
            return jsonify(result)

        return result

    return wrapper

__all__ = ["typed"]
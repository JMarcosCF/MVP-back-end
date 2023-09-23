from pydantic import BaseModel
from typing import Optional, List
from model.equipamento import Equipamento

class EquipamentoSchema(BaseModel):
    """
        Define como um novo equipamento a ser inserido
        deve ser representado.
    """

    modelo: str = "DVP14SS2"
    fabricante: str = "Delta"

class EquipamentoBuscaSchema(BaseModel):
    """
        Define como deve ser a estrutura que representa
        a busca. Que será realizada apenas com base no 
        nome do equipamento.
    """

    modelo: str = "Modelo Teste"

class ListagemEquipamentosSchema(BaseModel):
    """
        Define como uma listagem de equipamentos será
        retornado.
    """

    equipamentos:List[EquipamentoSchema]

def apresenta_equipamentos(equipamentos: List[Equipamento]):
    """
        Retorna uma representação do equipamento seguindo
        o schema definido em EquipamentoViewSchema.
    """

    result = []
    for equipamento in equipamentos:
        result.append({
            "modelo": equipamento.modelo,
            "fabricante": equipamento.fabricante
        })

    return {"equipamentos": result}

class EquipamentoViewSchema(BaseModel):
    """
        Define como um produto será retornado: 
        equipamento.
    """

    id: int = 1
    modelo: str = "DVP14SS2"
    fabricante: str = "DELTA"

class EquipamentoDelSchema(BaseModel):
    """
        Define como deve ser a estrutura do dado retornado
         após uma requisição de remoção.
    """
    msn: str
    modelo: str

def apresenta_equipamento(equipamento: Equipamento):
   """
        Retorna uma representação do produto seguindo
        o schema definido em EquipamentoViewSchema.
   """ 

   return{
       "id": equipamento.id,
       "modelo": equipamento.modelo,
       "fabricante": equipamento.fabricante
   }
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Equipamento
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0" )
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção da documentação: Swagger, Redoc ou RapiDoc")
equipamento_tag = Tag(name="Equipamento", description="Adição, visualização e remoção de equipamentos à base ")


@app.get('/', tags=[home_tag])
def home():
    """
        Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/cadastrar_equipamento', tags=[equipamento_tag],
          responses={"200": EquipamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema })
def add_equipamento(form: EquipamentoSchema):
    """
        Cadastrar um novo Equipamento à base de dados 
        Retorna uma representação dos equipamentos.
    """

    equipamento = Equipamento(
        modelo=form.modelo,
        fabricante=form.fabricante
    )
    logger.debug(f"Adicionado equipamento de modelo: '{equipamento.modelo}'")
    try:
        # Criar conexão com a base
        session = Session()
        # Adicionar equipamento
        session.add(equipamento)
        # Efetivando o comando de adição de novo equipamento na tabela
        session.commit()
        logger.debug(f"Adicionado equipamento de modelo: '{equipamento.modelo}'")
        return apresenta_equipamento(equipamento), 200
    
    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do InegrityError
        error_msg = "Equipamento de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar equipamento '{equipamento.modelo}', {error_msg} ")
        return {"msn": error_msg}, 400
    
    except Exception as e:
        # Caso um erro fora do previsto
        error_msg = "Não foi possével salvar novo equipamento :/"
        logger.warning(f"Erro ao adicionar equipamento '{equipamento.modelo}', {error_msg}")
        return {"msn": error_msg}, 400
    
@app.get('/buscar_equipamento', tags=[equipamento_tag],
         responses={"200": EquipamentoViewSchema, "404": ErrorSchema})
def get_buscar_produto(query: EquipamentoBuscaSchema):
    """
        Faz a busca por um Equipamento a partir id
        Retorna uma representação dos equipamentos.
    """
    equipamento_modelo = unquote(unquote(query.modelo)) 
    logger.debug(f"Coletando dados sobre o equiamento #{equipamento_modelo}")
    # Criando conexão com a base 
    session = Session()
    # Fazendo a busca
    equipamento = session.query(Equipamento).filter(Equipamento.modelo == equipamento_modelo).first()

    if not equipamento:
        # Se o equipamento não for encontrado
        error_msg = "Equipamento não encontrado na base :/"
        logger.warning(f"Erro ao buscar equipamento '{equipamento_modelo}', {error_msg}")
        return {"msn": error_msg}, 404
    else:
        logger.debug(f"Equipamento encontrado: '{equipamento.modelo}'")
        # Retorna a representação do equipamento
        return apresenta_equipamento(equipamento), 200
    
@app.delete('/deleta_equipamento', tags=[equipamento_tag],
            responses={"200": EquipamentoDelSchema, "404": ErrorSchema})
def del_equipamento(query: EquipamentoBuscaSchema):
    """
        Deleta um equipamento a partir no modelo informado
        Retorna uma mensagem de confirmação da remoção.
    """

    equipamento_modelo = unquote(unquote(query.modelo))
    print(equipamento_modelo)
    logger.debug(f"Deletando dados sobre o produto '{equipamento_modelo}'")
    # Cria conexão com a base
    session = Session()
    # Fazendo a remoção
    remov = session.query(Equipamento).filter(Equipamento.modelo == equipamento_modelo).delete()
    session.commit()

    if remov:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deleando equipamento '{equipamento_modelo}'")
        return {"msn": "Equipamento removido", "modelo": equipamento_modelo}
    else:
        # Se o equipamento não foi encontrado na base 
        error_msg = "Equipamento não encontrado na base :/"
        logger.warning(f"Erro ao deletar equipamento '{equipamento_modelo}', '{error_msg}'")
        return {"msn": error_msg}, 404
    
@app.get('/listar_equipamentos', tags=[equipamento_tag],
         responses={"200": ListagemEquipamentosSchema, "404": ErrorSchema})
def get_listar_equipamentos():
    """
        Faz a busca de todos os equipamentos cadastrados na base
        Retona uma representação da listagem de equipamentos.
    """
    logger.debug(f"Coletando os equipamentos")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    equipamentos = session.query(Equipamento).all()

    if not equipamentos:
        # Se não há equipamentos cadastrados na base
        return {"equipamentos": []}, 200
    else:
        logger.debug(f"%d equipamentos encontrados" % len(equipamentos))
        # Retorna a representação de equipamento
        print(equipamentos)
        return apresenta_equipamentos(equipamentos), 200
    
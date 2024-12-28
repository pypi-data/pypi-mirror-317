import json
from mapafiscal.domain.services import MapaFiscalBuilder, ContextoFiscal
from mapafiscal.domain.common import NaturezaOperacao, TipoCliente, Finalidade, RegimeTributacao, PerfilContribuinte
from mapafiscal.interfaces.repositorio_interface import RepositorioInterface
from mapafiscal.domain.aggregates import MapaFiscal

class CenarioBuilder:
    """Classe para construção do mapa fiscal a partir de um arquivo de configuração."""

    def __init__(self, cenario_file: str, repositorio: RepositorioInterface):
        self.cenario_file = cenario_file
        self.repositorio = repositorio

    def build_cenario(self) -> MapaFiscal:
        
        with open(self.cenario_file, encoding="utf-8") as file:            
                config = json.load(file)
                
                cliente= config["cliente"]
                produtos = config.get("produtos", [])
                cenarios = config.get("cenarios", [])
                uf_origem = config["uf_origem"]
                regime_tributacao = RegimeTributacao.from_value(config["regime_tributacao"])
                perfil_contribuinte = PerfilContribuinte.from_value(config["perfil_contribuinte"])
        
        contexto = ContextoFiscal(uf_origem=uf_origem,
                                regime_tributacao=regime_tributacao,
                                perfil_contribuinte=perfil_contribuinte,
                                repositorio=self.repositorio)
        
        # Construindo mapa fiscal
        mapa_builder = MapaFiscalBuilder(cliente=cliente, contexto=contexto)
        
        for produto in produtos:    
            classe_fiscal = mapa_builder.build_classe_fiscal(codigo=produto.get("codigo"), 
                                                            ncm=produto.get("ncm"), 
                                                            descricao=produto.get("descricao", ""), 
                                                            origem=produto.get("origem", 0),
                                                            cest=produto.get("cest", ""),
                                                            segmento=produto.get("segmento", ""),
                                                            fabricante_equiparado=produto.get("fabricante_ou_equiparado", False))
            

            mapa_builder.build_classes_st(classe_fiscal=classe_fiscal)
            
            for cenario in cenarios:
            
                mapa_builder.build_cenarios(grupo=cenario.get("grupo", "padrao"),
                                            natureza_operacao=NaturezaOperacao.from_value(cenario["natureza_operacao"]),
                                            tipo_cliente=TipoCliente.from_value(cenario["tipo_cliente"]),
                                            finalidade=Finalidade.from_value(cenario["finalidade"]),
                                            classe_fiscal=classe_fiscal,
                                            uf_list=cenario.get("uf_list"))
                
                mapa_builder.build_operacoes(grupo=cenario.get("grupo", "padrao"), classe_fiscal=classe_fiscal)     
                    
        return mapa_builder.build(f"Mapa Fiscal - {cliente}")    


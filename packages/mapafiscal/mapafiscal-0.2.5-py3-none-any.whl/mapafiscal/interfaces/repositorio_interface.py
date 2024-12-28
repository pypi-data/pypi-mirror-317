from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar, List, Optional

# Um tipo genérico para ser usado nos métodos do repositório
T = TypeVar('T')

class RepositorioInterface(ABC, Generic[T]):
    """
    Interface para repositórios de persistência de dados.
    Define os métodos básicos que qualquer repositório deve implementar.
    """

    @abstractmethod
    def adicionar(self, obj: T, clazz: Type[T]) -> None:
        """
        Adiciona um novo objeto ao repositório.
        Args:
            obj (T): Objeto a ser adicionado.
            clazz (Type[T]): Classe do objeto.
        """
        pass

    @abstractmethod
    def obter_por_id(self, id: int, clazz: Type[T]) -> Optional[T]:
        """
        Obtém um objeto pelo ID.
        Args:
            id (int): Identificador único do objeto.
            clazz (Type[T]): Classe do objeto.

        Returns:
            Optional[T]: O objeto correspondente ou None caso não exista.
            clazz (Type[T]): Classe do objeto.
        """
        pass

    @abstractmethod
    def atualizar(self, obj: T, clazz: Type[T]) -> None:
        """
        Atualiza um objeto existente no repositório.
        Args:
            obj (T): Objeto com as alterações para ser atualizado.
            clazz (Type[T]): Classe do objeto.
        """
        pass

    @abstractmethod
    def remover(self, id: int, clazz: Type[T]) -> None:
        """
        Remove um objeto do repositório pelo ID.
        Args:
            id (int): Identificador único do objeto a ser removido.
            clazz (Type[T]): Classe do objeto.
        """
        pass

    @abstractmethod
    def listar_todos(self, clazz: Type[T]) -> List[T]:
        """
        Lista todos os objetos presentes no repositório.

        Args:
            clazz (Type[T]): Classe do objeto.
            
        Returns:
            List[T]: Lista de todos os objetos do repositório.
        """
        pass

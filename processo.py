class Processo:
    def __init__(self, id, data, nome, pai, mae, obs):
        self.id = id
        self.data = data
        self.nome = nome
        self.pai = pai
        self.mae = mae
        self.obs = obs

    def __eq__(self, o: object) -> bool:
        return self.__class__ == o.__class__ and self.id == o.id and self.data == o.data and self.nome == o.nome and \
               self.pai == o.pai and self.mae == o.mae and self.obs == o.obs

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return 'ID: ' + self.id

import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item import ExtensionResultItem


class SocinExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, SocinCommandListener())


class SocinCommandListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        args = query.strip().split()

        if not args:
            return [self._invalid_command()]

        comando = args[0].lower()

        if comando in ["desliga", "reinicia"]:
            if len(args) != 2:
                return [self._invalid_command()]
            try:
                minutos = int(args[1])
                acao = "-h" if comando == "desliga" else "-r"
                subprocess.run(["shutdown", acao, f"+{minutos}"])

                return [
                    ExtensionResultItem(
                        icon='images/socin.png',
                        name=f"{'Desligamento' if comando == 'desliga' else 'Reinicialização'} agendado para {minutos} minuto(s)",
                        description=f"O sistema será {'desligado' if comando == 'desliga' else 'reiniciado'} em {minutos} minuto(s).",
                        on_enter=None
                    )
                ]
            except ValueError:
                return [self._tempo_invalido()]

        elif comando == "cancela":
            subprocess.run(["shutdown", "-c"])
            return [
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Cancelado",
                    description="Qualquer desligamento ou reinício agendado foi cancelado.",
                    on_enter=None
                )
            ]

        else:
            return [self._invalid_command()]

    def _invalid_command(self):
        return ExtensionResultItem(
            icon='images/socin.png',
            name="Comando inválido",
            description='Use:\n"socin desliga 5", "socin reinicia 5" ou "socin cancela"',
            on_enter=None
        )

    def _tempo_invalido(self):
        return ExtensionResultItem(
            icon='images/socin.png',
            name="Tempo inválido",
            description="Informe o tempo em minutos. Exemplo: socin desliga 5",
            on_enter=None
        )


if __name__ == '__main__':
    SocinExtension().run()

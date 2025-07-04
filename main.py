import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class SocinExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryListener())
        self.subscribe(ItemEnterEvent, ItemEnterListener())


class KeywordQueryListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        args = query.strip().split()

        if not args:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Comandos: desliga, reinicia, cancela",
                    description="Ex: socin desliga 5",
                    on_enter=HideWindowAction()
                )
            ])

        comando = args[0].lower()

        if comando in ['desliga', 'reinicia']:
            if len(args) != 2 or not args[1].isdigit():
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/socin.png',
                        name="Tempo inválido",
                        description="Ex: socin desliga 5",
                        on_enter=HideWindowAction()
                    )
                ])

            minutos = int(args[1])
            acao = "Desligar" if comando == 'desliga' else "Reiniciar"

            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name=f"{acao} em {minutos} minuto(s)",
                    description=f"O sistema será {acao.lower()}ado em {minutos} minuto(s).",
                    on_enter=ExtensionCustomAction({
                        "comando": comando,
                        "minutos": minutos
                    }, keep_app_open=False)
                )
            ])

        elif comando == 'cancela':
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Cancelar agendamento",
                    description="Cancelar desligamento ou reinício pendente",
                    on_enter=ExtensionCustomAction({
                        "comando": "cancela"
                    }, keep_app_open=False)
                )
            ])

        else:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/socin.png',
                    name="Comando inválido",
                    description="Use: desliga, reinicia ou cancela",
                    on_enter=HideWindowAction()
                )
            ])


class ItemEnterListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        comando = data.get("comando")

        try:
            if comando == 'desliga':
                minutos = int(data.get("minutos", 0))
                subprocess.run(["shutdown", "-h", f"+{minutos}"])

            elif comando == 'reinicia':
                minutos = int(data.get("minutos", 0))
                subprocess.run(["shutdown", "-r", f"+{minutos}"])

            elif comando == 'cancela':
                subprocess.run(["shutdown", "-c"])
        except Exception as e:
            print(f"Erro ao executar comando: {e}")

        return HideWindowAction()


if __name__ == '__main__':
    SocinExtension().run()
